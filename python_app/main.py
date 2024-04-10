from flask import Flask, Response
from prometheus_client import make_wsgi_app, CollectorRegistry, Gauge, generate_latest
import time
import threading
import os

app = Flask(__name__)
registry = CollectorRegistry()

# Создаем метрику с именем 'PY_RESPONSE_TIME'
PY_RESPONSE_TIME = Gauge('PY_RESPONSE_TIME', 'Response time of the app in seconds', registry=registry)
# Создаем метрику для подсчета посещений
PY_VISITS = Gauge('PY_VISITS', 'Number of visits to /', registry=registry)

# Получаем имя хоста из переменной окружения HOSTNAME
hostname = os.environ.get('HOSTNAME', '0.0.0.0')  # Если HOSTNAME не установлено, используем значение по умолчанию

def record_metrics():
    while True:
        # Записываем метрики состояния приложения
        # Здесь может быть ваша логика для записи состояния приложения
        # Например, PY_RESPONSE_TIME.set() для записи времени ответа
        PY_RESPONSE_TIME.set(time.time())  # Пример: устанавливаем текущее время в качестве метрики времени ответа
        # Ждем 5 секунд перед записью следующих метрик
        time.sleep(5)

# Запускаем поток для записи метрик каждые 5 секунд
metrics_thread = threading.Thread(target=record_metrics)
metrics_thread.daemon = True
metrics_thread.start()

@app.route('/metrics')
def metrics():
    # Возвращаем метрики в формате Prometheus
    return Response(generate_latest(registry), mimetype='text/plain')

@app.route('/')
def index():
    # Записываем метрику посещения страницы
    PY_VISITS.inc()
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=False, host=hostname, port=8010)
