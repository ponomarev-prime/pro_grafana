from flask import Flask
from prometheus_client import make_wsgi_app, CollectorRegistry, Gauge

app = Flask(__name__)
registry = CollectorRegistry()

# Создаем метрику с именем 'app_response_time'
app_response_time = Gauge('app_response_time', 'Response time of the app in seconds', registry=registry)

@app.route('/metrics')
def metrics():
    # Возвращаем метрики в формате Prometheus
    return make_wsgi_app().full_dispatch_request()

@app.route('/')
def index():
    # Здесь будет ваш код приложения
    app_response_time.set_to_current_time()
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True, port=8000)
