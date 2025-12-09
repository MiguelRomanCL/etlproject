# Situación Actual del Proyecto (Handover)

**Fecha**: 2025-12-09
**Contexto**: Retomando `msw-kpi-conversion` para refactorización a flujo lineal (sin workers/async).

## 1. El Problema Original
El código funcionaba perfectamente en el pasado, pero al intentar levantarlo hoy falló inmediatamente con errores críticos de arranque.
- **Error Principal**: `ValueError: not enough values to unpack` en `fastapi/applications.py`.
- **Causa**: Incompatibilidad de versiones tras actualizaciones automáticas o entornos sucios. La versión instalada de `pydantic` (2.12.1) introdujo cambios que rompieron la compatibilidad con la versión antigua de `fastapi` (0.119.0) que tenía el proyecto.

## 2. Acciones Tomadas y Soluciones

### A. Corrección de Dependencias
- Se detectó que actualizar solo Pydantic generaba conflictos con otras librerías.
- **Solución Definitiva**: Se actualizó **FastAPI a la versión 0.124.0+** y `pydantic` a `2.12.5`. Esto resolvió el problema de middleware.

### B. Entorno Virtual Nuevo (`.venv_v2`)
- El entorno original `.venv` estaba corrupto/inconsistente.
- Se creó un nuevo entorno limpio: **`.venv_v2`**.
- **IMPORTANTE**: Debes usar este entorno para ejecutar el proyecto.
  ```powershell
  .venv_v2\Scripts\Activate.ps1
  ```

### C. Mejora de Robustez (Error 500)
- Detectamos un error `500 Internal Server Error` al hacer POST con body vacío.
- **Fix**: Se modificó `src/app/db/sql/database.py` para manejar `JSONDecodeError` y devolver `400 Bad Request` en su lugar. El sistema es ahora más resiliente.

## 3. Estado Actual

- **Servidor**: Arranca correctamente (`INFO: Uvicorn running...`).
- **Endpoints**:
  - `GET /` -> Devuelve 404 (Correcto).
  - `POST /conversion` -> Operativo.
- **Robustez**: Responde 400 Bad Request ante inputs inválidos.
- **Base de Datos**: **Conexión Exitosa**.
- **Código**: Se verificó flujo lineal síncrono.
- **Ejecución**: ✅ **POST /conversion** (con cliente `tecnoandina`) retorna **200 OK**. Se corrigieron bugs en `get_data.py` (WindowsPath error y columna id_stage faltante) que impedían esto.
- **Dato Clave**: La lógica depende de que el CSV contenga ciertos atributos o sean inyectados manualmente como hicimos en el fix.

## 4. Próximos Pasos

El sistema está **completamente operativo y verificado**.

1. **Entorno**: Sigue usando `.venv_v2`.
2. **Deploy**: El código está listo para merge a main.

## 5. Guía Rápida para Ejecutar (Para Humanos)

Para "hacer que funcione" y guardar en la DB, no basta con abrir la página principal. Sigue estos pasos:

1.  Abre el navegador en: **http://127.0.0.1:8000/docs**
2.  Busca la barra verde que dice `POST /conversion`. Haz clic en la flecha para desplegarlo.
3.  Haz clic en el botón **"Try it out"** (arriba a la derecha del bloque).
4.  En el cuadro de texto "Request body", escribe el nombre de tu cliente real:
    ```json
    {
      "client": "nombre_de_tu_esquema_real"
    }
    ```
    > **IMPORTANTE**: El código no tiene el nombre del cliente escrito (es dinámico). Debes sacarlo de tu archivo `.env` local (variable `CLIENT` o `POSTGRES_USER`) o de tu base de datos (nombre del esquema, ej: `agrisuper`, `pollos`, etc).

5.  Haz clic en el botón azul grande **"Execute"**.

Ahí verás cómo la terminal empieza a procesar y, si el cliente es correcto, guardará los datos.

---
**Comando de arranque probado:**
```powershell
.venv_v2\Scripts\python.exe -m uvicorn main:app --reload
```
