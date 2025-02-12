const { app, BrowserWindow, screen } = require('electron');

let win;

app.whenReady().then(() => {
    const { width, height } = screen.getPrimaryDisplay().workAreaSize;

    win = new BrowserWindow({
        width: 910,
        height: 280,
        x: ((width - 910) / 2), // Position it to the bottom-right corner
        y: height - 280,
        alwaysOnTop: true, // Keep the widget floating
        frame: false, // Remove window frame
        transparent: false, // Make it transparent
        resizable: true,
        movable: true,
        webPreferences: {
            nodeIntegration: true,
        },
    });

    win.loadURL(`file://${__dirname}/keyboard.html`);
});
