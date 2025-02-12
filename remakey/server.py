from contextlib import asynccontextmanager
from typing import List, Optional, Union
from fastapi import FastAPI, Request, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import uvicorn

from enums import KeyNames
from key_logger_commander import KeyLoggerManager
from remap_layer import ActionsEnum
from utils import serialize_layer_mapping
from fastapi.templating import Jinja2Templates

key_logger_manager = KeyLoggerManager()


@asynccontextmanager
async def lifespan(app: FastAPI):
    global key_logger_manager
    print("Starting Key Logger Manager...")
    key_logger_manager.start_thread()
    key_logger_manager.start()

    yield  # This suspends execution until the app shuts down

    print("Stopping Key Logger Manager...")
    key_logger_manager.stop()
    key_logger_manager.join_thread()


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")


class ChangeLayerBody(BaseModel):
    layer_id: str


class KeyActionConfiguration(BaseModel):
    type: Optional[ActionsEnum] = None
    value: Optional[Union[int, KeyNames, List[KeyNames]]] = None


class KeyConfiguration(BaseModel):
    action: Optional[KeyActionConfiguration] = None


# Define the exported type alias
KeyMappingType = Union[KeyConfiguration, int, KeyNames, List[KeyNames], None]


# Define LayerMapping Model
class LayerMapping(BaseModel):
    mapping: dict[KeyNames, KeyMappingType]


class AddRemapToLayerBody(BaseModel):
    layer_id: str
    key: KeyNames
    value: str


def get_key_logger_manager():
    return key_logger_manager  # Return the existing instance


@app.post("/start")
async def handle_start_command(
    manager: KeyLoggerManager = Depends(get_key_logger_manager),
):
    print("Received start command")
    manager.start()


@app.post("/stop")
async def handle_stop_command(
    manager: KeyLoggerManager = Depends(get_key_logger_manager),
):
    print("Received stop command")
    manager.stop()


@app.get("/clear-logs")
async def clear_logs():
    key_logger_manager.clear_logs()
    return "success"


@app.get("/logs")
async def get_logs():
    logs = key_logger_manager.get_logs()
    return {"logs": logs}


@app.get("/sse")
async def get_sse(request: Request):
    return StreamingResponse(
        key_logger_manager.get_change_layer_logs_generator(),
        media_type="text/event-stream",
    )


@app.get("/layers")
async def get_layers():
    layers = key_logger_manager.get_layers()
    result = []

    for layer in layers:
        result.append({"id": layer.id, "name": layer.name})

    return result


@app.get("/layers/{layer_id}/mapping")
async def get_layer_mapping(layer_id: str):
    mapping = serialize_layer_mapping(key_logger_manager.get_layer_mapping(layer_id))

    return mapping


@app.post("/layers/{layer_id}/mapping")
async def add_remap_to_layer(
    layer_id: str, add_remap_to_layer_body: AddRemapToLayerBody
):
    key_logger_manager.add_remap_to_layer(
        layer_id, add_remap_to_layer_body.key, add_remap_to_layer_body.value
    )


@app.post("/change-layer")
async def change_layer(change_layer_body: ChangeLayerBody):
    key_logger_manager.set_current_layer_by_id(change_layer_body.layer_id)
    return "success"


@app.get("/editor")
async def get_editor(request: Request):
    return templates.TemplateResponse("keyboard.html", {"request": request})


def main():
    print("Remakey server is running...")
    uvicorn.run("server:app", host="0.0.0.0", port=5000)


if __name__ == "__main__":
    main()
