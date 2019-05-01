from watchdog.observers import Observer
import watcher.WatchdogHandler as wh
import time

file_path = "../input"

if __name__=="__main__":
    observer = Observer()
    observer.schedule(wh.WatchdogHandler(), path=file_path)
    observer.start()

    print("Process started.  Press Ctrl+c to exit...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()