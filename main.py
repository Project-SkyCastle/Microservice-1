import uvicorn
from src.endpoints import app, db

if __name__ == "__main__":
    db.reconnect()
    uvicorn.run(app, host="0.0.0.0", port=8012)
