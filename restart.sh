pid=$(ps -ef | grep "python main.py" | grep -v grep | awk '{print $2}')

if [ ! -z "${pid}" ]; then
    kill pid
fi

cd ~/6156Project_SkyCastle-Microservice1/ &&
git pull -f origin main && python3 -m virtualenv .venv && source .venv/bin/activate &&  python -m pip install -r requirements.txt && python main.py

exit 0