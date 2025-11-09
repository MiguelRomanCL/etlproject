# Análisis de fuentes de datos y dependencias – rama `refactor/prefect-ready`

## 1. Visión general del flujo
La API expuesta por `POST /conversion` en `src/app/routers/conversion.py` delega la lógica al servicio `get_conversion` (`src/app/services/conversion.py`). Este servicio:
1. Obtiene parámetros iniciales de crianza y entidades (`get_init_params`).
2. Recupera pesos, consumo de alimento y datos de mortalidad (`get_weights_consumptions`).
3. Carga estándares productivos desde archivos CSV (`get_standard`).
4. Calcula conversiones acumuladas con Polars y persiste el resultado (`save_conversion`).

Todo el ciclo depende de una base de datos PostgreSQL multitenant y de archivos locales incluidos en el repositorio.

## 2. Fuentes de información

### 2.1 Base de datos relacional (PostgreSQL)
- **Motor:** `postgresql+psycopg2` configurado en `src/app/db/sql/database.py`.
- **Cadena de conexión:** se construye con `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_SERVER` y `POSTGRES_DATABASE`, más el parámetro `application_name` igual al nombre del proyecto.
- **Gestión de esquemas:** `get_session(tenant_schema)` aplica `schema_translate_map={None: tenant_schema}` para aislar los datos por tenant. El esquema se determina por el campo `client` incluido en el cuerpo del request (`get_db`).
- **Tablas consultadas:**
  - `breedings`, `breeding_data`, `entities` (`select_init_params`).
  - `animal_weights`, `food_consumptions`, `mortalities`, `breedings`, `breeding_data` (`select_breeding_weights_consumption_data`).
  - `animal_conversion` (upsert en `save_conversion`).
- **Consultas principales:** definidas en `src/app/db/sql/queries.py` mediante SQLAlchemy/SQLModel.

### 2.2 Archivos locales
- `src/maestroestandargenetica_202510160912_pollos.csv`
- `src/maestroestandargenetica_202510161619_cerdos.csv`

`get_standard()` (`src/app/utilities/get_data.py`) lee ambos archivos con Polars, agrega el campo `id_stage` (1 para pollos, 2 para cerdos), concatena los datos y filtra la genética `ROSS - 2020`. Después renombra columnas para armonizarlas con el resto del flujo y devolver un DataFrame con los estándares acumulados.

### 2.3 Servicios externos adicionales
- **Redis:** el paquete `redis` figura en `src/requirements.txt` y el README menciona soporte de caché, pero no existe código que instancie o utilice Redis en esta rama (el módulo `src/app/db/redis/__init__.py` está vacío).
- **Otros servicios (Influx, data lakes, APIs externas, Prefect, etc.):** no se referencian ni se consumen en el código actual.

## 3. Módulos y funciones de obtención y carga de datos

| Fase | Ubicación | Función/Clase | Descripción |
|------|-----------|---------------|-------------|
| **Extracción** | `src/app/db/sql/database.py` | `get_db`, `get_session` | Gestionan sesiones SQLModel hacia PostgreSQL con schema por tenant. |
| | `src/app/db/sql/queries.py` | `select_init_params` | Construye el `SELECT` de parámetros iniciales combinando `breedings`, `entities` y `breeding_data`. |
| | `src/app/db/sql/queries.py` | `select_breeding_weights_consumption_data` | Recupera pesos, consumo y mortalidad vinculados a una lista de `id_breeding`. |
| | `src/app/utilities/get_data.py` | `get_init_params`, `get_weights_consumptions` | Ejecutan las consultas anteriores usando `Session.exec` y gestionan errores con logging. |
| **Transformación** | `src/app/services/conversion.py` | `get_conversion` | Realiza cálculos con Polars: imputación de stock, derivación de conversiones, unión con parámetros y estándares. |
| | `src/app/utilities/get_data.py` | `get_standard` | Procesa los CSV para generar el DataFrame de referencia. |
| **Carga** | `src/app/utilities/get_data.py` | `save_conversion` | Ejecuta `upsert_animalshed_conversion` (INSERT ... ON CONFLICT) y hace commit sobre `animal_conversion`. |
| | `src/app/db/sql/queries.py` | `upsert_animalshed_conversion` | Define la instrucción `INSERT`/`ON CONFLICT` para `animal_conversion`. |

