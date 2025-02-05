import { Action, ActionPanel, List, showToast, Toast } from "@raycast/api";
import axios from "axios";
import { useEffect, useState } from "react";
const API_URL = "http://localhost:5000"; // Your FastAPI server

type Layer = {
    id: string;
    name: string;
}
type Layers = Layer[];

export default function Command() {
    const [layers, setLayers] = useState<Layers>([]);

    useEffect(() => {
        axios.get<Layers>(`${API_URL}/layers`).then((response) => {
            setLayers(response.data);
        });
    }, []);

    // Function to send start/stop commands
    const sendCommand = async (command: "start" | "stop" | "clear-logs") => {
        try {
            await axios.post(`${API_URL}/${command}`);
            showToast({ style: Toast.Style.Success, title: `Keylogger ${command}ed` });
        } catch (error) {
            console.log(error)
            showToast({ style: Toast.Style.Failure, title: `Failed to ${command} keylogger` });
        }
    };

    const setLayer = async (layerId: string) => {
        try {
            await axios.post(`${API_URL}/change-layer`, { "layer_id": layerId }, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            showToast({ style: Toast.Style.Success, title: `Successfully changed layer` });
        } catch (error) {
            console.log(error)
            showToast({ style: Toast.Style.Failure, title: `Failed to set layer` });
        }
    };

    return (
        <List searchBarPlaceholder="Search logs...">
            <List.Section title="Actions">
                <List.Item
                    title="Start Keylogger"
                    actions={
                        <ActionPanel>
                            <Action title="Start" onAction={() => sendCommand("start")} />
                        </ActionPanel>
                    }
                />
                <List.Item
                    title="Stop Keylogger"
                    actions={
                        <ActionPanel>
                            <Action title="Stop" onAction={() => sendCommand("stop")} />
                        </ActionPanel>
                    }
                />
                <List.Item
                    title="Clear logs"
                    actions={
                        <ActionPanel>
                            <Action title="Clear" onAction={() => sendCommand("clear-logs")} />
                        </ActionPanel>
                    }
                />
            </List.Section>

            <List.Section title="Layers">
                {layers.length === 0 ? (

                    <List.Item title="No layers available" />
                ) : (
                    layers.map((layer) => <List.Item key={layer.id} title={layer.name} actions={<ActionPanel>
                        <Action title="Set" onAction={() => { setLayer(layer.id) }} />
                    </ActionPanel>} />)
                )}
            </List.Section>
        </List>
    );
}
