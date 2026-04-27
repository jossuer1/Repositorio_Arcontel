import requests
import platform

def obtener_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "0.0.0.0"

def obtener_dispositivo():
    return f"{platform.system()} - {platform.machine()}"