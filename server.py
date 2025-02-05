from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from key_logger_commander import KeyLoggerManager

app = FastAPI()
key_logger_manager = KeyLoggerManager()


class ChangeLayerBody(BaseModel):
    layer_id: str


@app.post("/start")
async def handle_command():
    print("Received start command")
    key_logger_manager.start()


@app.post("/stop")
async def handle_command():
    print("Received start command")
    key_logger_manager.stop()


@app.get("/clear-logs")
async def clear_logs():
    key_logger_manager.clear_logs()
    return "success"


@app.get("/logs")
async def get_logs():
    logs = key_logger_manager.get_logs()
    return {"logs": logs}


@app.get("/layers")
async def get_layers():
    layers = key_logger_manager.get_layers()
    result = []

    for layer in layers:
        result.append({"id": layer.id, "name": layer.name})

    return result


@app.post("/change-layer")
async def change_layer(change_layer_body: ChangeLayerBody):
    key_logger_manager.set_current_layer_by_id(change_layer_body.layer_id)
    return "success"


if __name__ == "__main__":
    key_logger_manager.start_thread()
    uvicorn.run(app, host="0.0.0.0", port=5000)
    key_logger_manager.join_thread()
