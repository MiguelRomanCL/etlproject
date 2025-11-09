# 📘 Prefect-Ready Blueprint (M1 IA-Asistido)

## 1. Propósito

Este repositorio será migrado a una **arquitectura Prefect-ready M1**, eliminando workers, pools y orquestaciones internas.  
El objetivo es lograr una separación clara entre las etapas **Extract – Transform – Load**, exponer flujos Prefect declarativos (`@flow`, `@task`) y permitir que el código sea **comprensible, modificable y auditable por una IA** bajo el estándar M1.

---

## 2. Estructura objetivo

```
src/
  core/
    extractors/
    transformers/
    loaders/
    pipelines/
  infrastructure/
    db/
    http/
prefect_flows/
  main_flow.py
config/
  settings.py
  config.yaml
docs/
  adr/
  prompts/
tests/
```

Cada carpeta debe tener un propósito único:
- **extractors/** → conexión a fuentes de datos (SQL, API, blob).
- **transformers/** → limpieza, agregación y enriquecimiento.
- **loaders/** → exportación a lago de datos o destino final.
- **prefect_flows/** → define la orquestación (`@flow`, `@task`).
- **docs/adr/** → decisiones técnicas y trazabilidad.
- **tests/** → validación funcional y de contratos.

---

## 3. Convenciones semánticas IA

| Elemento | Requisito | Ejemplo |
|-----------|-----------|----------|
| **Decoradores Prefect** | Usar `@flow` y `@task` declarativos (Prefect 3.x). | `@flow(name="Conversion Flow")` |
| **Docstrings estructurados** | Incluir gramática YAML embebida (`# FLOW: extract→transform→load→output`). | `# FLOW: extract→transform→load` |
| **Schemas** | Pydantic + `.model_json_schema()` para validar y exportar a JSON-LD. | `schemas/conversion_input.py` |
| **Configuración** | `config.yaml` y `settings.py` con metadata clara (`#CFG: source=SQL; scope=infra`). | |
| **ADRs** | Formato Q&A: *Context → Decision → Consequence*. | `docs/adr/refactor_2025_monitor_one.md` |

---

## 4. Ejemplo de refactor mínimo

### Antes (Legacy)
```python
def run_conversion():
    data = get_data_from_sql()
    result = transform_data(data)
    save_to_somewhere(result)
```

### Después (Prefect-ready)
```python
from prefect import flow, task

@task
def extract_data():
    return get_data_from_sql()

@task
def transform_data_task(data):
    return transform_data(data)

@task
def load_data_task(result):
    save_to_somewhere(result)

@flow(name="Conversion Flow")
def conversion_flow():
    data = extract_data()
    transformed = transform_data_task(data)
    load_data_task(transformed)
```

---

## 5. Instrucciones para IA

> **Objetivo del refactor automático:**
>
> - Detectar funciones o módulos donde se mezclen pasos de extracción, transformación o carga y **moverlos** a carpetas dedicadas (`extractors/`, `transformers/`, `loaders/`).
> - Crear archivos en `prefect_flows/` que declaren los flujos con `@flow` y `@task`.
> - Incorporar **docstrings estructurados YAML** con descripciones `# FLOW:` y `# STEP:`.
> - Generar documentación del cambio en `docs/adr/refactor_<fecha>.md` explicando:
>   - Contexto
>   - Decisión tomada
>   - Consecuencias y mejoras
> - **No eliminar lógica de negocio**: el refactor debe mantener la funcionalidad original.
> - Asegurar que el código resultante pueda ser ejecutado por **Prefect** como flujo declarativo.

---

## 6. Validación post-refactor

- Ejecutar `pytest` y validar que los resultados coincidan con los del código original.  
- Verificar que los flujos pueden correrse con `prefect deployment run` o `prefect server start`.  
- Confirmar que `@flow` y `@task` están correctamente definidos y que los módulos E/T/L son independientes.

---

## 7. Resultado esperado

El repositorio debe transformarse en una **base Prefect-ready e IA-compatible**, donde:

- Cada paso está modularizado (E/T/L).  
- Prefect controla la orquestación, no el código interno.  
- El código se “explica a sí mismo” mediante docstrings estructurados.  
- La IA puede entender, validar y regenerar componentes con mínima supervisión.  

> 🔹 “El código no solo se ejecuta: se explica, se audita y se mejora con ayuda de la IA.”
