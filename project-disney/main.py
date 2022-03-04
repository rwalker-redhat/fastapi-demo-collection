from fastapi import FastAPI
import uvicorn
from api import disney

app = FastAPI()


def configure():
    configure_routing()


def configure_routing():
    app.include_router(disney.router)


if __name__ == '__main__':
    configure()
    uvicorn.run(app, host='0.0.0.0', port=8000)
else:
    configure()