## 4. Gestión de conexiones y sesiones
- **Motor global:** instanciado una única vez (`engine = create_engine(...)`).
- **Scope por tenant:** `get_session` aplica `schema_translate_map` y se envuelve en un context manager que cierra la sesión tras su uso.
- **Inyección en FastAPI:** `get_db` es un dependency provider asíncrono. Lee el cuerpo de la petición buscando `client`. Si no está presente, lanza `HTTPException 422`.
- **Comportamiento transaccional:** `save_conversion` ejecuta la sentencia upsert y confirma con `session.commit()`. Ante errores revierte con `session.rollback()`.

## 5. Variables de entorno

| Variable | Ubicación de uso | Propósito |
|----------|------------------|-----------|
| `POSTGRES_SERVER` | `src/app/config/config.py` → `DATABASE_URL` | Host o `host:puerto` del servidor PostgreSQL. |
| `POSTGRES_USER` | `src/app/config/config.py` → `DATABASE_URL` | Usuario para autenticarse contra la base de datos. |
| `POSTGRES_PASSWORD` | `src/app/config/config.py` → `DATABASE_URL` | Contraseña del usuario. |
| `POSTGRES_DATABASE` | `src/app/config/config.py` → `DATABASE_URL` | Base de datos que contiene los esquemas tenant. |

> El README menciona `PROJECT_NAME`, pero en esta rama el nombre del proyecto se define como constante en `src/app/config/config.py` y no depende de variables de entorno.

Estas variables deben declararse (por ejemplo en `.env`) y se cargan mediante `os.getenv` al iniciar la aplicación. El archivo `.env_example` incluido en la raíz muestra un ejemplo completo con descripciones.

## 6. Esquema de datos y dependencias
- **Modelos SQLModel** (`src/app/models/*.py`): definen las tablas consultadas, incluyendo claves primarias y campos relevantes para los cálculos (peso, consumo, stock, edades, sexos, etc.).
- **Esquema Polars** (`src/app/schemas/polars.py`): asegura tipos esperados al convertir listas de dicts a DataFrame antes de operar.
- **Dependencias de terceros:**
  - `fastapi` y `uvicorn` para la API.
  - `sqlmodel`/`sqlalchemy` para la capa SQL.
  - `polars` para manipulación de datos tabulares.
  - `psycopg2-binary` como driver PostgreSQL.
  - `redis` está instalado pero sin uso en código.

## 7. Requisitos para ejecutar localmente
1. **Servicios:**
   - Instancia de PostgreSQL accesible con los esquemas y tablas mencionados.
   - Archivos CSV incluidos en `src/` (deben permanecer en esa ruta o actualizar `get_standard`).
   - No se requiere Redis ni otros servicios adicionales para la funcionalidad actual.
2. **Variables de entorno:** definir las cuatro variables de la sección 5 (`.env` a partir de `.env_example`).
3. **Dependencias Python:** instalar desde `src/requirements.txt` o mediante `uv sync`/`pip install -e .`.
4. **Ejecución:** iniciar FastAPI con `uvicorn main:app --reload` desde `src/`. Al consumir `POST /conversion`, enviar un JSON con `{"client": "<schema>"}` para seleccionar el tenant.

## 8. Resumen ejecutivo
- **Fuentes de datos:** PostgreSQL (tablas `breedings`, `breeding_data`, `entities`, `animal_weights`, `food_consumptions`, `mortalities`, `animal_conversion`) y archivos CSV de estándares genéticos. Redis u otros almacenes no se usan.
- **Variables de entorno:** `POSTGRES_SERVER`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DATABASE`.
- **Servicios externos requeridos:** solo PostgreSQL; los estándares se sirven desde archivos locales.
- **Para ejecutar en local:** base PostgreSQL con los esquemas esperados, configurar las variables indicadas, mantener los CSV en `src/` y ejecutar la app FastAPI.
