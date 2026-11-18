const { app, BrowserWindow, shell, ipcMain, Menu, Tray } = require('electron');
const path = require('path');

let mainWindow = null;
let tray = null;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1280,
        height: 820,
        minWidth: 960,
        minHeight: 600,
        title: "TubeDZ — YouTube Sans Pub 🇩🇿",
        icon: path.join(__dirname, 'logo.png'),
        backgroundColor: '#0b0c10',
        autoHideMenuBar: true,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false,
            enableRemoteModule: false,
            sandbox: true
        }
    });

    // Load local index.html with fallback
    const startUrl = path.join(__dirname, 'index.html');
    mainWindow.loadFile(startUrl).catch(() => {
        mainWindow.loadURL('https://tubedz.onrender.com');
    });

    // Open external links safely in system default browser
    mainWindow.webContents.setWindowOpenHandler(({ url }) => {
        if (!url.includes('youtube.com/embed')) {
            shell.openExternal(url);
            return { action: 'deny' };
        }
        return { action: 'allow' };
    });

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

// App lifecycle
app.whenReady().then(() => {
    createWindow();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});
