# Usage Guide

This document describes how to run the conversion KPI service locally, how the FastAPI and Prefect entry points relate to each other, and the external services you must provision before testing the project.

## 1. Architecture at a Glance

- **FastAPI service** (`src/main.py`) exposes the REST API. It mounts the conversion router and depends on a request-scoped SQLModel session that selects the tenant schema from the incoming payload.【F:src/main.py†L1-L18】【F:src/app/db/sql/database.py†L24-L37】
- **Prefect flow** (`prefect_flows/main_flow.py`) orchestrates the same extract → transform → load steps as asynchronous tasks and expects the tenant schema as its `tenant` parameter.【F:prefect_flows/main_flow.py†L1-L41】
- **Shared business logic** lives under `src/core/{extractors, transformers, loaders}` and is reused by both execution paths.【F:src/app/services/conversion.py†L1-L23】【F:src/core/extractors/conversion.py†L1-L95】【F:src/core/transformers/conversion.py†L1-L138】【F:src/core/loaders/conversion.py†L1-L58】

With this layout, FastAPI continues to serve synchronous requests, while Prefect can run the same workload under external orchestration.

## 2. External Dependencies

Prepare the following services and assets before running either entry point:

- **PostgreSQL** with the schemas and tables expected by the SQLModel models and queries (e.g., `AnimalWeights`, `FoodConsumption`). The code connects through a tenant-aware DSN built from environment variables.【F:src/app/db/sql/database.py†L1-L23】【F:src/app/db/sql/queries.py†L1-L86】
- **Prefect 3.x** CLI and API access. You can target Prefect Cloud or a self-hosted Prefect server; an agent must be available to pick up deployments.
- **CSV catalog files** included in `src/` (Ross 2020 standards) for the standard conversion lookup used during transformations.【F:src/core/extractors/conversion.py†L42-L74】
- **Python 3.12** and project dependencies declared in `pyproject.toml` (FastAPI, Polars, SQLModel, Prefect, etc.).【F:pyproject.toml†L1-L32】

> **Note:** Redis is listed as a dependency but is not referenced by the current codebase, so you do not need it for local execution.

## 3. Environment Configuration

1. Copy the example file and update the placeholders with your PostgreSQL credentials:
   ```bash
   cp .env_example .env
   ```
2. Ensure the target database has a schema per tenant that mirrors the expected tables. The API will look for a `client` key in the request body and use it as the schema name.【F:src/app/db/sql/database.py†L24-L37】

## 4. Installing Dependencies

You can use either [uv](https://github.com/astral-sh/uv) or pip:

- With uv (recommended):
  ```bash
  uv sync
  ```
- With pip:
  ```bash
  pip install -e .
  ```

These commands install the shared runtime for both FastAPI and Prefect.

## 5. Running the FastAPI Service

1. Activate your virtual environment and load the `.env` file (for example by exporting variables or using `direnv`).
2. Start the API server from the project root:
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   The app factory defined in `src/main.py` will mount the conversion router automatically.【F:src/main.py†L1-L14】【F:src/app/routers/conversion.py†L1-L18】
3. Send a POST request that includes the tenant schema:
   ```bash
   curl -X POST \
     http://localhost:8000/conversion \
     -H "Content-Type: application/json" \
     -d '{"client": "tenant_schema"}'
   ```
   The dependency `get_db` reads the `client` field, creates a SQLModel session bound to that schema, and the service executes the extract/transform/load logic synchronously.【F:src/app/db/sql/database.py†L24-L37】【F:src/app/services/conversion.py†L12-L23】

### How FastAPI Fits In

FastAPI currently runs end-to-end without Prefect: it calls the shared core utilities directly and commits the results before returning the payload. This is useful for synchronous API consumption or manual testing without the Prefect control plane.【F:src/app/services/conversion.py†L12-L23】

## 6. Running the Prefect Flow

1. Authenticate against your Prefect server or cloud workspace (`prefect cloud login` or `prefect config set PREFECT_API_URL=...`).
2. Build and register a deployment for `main_flow`:
   ```bash
   prefect deploy prefect_flows/main_flow.py:main_flow --name main_flow --apply
   ```
3. Start an agent that can pick up the deployment (for example, the default work pool):
   ```bash
   prefect agent start --pool default-agent-pool
   ```
4. Trigger the flow with the tenant parameter:
   ```bash
   prefect deployment run "main_flow" --params '{"tenant": "tenant_schema"}'
   ```

The flow submits Prefect tasks for extraction, transformation, and loading, then returns the computed records. Because the tasks reuse the same core modules, the database writes and final payload match the FastAPI behaviour.【F:prefect_flows/main_flow.py†L19-L41】【F:src/core/loaders/conversion.py†L34-L48】

### How Prefect Fits In

Prefect acts as an external orchestrator: it replaces legacy workers/pools and governs retries, scheduling, and observability. The flow produces the same side effects as the API but under Prefect control, enabling automated scheduling or event-driven execution.

## 7. Running Both Together

FastAPI and Prefect can coexist:

- FastAPI serves HTTP clients and can be used for manual recalculations or as an integration point for other services.
- Prefect runs scheduled or ad-hoc ETL executions across tenants.
- Both rely on the same core modules and Postgres instance, so database transactions remain consistent across execution modes.【F:src/app/services/conversion.py†L12-L23】【F:prefect_flows/main_flow.py†L19-L41】

### Triggering Prefect from FastAPI (Optional)

The current code path does **not** trigger Prefect runs when the API endpoint is called; the calculation happens immediately within the request cycle. To let FastAPI request Prefect-managed executions you would need to:

1. Replace the direct call to `get_conversion` with a Prefect client invocation (e.g., `from prefect.client.orchestration import get_client`).
2. Submit `main_flow` with the tenant parameter via `await client.create_flow_run_from_deployment(...)` or by calling `main_flow.with_options(...).submit(...)`.
3. Return an acknowledgment or poll Prefect for completion before returning the final payload.

These changes are optional and are not present in the repository today.

## 8. Verifying the Results

- **FastAPI:** Inspect the HTTP response and confirm the upserted rows in `animal_conversion` (or the target table) after hitting the endpoint.
- **Prefect:** Monitor the run in the Prefect UI to ensure all tasks complete successfully and that the database contains the new records.
- **Logs:** Both execution modes log to `./logs/msw-conversion-m.log` by default, which helps validate the ETL stages.【F:src/app/config/logger.py†L7-L54】

By following this guide you can stand up the API, execute the Prefect flow, and understand how they complement each other in a Prefect-ready architecture.
