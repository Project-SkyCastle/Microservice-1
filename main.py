import uvicorn
from src.endpoints import app, db
import os
import logging
from datetime import datetime


def write_pid():
    pid = os.getpid()
    with open("/tmp/path.txt", "w") as f:
        print(pid)
        f.write(str(pid))


if __name__ == "__main__":
    dt = datetime.now().strftime("%Y-%m-%d")

    logging.basicConfig(
        filename=f"service.log.{dt}",
        filemode="a",
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.DEBUG,
    )

    write_pid()
    db.reconnect()
    uvicorn.run(app, host="0.0.0.0", port=8012)
