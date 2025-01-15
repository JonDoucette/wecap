from datetime import datetime, timedelta
from PyQt5.QtCore import QTimer, QObject

class NotificationHandler(QObject):
    def __init__(self, main_window, db_manager, system_tray):
        super().__init__()
        self.main_window = main_window
        self.db_manager = db_manager
        self.system_tray = system_tray
        self.check_interval = 3 * 60 * 60 * 1000  # Check once every 3 hours (in milliseconds)

        # Setup a QTimer to check weekly recap on Fridays
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_and_notify)
        self.timer.start(self.check_interval)

    def check_and_notify(self, first_time = False):
        """Check the database and send a notification if no entry exists for this week."""
        if self.is_friday():
            if not self.entry_exists_for_week():
                self.send_notification()
            if first_time:
                self.send_notification()

    def is_friday(self):
        """Check if today is Friday."""
        return datetime.now().weekday() == 4 # 4 corresponds to Friday

    def entry_exists_for_week(self):
        """Check the database for an entry in the current week."""
        start_of_week = datetime.now() - timedelta(days=datetime.now().weekday())
        end_of_week = start_of_week + timedelta(days=5)  # Up to Saturday

        count = self.db_manager.get_count_of_entries_between_times(start_of_week, end_of_week)
        return count > 0

    def send_notification(self):
        """Send a system tray notification reminding the user to fill out their recap."""
        self.system_tray.send_notification(
            "Weekly Recap Reminder",
            "Don't forget to fill out your weekly recap!"
        )
