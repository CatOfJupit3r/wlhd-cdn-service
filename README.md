# wlhd-cdn-service

this is FastAPI cdn-like service to handle custom game logic for WLHD Projects. Run in Docker along side other services

## Environment Variables

- `PORT` — Port to run the service on.
- `HOST` — Host to run the service on.
- `ADMIN_TOKEN` — Token to access admin routes.
- `SKIP_PREPARE` — If set to `True`, will skip preparing the service. Make sure that data folder is properly populated.
