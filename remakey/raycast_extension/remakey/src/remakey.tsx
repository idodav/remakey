import { Action, ActionPanel, Icon, List, open, showToast, Toast } from "@raycast/api";
import axios from "axios";
import { useEffect, useState } from "react";

const API_URL = "http://localhost:5000"; // Your FastAPI server

type Layer = {
    id: string;
    name: string;
};

type Layers = Layer[];

type Remap = {
    [key: string]: {
        action: {
            type: string;
            value: string | number;
        };
    } | string; // To handle direct key-to-key mappings
};

export default function Command() {
    const [layers, setLayers] = useState<Layers>([]);
    const [remaps, setRemaps] = useState<Remap | null>(null);
    const [selectedLayer, setSelectedLayer] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);

    // Fetch available layers
    useEffect(() => {
        axios.get<Layers>(`${API_URL}/layers`)
            .then((response) => {
                setLayers(response.data);
            })
            .catch((error) => {
                console.error(error);
                showToast({ style: Toast.Style.Failure, title: "Failed to fetch layers" });
            });
    }, []);

    // Fetch remaps for selected layer
    const fetchRemaps = async (layerId: string) => {
        setIsLoading(true);
        try {
            const response = await axios.get<Remap>(`${API_URL}/layers/${layerId}/mapping`);
            setRemaps(response.data);
            setSelectedLayer(layerId);
        } catch (error) {
            console.error(error);
            showToast({ style: Toast.Style.Failure, title: "Failed to fetch remaps" });
        }
        setIsLoading(false);
    };

    // Function to send start/stop commands
    const sendCommand = async (command: "start" | "stop" | "clear-logs") => {
        try {
            await axios.post(`${API_URL}/${command}`);
            showToast({ style: Toast.Style.Success, title: `Keylogger ${command}ed` });
        } catch (error) {
            console.error(error);
            showToast({ style: Toast.Style.Failure, title: `Failed to ${command} keylogger` });
        }
    };

    // Function to change layer
    const setLayer = async (layerId: string) => {
        try {
            await axios.post(`${API_URL}/change-layer`, { layer_id: layerId }, {
                headers: { "Content-Type": "application/json" }
            });
            showToast({ style: Toast.Style.Success, title: `Successfully changed layer` });
        } catch (error) {
            console.error(error);
            showToast({ style: Toast.Style.Failure, title: `Failed to set layer` });
        }
    };

    return (
        <>
            <List isLoading={isLoading} searchBarPlaceholder="Search...">

                {/* General Actions */}
                <List.Section title="Actions">
                    <List.Item
                        title="Open Config Editor"
                        actions={
                            <ActionPanel>
                                <Action title="Start" onAction={() => open("http://localhost:5000/editor", "Google Chrome")} />
                            </ActionPanel>
                        }
                    />
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

                {/* Layer Selection */}
                <List.Section title="Layers">
                    {layers.length === 0 ? (
                        <List.Item title="No layers available" />
                    ) : (
                        layers.map((layer) => (
                            <List.Item
                                key={layer.id}
                                title={layer.name}
                                actions={
                                    <ActionPanel>
                                        <Action title="Set Layer" onAction={() => setLayer(layer.id)} />
                                        <Action title="View Remaps" onAction={() => fetchRemaps(layer.id)} />
                                    </ActionPanel>
                                }
                            />
                        ))
                    )}
                </List.Section>

                {/* Display Remaps */}
                {selectedLayer && remaps && (
                    <List.Section title="Action Remaps">
                        {Object.entries(remaps)
                            .filter(([_, mapping]) => typeof mapping !== "string")
                            .map(([key, mapping]) => {
                                const actionType = mapping.action.type;
                                const actionValue = mapping.action.value;

                                // More beautiful formatting
                                const formattedSubtitle =
                                    actionType === "SET_LAYER"
                                        ? `🗂 Layer ${actionValue}`
                                        : actionType === "INVOKE_COMMAND"
                                            ? `🖥 Run Command → ${actionValue}`
                                            : `⚡ ${actionType} → ${actionValue}`;

                                return (
                                    <List.Item
                                        key={key}
                                        title={key}
                                        subtitle={formattedSubtitle}
                                        icon={
                                            actionType === "SET_LAYER"
                                                ? Icon.Layers
                                                : actionType === "INVOKE_COMMAND"
                                                    ? Icon.Terminal
                                                    : Icon.ExclamationMark
                                        }
                                        actions={
                                            <ActionPanel>
                                                <Action.CopyToClipboard title="Copy Remap" content={`${key} → ${formattedSubtitle}`} />
                                                {actionType === "INVOKE_COMMAND" && (
                                                    <Action
                                                        title="Run Command"
                                                        icon={Icon.Terminal}
                                                        onAction={() => axios.post(`${API_URL}/run-command`, { command: actionValue })}
                                                    />
                                                )}
                                            </ActionPanel>
                                        }
                                    />
                                );
                            })}
                    </List.Section>
                )}
            </List>
        </>
    );
}
