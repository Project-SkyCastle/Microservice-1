import os
from time import sleep
import psutil
import subprocess

tempfile = "tempfile"


def restart():
    try: 
        with open("/tmp/path.txt", "r") as f:
            pid = f.readline()
            if pid:
                print("pid=", pid)
        process = psutil.Process(int(pid))
        process.terminate()
    except Exception as e:
        print(e)

    print("starting main.py...")
    subprocess.Popen(
        [
            "python3",
            "/home/ec2-user/Microservice-1/main.py",
            ">>",
            "/home/ec2-user/Microservice-1/service.log",
        ],
        close_fds=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
    )


def check_new_tempfile():
    prev_mtime = os.path.getmtime(tempfile)

    while True:
        try:
            curr_mtime = os.path.getmtime(tempfile)
            if prev_mtime != curr_mtime:
                print("Found new tempfile")
                restart()
                prev_mtime = curr_mtime
        except Exception as e:
            print(e)
        sleep(1)


check_new_tempfile()
