import schedule
import time
import threading
import logging
import os, sys
import datetime
# import daemon

format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")
days_old_files = 30
mypath = "videos"
time_of_deletion = "03:30"

def delete_old():
    onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    print("Checking for",days_old_files,"day(s) old files...")
    now = time.time()
    for file in onlyfiles:
        file_path = mypath+"/"+file
        date = file.split()[0]
        time_stamp = time.mktime(datetime.datetime.strptime(date,"%Y-%m-%d").timetuple())
        if(time_stamp < (now - days_old_files*24 * 3600)):
            try:
                os.remove(file_path)
                print("Old file Removed:", file_path)
            except Exception as e:
                print("\n----- BEGIN DELETION EXCEPTION ------")
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno)
                print(e)
                print("------ END DELETION EXCEPTION ------")
    
    print("Done checking")

def thread_function():
    schedule.every().day.at(time_of_deletion).do(delete_old)
    # schedule.every(1).minutes.do(delete_old)

    while True:
        schedule.run_pending()
        time.sleep(60)

def start_job(new_day = 30):
    global days_old_files
    assert new_day >= 0, "Can not check on negative day old files"
    days_old_files = new_day
    print("Maximum age of files before deletion:", days_old_files)

    logging.info("Starting thread for auto delete, thread runs each day at " + time_of_deletion)
    # print(daemon.__file__)
    # with daemon.DaemonContext():
    x = threading.Thread(target=thread_function)
    x.start()

if __name__ == "__main__":
    start_job()