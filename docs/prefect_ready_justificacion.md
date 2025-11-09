# ⚙️ Justificación Técnica y Requerimientos del Enfoque Prefect-Ready (M1)

## 1. Contexto general

Actualmente, varios repositorios KPI mantienen una **lógica interna de orquestación** basada en *workers*, *pools* y *schedulers* propios.
Esa arquitectura fue útil en etapas iniciales —cuando cada KPI funcionaba de forma autónoma—, pero hoy se vuelve **redundante y costosa** dentro del marco operativo de **M1**, donde la orquestación de KPIs ya está **centralizada bajo Prefect** como estándar.

Esto genera una serie de problemas estructurales:

1. **Duplicación de orquestación:** los repositorios ejecutan sus propios flujos internos mientras M1 intenta orquestarlos externamente. Esto provoca desalineación y mayor complejidad operacional.
2. **Consumo innecesario de recursos:** los *workers* mantienen procesos activos (colas, threads, loops) incluso cuando Prefect ya ofrece ejecución bajo demanda, con gestión automática de dependencias y reintentos.

En síntesis: **la orquestación interna dejó de ser necesaria y pasó a ser contraproducente**.
Migrar a un enfoque **Prefect-ready** permitirá repositorios más ligeros, gobernables y totalmente integrados al flujo maestro de M1.

---

## 2. Propósito del cambio

El objetivo es **refactorizar los repositorios KPI existentes** para que deleguen toda la orquestación a Prefect, manteniendo en el código únicamente la **lógica funcional (E/T/L)**.
Esto implica que los repositorios dejen de operar como sistemas autónomos y pasen a comportarse como **unidades orquestables** dentro del marco de M1.

Los beneficios directos son:

- **Eliminación de procesos residentes** (workers y pools innecesarios).
- **Reducción de carga operativa y de costos de ejecución.**
- **Estandarización estructural**: todos los KPIs siguen la misma gramática `extract → transform → load`.
- **Observabilidad y auditoría unificada** bajo el dashboard Prefect.
- **Compatibilidad IA-asistida**: repositorios legibles, refactorizables y semánticamente consistentes para modelos.

---

## 3. Qué significa ser “Prefect-ready”

Un repositorio **Prefect-ready** define su flujo de ejecución **declarativamente**, usando los decoradores `@flow` y `@task` de Prefect.
No contiene lógica interna de scheduling, loops de ejecución ni workers residentes.

### Requisitos clave:

1. **Separación de responsabilidades**
    - `extractors/` → extracción de datos desde SQL, SAP, APIs o DataLake.
    - `transformers/` → limpieza, cálculo, agregación.
    - `loaders/` → publicación o guardado de resultados.
    - `prefect_flows/` → definición del flujo principal (`@flow`, `@task`).
2. **Orquestación declarativa**
    - Prefect controla dependencias, paralelismo, reintentos, alertas y logs.
    - Los flujos se ejecutan desde M1/Prefect, no desde scripts locales.
3. **Ejecución centralizada**
    - Cada flujo tiene visibilidad completa en el dashboard Prefect.
    - El estado, duración, inputs y outputs de cada tarea se registran automáticamente.

---

## 4. Conceptos clave: `@flow` y `@task`

Prefect usa una sintaxis declarativa simple que reemplaza la lógica interna de orquestación.

### 🔹 `@task` — Unidad atómica de trabajo

```python
from prefect import task

@task
def extract_data():
    return read_sql("SELECT * FROM tabla")
```
Cada @task representa una etapa individual del proceso (extract, transform o load).
Prefect puede ejecutarlas en paralelo, aplicar retries y registrar métricas detalladas.

### 🔹 `@flow` — Orquestador del pipeline

```python
from prefect import flow

@flow(name="Calcular Conversión")
def prediction_flow():
    data = extract_data()
    result = transform_data(data)
    load_to_somewhere(result)
```
El @flow define la secuencia lógica y las dependencias entre tareas.
Permite que Prefect las ejecute con control total y trazabilidad completa.

---

## 5. Por qué Prefect es el enfoque adhoc

Prefect encaja naturalmente en el estándar actual de M1 y soluciona las limitaciones del modelo anterior:

| Aspecto | Enfoque Legacy | Enfoque Prefect-ready |
|----------|----------------|-----------------------|
| **Orquestación** | Manual, en el propio código. | Externa, gobernada por Prefect. |
| **Uso de recursos** | Workers activos, consumo constante. | Ejecución bajo demanda, recursos optimizados. |
| **Logs y trazabilidad** | Locales y fragmentados. | Centralizados y auditables desde Prefect. |
| **Escalabilidad** | Limitada al entorno local. | Multi-agente, multi-nodo. |
| **Mantenimiento** | Scripts acoplados, poca reusabilidad. | Estructura modular E/T/L. |
| **Compatibilidad IA** | Código opaco, sin semántica estándar. | Código auto-descriptivo y refactorizable. |

En otras palabras, Prefect-ready es la forma natural de operar dentro del ecosistema M1:

- Ahorra recursos.
- Simplifica el mantenimiento.
- Mejora la observabilidad.
- Y sienta las bases para un desarrollo Human+AI coherente y gobernable.

---

## 6. Requisitos mínimos de implementación

1. Reestructurar los repositorios según el esquema:

```
src/core/{extractors, transformers, loaders, pipelines}
prefect_flows/
config/
docs/
tests/
```
2. Definir flujos principales en `prefect_flows/*.py` usando `@flow` y `@task`.
3. Eliminar schedulers, loops y workers internos.
4. Documentar la orquestación con docstrings tipo DSL (`# FLOW: extract→transform→load`).
5. Consolidar configuración en `config.yaml` y `.env`.
6. Validar equivalencia funcional mediante `pytest`.
7. Registrar las decisiones de migración en `docs/adr/refactor_<fecha>.md`.

---

## 7. Resultado esperado

Tras la migración, cada KPI podrá:

- Ser ejecutado, versionado y monitoreado desde Prefect sin código auxiliar.
- Integrarse directamente en los flujos M1 existentes.
- Operar con trazabilidad completa y logs unificados.
- Exponer una estructura modular, semántica y compatible con IA.

> 🔹 En resumen:
> El objetivo no es solo modernizar el código, sino alinear toda la capa de KPIs con el estándar operativo de M1, eliminando redundancias y permitiendo que Prefect —y, a futuro, la IA— sean quienes gestionen la orquestación de manera inteligente, trazable y eficiente.
