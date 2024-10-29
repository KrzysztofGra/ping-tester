from ping3 import ping
from graph import update_graph
import time
import subprocess
from pathlib import Path
import socket
import psutil


log_file = Path.home() / "Documents" / "ping-tester-disconnected.txt"
ping_times = []


def get_network_info():
    """Retrieve SSID and router IP (default gateway) for identifying the connected network."""
    ssid = None
    router_ip = None

    try:
        # Retrieve SSID using netsh
        result = subprocess.check_output("netsh wlan show interfaces", shell=True).decode('cp850')
        for line in result.split('\n'):
            if "SSID" in line and "BSSID" not in line:
                ssid = line.split(":")[1].strip()

        # Retrieve default gateway IP using psutil
        gateways = psutil.net_if_addrs()
        for interface, addrs in gateways.items():
            for addr in addrs:
                if addr.family == socket.AF_INET:  # Check for IPv4 addresses
                    router_ip = addr.address
                    break
            if router_ip:
                break

        return ssid, router_ip if router_ip else "Unknown IP"
    except Exception as e:
        print(f"Error retrieving network info: {e}")
        return ssid if ssid else "Unknown SSID", "Unknown IP"
    
def log_connection_loss(server_name):
    with open(log_file, "a") as file:
        ssid, router_ip = get_network_info()
        file.write(f"Lost connections: {time.strftime('%Y-%m-%d %H:%M:%S')}, SSID: {ssid}, Router IP: {router_ip}, Serwer: {server_name}\n")

def update_canvas_text(canvas, current_ping_text, foreground_color):
    canvas.delete("ping_text")
    offsets = [(0, 0), (2, 2), (0, 0), (2, 2)]
    for x_offset, y_offset in offsets:
        canvas.create_text(150 + x_offset, 20 + y_offset, text=current_ping_text,
                           font=("Arial", 20, "bold"), fill="black", tags="ping_text")
    canvas.create_text(150, 20, text=current_ping_text, font=("Arial", 20, "bold"),
                       fill=foreground_color, tags="ping_text")

def check_connection(root, canvas, ax, fig, server="google.com"):
    global ping_times
    try:
        response_time = ping(server)
        if response_time:
            ping_value_ms = response_time * 1000
            ping_times.append(ping_value_ms)
            if len(ping_times) > 50:
                ping_times.pop(0)
            current_ping_text = f"{int(ping_value_ms)} ms"
            color = "#99FF99" if ping_value_ms < 60 else "#FFFF99" if ping_value_ms < 100 else "#FFCC99"
            update_canvas_text(canvas, current_ping_text, color)
        else:
            ping_times.append(-1)
            if len(ping_times) > 50:
                ping_times.pop(0)
            log_connection_loss(server)
            update_canvas_text(canvas, "Offline", "#FF9999")
        update_graph(ax, fig, ping_times)
    except Exception as e:
        log_connection_loss(server)
        update_canvas_text(canvas, "Offline", "#FF9999")

def get_ssid():
    try:
        result = subprocess.check_output("netsh wlan show interfaces", shell=True).decode('utf-8')
        for line in result.split('\n'):
            if "SSID" in line:
                return line.split(":")[1].strip()
    except Exception as e:
        print(f"Błąd podczas pobierania SSID: {e}")
        return "Nieznana sieć"
    
