# pylint: disable=invalid-name
import os

bind = "0.0.0.0:8000"
worker_class = "uvicorn.workers.UvicornWorker"
workers = int(os.environ.get("WORKERS", 4))
timeout = 120
accesslog = "var/log/access.log"
errorlog = "var/log/error.log"
