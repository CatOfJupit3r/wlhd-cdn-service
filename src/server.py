from fastapi import FastAPI
from routes import apply_routes


app = FastAPI()

apply_routes(app)
