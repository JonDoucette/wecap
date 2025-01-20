from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon

class SystemTray(QSystemTrayIcon):
    def __init__(self, icon_path, main_window):
        super().__init__(QIcon(icon_path), main_window)
        self.main_window = main_window
        self.setToolTip("Wecap")

        # Create a context menu for the tray icon
        self.tray_menu = QMenu()
        self.show_action = QAction("Show", self.tray_menu)
        self.show_action.triggered.connect(self.on_show_window)
        self.close_action = QAction("Close", self.tray_menu)
        self.close_action.triggered.connect(self.exit_application)
        self.tray_menu.addAction(self.show_action)
        self.tray_menu.addAction(self.close_action)
        self.setContextMenu(self.tray_menu)

        # Show tray icon
        self.show()

        # Connect tray icon click to bring up the main window
        self.activated.connect(self.on_tray_icon_clicked)

    def on_tray_icon_clicked(self, reason):
        """Handle tray icon clicks and bring the main application window to the foreground."""
        if reason == QSystemTrayIcon.Trigger:  # Trigger is typically a left-click
            self.on_show_window()

    def on_show_window(self):
        """Bring the main application window to the foreground."""
        self.main_window.show()
        self.main_window.activateWindow()
        self.main_window.raise_()

    def send_notification(self, title, message):
        """Send a system tray notification reminding the user."""
        self.showMessage(
            title,
            message,
            QSystemTrayIcon.Information,
            5000  # Duration in milliseconds
        )

    def exit_application(self):
        """Exit the application."""
        self.hide()
        self.main_window.close()
