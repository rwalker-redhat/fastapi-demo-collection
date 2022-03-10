from fastapi import FastAPI
import uvicorn
from api import disney, auth

app = FastAPI()


def configure():
    configure_routing()


def configure_routing():
    app.include_router(auth.router)
    app.include_router(disney.router)


if __name__ == '__main__':
    configure()
    uvicorn.run(app,
                host='0.0.0.0',
                port=8002,
                log_level="debug",
                ssl_keyfile="localhost.key",
                ssl_certfile="localhost.crt")
else:
    configure()
