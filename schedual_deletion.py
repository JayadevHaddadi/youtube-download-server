import schedule
import time
import threading
import logging
import delete_old_files

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")

def job():
    delete_old_files.del_old_files()

def thread_function():
    schedule.every().day.at("03:30").do(job)
    schedule.every(1).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

def start_job():
    logging.info("Starting thread for auto delete old files")
    x = threading.Thread(target=thread_function)
    x.start()

if __name__ == "__main__":
    start_job()