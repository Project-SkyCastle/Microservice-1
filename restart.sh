pid=$(ps -ef | grep "python main.py" | grep -v grep | awk '{print $2}')

if [ ! -z "${pid}" ]; then
    echo "killing ${pid}"
    kill $pid
fi

cd ~/Microservice-1"/ && git pull -f origin main && python3 -m pip install -r requirements.txt && python3 main.py > service.log &

exit 0