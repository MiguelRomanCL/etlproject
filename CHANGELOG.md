# Changelog

Todos los cambios importantes iran en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto adhiere a [Versionado Semántico](https://semver.org/spec/v2.0.0.html).


## [0.1.0] - 2025-10-22
### Added
- Implementación inicial del proyecto MSW KPI Conversion.
- API FastAPI para cálculo de conversión alimenticia.
- Modelos de base de datos para pesajes de animales, crianzas, conversión, entidades, consumo de alimentos y mortalidad.
- Integración con PostgreSQL mediante SQLAlchemy y SQLModel.
- Soporte para Redis.
- Procesamiento de datos con Polars.
- Router `/conversion` para cálculo de métricas de conversión.
- Servicio de conversión con lógica de negocio.
- Utilidades para obtención de datos y temporizadores.
- Configuración de logger personalizado.
- Archivo de configuración con variables de entorno.
- Pre-commit hooks para calidad de código (Black, isort, Ruff, autoflake).
- Archivos de estándares genéticos para pollos y cerdos en CSV.
- Docker y docker-compose para despliegue.
- Pipeline de Azure DevOps.
- Documentación inicial en README.md.

### Removed
- Módulos relacionados con consumo de agua (*water_consumption*).
- Integración con InfluxDB (*influx* database).
- Utilidades generales no utilizadas (*utils.py*).
