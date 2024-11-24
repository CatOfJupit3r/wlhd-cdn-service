# wlhd-cdn-service

this is FastAPI cdn-like service to handle custom game logic for WLHD Projects. Run in Docker along side other services

## Environment Variables

- `PORT` — Port to run the service on.
- `HOST` — Host to run the service on.
- `ADMIN_TOKEN` — Token to access admin routes.
- `COORDINATOR_TOKEN` — Token to access coordinator routes.
- `SKIP_PREPARE` — If set to `True`, will skip preparing the service. Make sure that data folder is properly populated.
- `VALKEY_PORT` — Port to the Valkey service is running on.
- `VALKEY_HOST` — Host to the Valkey service is running on.
- `VALKEY_DB` — Database to use for Valkey.
- `VALKEY_KEY_LIFETIME` — Lifetime of the keys in Valkey.
