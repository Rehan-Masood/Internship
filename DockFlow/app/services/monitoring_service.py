import time
import psutil
from app.services.metrics_service import collect_metrics
from app.services.docker_service import list_containers

def collect_system():
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    net = psutil.net_io_counters()
    metrics = collect_metrics()
    return {
        "timestamp": time.time(),
        "cpu_percent": psutil.cpu_percent(interval=0.05),
        "memory_percent": memory.percent,
        "memory_used_mb": round(memory.used / 1024 / 1024, 1),
        "memory_total_mb": round(memory.total / 1024 / 1024, 1),
        "disk_percent": disk.percent,
        "network_sent_mb": round(net.bytes_sent / 1024 / 1024, 1),
        "network_recv_mb": round(net.bytes_recv / 1024 / 1024, 1),
        "requests": metrics["total_requests"],
        "errors": metrics["error_count"],
        "avg_response_ms": metrics["avg_response_ms"],
        "containers": list_containers(),
    }
