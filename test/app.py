import psutil
import gpustat
import platform
import time


while True:
    # Información sobre la memoria RAM
    memory_info = psutil.virtual_memory()
    ram_total = memory_info.total
    ram_percent = memory_info.percent
    ram_available = memory_info.available

    # print(f"Uso de RAM: {memory_info.percent}%")
    # print(f"Memoria total: {memory_info.total / (1024 ** 3):.2f} GB")
    # print(f"Memoria disponible: {memory_info.available / (1024 ** 3):.2f} GB")

    # Información sobre la CPU
    cpu_percent = psutil.cpu_percent(interval=1)
    # print(f"Uso de CPU: {cpu_percent}%")

    # gpu_stats = gpustat.GPUStatCollection.new_query()
    # for gpu in gpu_stats.gpus:
    #     print(f"GPU {gpu.index}: {gpu.name}, Utilization: {gpu.utilization}%")

    # Información sobre el sistema operativo
    platform_system = platform.system()
    platform_version = platform.version()
    platform_machine = platform.machine()
    platform_processor = platform.processor()

    # print(f"Sistema operativo: {platform.system()}")
    # print(f"Versión del sistema operativo: {platform.version()}")
    # print(f"Arquitectura: {platform.machine()}")
    # print(f"Procesador: {platform.processor()}")

    json_data = {
        "ram": {
            "total": ram_total,
            "percent": ram_percent,
            "available": ram_available
        },
        "cpu": {
            "percent": cpu_percent
        },
        "platform": {
            "system": platform_system,
            "version": platform_version,
            "machine": platform_machine,
            "processor": platform_processor
        }
    }

    print(json_data)
    time.sleep(3)