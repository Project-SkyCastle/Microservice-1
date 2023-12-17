import uvicorn
from src.endpoints import app, db
import os

if __name__ == "__main__":
    pid = os.getpid()
    with open("/tmp/path.txt", "w") as f:
        print(pid)
        f.write(str(pid))
    db.reconnect()
    uvicorn.run(app, host="0.0.0.0", port=8012)
