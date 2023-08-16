from flask import Flask, jsonify
import psutil
import platform

app = Flask(__name__)

@app.route("/get_live_info", methods=["GET"])
def get_live_info():
    cpu_percent = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    network_info = psutil.net_io_counters()
    python_version = platform.python_version()
    platform_info = platform.platform()

    live_info = {
        "cpuUsage": f"{cpu_percent}%",
        "memoryUsage": f"{memory.used / 1024 / 1024:.2f} MB",
        "networkActivity": f"{network_info.bytes_sent / 1024:.2f} KB sent",
        "pythonVersion": python_version,
        "platform": platform_info
    }

    return jsonify(live_info)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
