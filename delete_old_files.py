import os
import datetime
import time

def del_old_files(days_old_files = 1,mypath = "videos"):
    onlyfiles = [f for f in os.listdir(mypath) if os.path.isfile(os.path.join(mypath, f))]
    print("Checking for",days_old_files,"day(s) old files...")
    now = time.time()
    for file in onlyfiles:
        file_path = mypath+"/"+file
        date = file.split()[0]
        time_stamp = time.mktime(datetime.datetime.strptime(date,"%Y-%m-%d").timetuple())
        if(time_stamp < (now - days_old_files*24 * 3600)):
            os.remove(file_path)
            print("Old file Removed:", file_path)
    print("Done checking")

if __name__ == "__main__":
    print("Calling del_old_files")
    del_old_files()
