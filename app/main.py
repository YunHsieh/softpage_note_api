from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.stores import init_database
from app.routers import init_routers


app = FastAPI()

origins = [
    '*',
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

init_database(app)
init_routers(app)


@app.get('/heath_check')
async def heath_check():
    return { 'status': 'ok' }
