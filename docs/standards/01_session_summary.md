---
title: "Estándar de Resumen de Sesión (Session Logs)"
type: "standard"
status: "stable"
version: "1.0"
---

# 02 – Estándar de Resumen de Sesión (Protocolo de Cierre)

## 1. Objetivo
Desacoplar la ejecución técnica de la actualización del estado del proyecto. Al finalizar una sesión, el Orquestador **NO** edita `01_estado_actual.md` directamente. En su lugar, genera un archivo de log inmutable.

## 2. Ubicación y Naming
* **Carpeta:** `docs/session_logs/`
* **Nombre de archivo:** `YYYY-MM-DD_topic_brief.md`
    * *Ejemplo:* `2025-11-26_logging_implementation.md`

## 3. Estructura del Log (Template Obligatorio)

El resumen debe seguir estrictamente este formato Markdown:

```markdown
---
date: "YYYY-MM-DD"
topic: "Nombre de la Tarea"
status: "success | partial | failed"
---

# Resumen Ejecutivo
Breve párrafo (3 lineas máx) de qué se logró hoy.

# Acciones Concretas (Changelog)
* [MODIFICADO] `src/main.py`: Se agregó inyección de dependencias.
* [CREADO] `src/utils/logger.py`: Nueva clase Logger.
* [ELIMINADO] `src/old_script.py`.

# Hallazgos y Deuda Técnica
* ¿Se descubrió algo nuevo?
* ¿Quedó algo pendiente o roto?

# Instrucción para el Keeper
Sugerencia explícita de qué actualizar en el `01_estado_actual.md`.
* Ej: "Cambiar estado de Componente X a VERDE".
* Ej: "Agregar alerta de performance en sección de Riesgos".