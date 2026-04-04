import time
import psutil
import os

def start_metrics():
    p = psutil.Process(os.getpid())
    return time.time(), p.memory_info().rss

def end_metrics(start_time, start_mem):
    p = psutil.Process(os.getpid())

    runtime = time.time() - start_time
    mem = (p.memory_info().rss - start_mem) / (1024 * 1024)

    return runtime, mem