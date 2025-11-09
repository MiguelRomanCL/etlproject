# 🧠 Refactor Instructions for Codex (M1 Prefect-Ready Transition)

## Objetivo general
Migrar este repositorio a una **arquitectura Prefect-ready** según los documentos:
- `docs/prefect_ready_blueprint.md`
- `docs/prefect_ready_justificacion.md`

El código actual utiliza *workers* y *pools* internos para auto-orquestarse.
Estos deben ser **eliminados o desactivados**, dejando que **Prefect controle la ejecución**.

## Instrucciones paso a paso

1. **Identificar puntos de orquestación interna**
   - Buscar funciones o clases que actúen como `main`, `worker`, `scheduler`, `queue`, o `pool`.
   - Reemplazarlas por un flujo central en `prefect_flows/main_flow.py`.

2. **Separar responsabilidades**
   - Mover extracción, transformación y carga a `src/core/extractors`, `src/core/transformers`, `src/core/loaders`.
   - Crear funciones limpias, sin dependencias entre capas.

3. **Declarar tareas Prefect**
   - Agregar decoradores `@task` a cada bloque funcional (extract, transform, load).
   - Crear un flujo principal con `@flow` que los encadene.

4. **Eliminar lógica redundante**
   - Borrar o comentar cualquier bucle de reintento, sleep, thread o pool.
   - Prefect maneja reintentos y paralelismo de forma nativa.

5. **Documentar cambios**
   - Crear archivo `docs/adr/refactor_<fecha>.md` explicando:
     - Qué módulos fueron reestructurados.
     - Qué partes de orquestación se eliminaron.
     - Cómo ejecutar el nuevo flujo con Prefect.

6. **Mantener equivalencia funcional**
   - No eliminar lógica de negocio (predicciones, cálculos, lecturas SQL).
   - Verificar que las funciones entreguen los mismos outputs que antes.

## Formato esperado
Al finalizar, el repo debe incluir:

```
src/core/{extractors, transformers, loaders}
prefect_flows/main_flow.py
config/{settings.py, config.yaml}
docs/{adr/, prefect_ready_blueprint.md, prefect_ready_justificacion.md}
tests/
```

Cada función principal debe tener un docstring YAML estructurado:

```python
# FLOW: extract→transform→load
# STEP: extract_data_from_sql
```

## Resultado esperado
- El flujo se ejecuta con:
  ```bash
  prefect deployment run "main_flow"
  ```
- No existen referencias a workers, pools ni colas internas.
- Prefect controla el flujo completo y registra cada tarea.

> 🔹 Nota final: No alterar los módulos de negocio (predicciones, transformaciones).  
> El cambio es **estructural y de orquestación**, no funcional.
