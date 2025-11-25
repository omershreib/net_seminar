from config import CONFIG
from detection.dashboard.app import run_app

monitor_parameters = CONFIG['system']['monitor_setup']


if __name__ == '__main__':
    run_app(monitor_parameters)
