import uvicorn
from service.main import factory

app = factory()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010, log_config="./settings/logging.conf")
