from src.utils.config import CONFIG
from src.application.service import service
from src.application.schedulers.summary_scheduler import start_scheduler

if __name__ == '__main__':
    service_conf = CONFIG['service']
    start_scheduler(service_conf)

    service.run(
        host=service_conf['host'],
        port=service_conf['port']
    )
