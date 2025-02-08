from typing import List, Optional, Union
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from remakey.enums import KeyNames
from key_logger_commander import KeyLoggerManager
from remap_layer import ActionsEnum
from remakey.utils import serialize_layer_mapping

app = FastAPI()
key_logger_manager = KeyLoggerManager()


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


@app.get("/layers/{layer_id}/mapping")
async def get_layer_mapping(layer_id: str):
    mapping = serialize_layer_mapping(key_logger_manager.get_layer_mapping(layer_id))

    return mapping


@app.post("/layers/{layer_id}/mapping")
async def add_remap_to_layerlayer(
    layer_id: str, add_remap_to_layer_body: AddRemapToLayerBody
):
    key_logger_manager.add_remap_to_layer(
        layer_id, add_remap_to_layer_body.key, add_remap_to_layer_body.value
    )


@app.post("/change-layer")
async def change_layer(change_layer_body: ChangeLayerBody):
    key_logger_manager.set_current_layer_by_id(change_layer_body.layer_id)
    return "success"


def main():
    print("Remakey server is running...")
    key_logger_manager.start_thread()
    uvicorn.run(app, host="0.0.0.0", port=5000)
    key_logger_manager.join_thread()


if __name__ == "__main__":
    main()
