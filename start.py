import os
from time import sleep
import psutil
import subprocess

tempfile = "tempfile"


def find_main(p):
    return (
        p.info["name"].lower() == "python"
        and p.info["cmdline"]
        and "main.py" in p.info["cmdline"][-1]
    )


def restart():
    processes = [
        p for p in psutil.process_iter(attrs=["pid", "name", "cmdline"]) if find_main(p)
    ]

    print(processes)

    if processes:
        print("terminating ", processes[0])
        processes[0].terminate()

    subprocess.check_call(["python3", "-m", "pip", "install", "-r", "requirements.txt"])

    subprocess.Popen(
        ["python3", "/home/ec2-user/Microservice-1/main.py", ">>", "service.log"],
        close_fds=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
    )


def check_new_tempfile():
    prev_mtime = os.path.getmtime(tempfile)

    while True:
        curr_mtime = os.path.getmtime(tempfile)
        if prev_mtime != curr_mtime:
            print("Found new tempfile")
            restart()
            prev_mtime = curr_mtime

        sleep(1)


check_new_tempfile()
