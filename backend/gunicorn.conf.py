import multiprocessing

bind = "0.0.0.0:8000"
# Backpressure: prefer more processes with fewer connections per worker
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 60
graceful_timeout = 30
keepalive = 2
accesslog = "-"
errorlog = "-"

# Backpressure: cap concurrent sockets per worker
worker_connections = 200

# Recycle workers to avoid FD leaks under extreme load
max_requests = 1000
max_requests_jitter = 200



