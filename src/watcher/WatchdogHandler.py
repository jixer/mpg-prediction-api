from watchdog.events import FileSystemEventHandler
import os
from data import model

class WatchdogHandler(FileSystemEventHandler):
    def on_created(self, event):
        """
        event.event_type
            'modified' | 'created' | 'moved' | 'deleted'
        event.is_directory
            True | False
        event.src_path
            path/to/observed/file
        """

        model.train_model(event.src_path)
        os.remove(event.src_path)
        print(event.src_path)