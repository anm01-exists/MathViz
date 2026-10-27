"""
MathViz - Interactive Probability Studio Launcher
Automatically finds a free available port and launches the server.
"""

import socket
import uvicorn
import os
import sys
import webbrowser
import threading
import time

def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((host, port))
            return False
        except OSError:
            return True

def find_available_port(preferred_port: int = 8000, max_attempts: int = 50) -> int:
    for port in range(preferred_port, preferred_port + max_attempts):
        if not is_port_in_use(port):
            return port
    return preferred_port

def open_browser_after_delay(url: str, delay_sec: float = 1.0):
    def _open():
        time.sleep(delay_sec)
        try:
            webbrowser.open(url)
        except Exception:
            pass
    threading.Thread(target=_open, daemon=True).start()

if __name__ == "__main__":
    # Ensure project root is in sys.path
    project_root = os.path.dirname(os.path.abspath(__file__))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Allow custom port from command line arguments (e.g. python run.py 8080)
    target_port = 8000
    for arg in sys.argv[1:]:
        if arg.startswith("--port="):
            try:
                target_port = int(arg.split("=")[1])
            except ValueError:
                pass
        elif arg.isdigit():
            target_port = int(arg)

    if is_port_in_use(target_port):
        free_port = find_available_port(target_port + 1)
        print(f"\n[NOTE] Port {target_port} is already in use by another program on your machine.")
        print(f"[AUTO-SWITCH] Automatically switching MathViz to available port: {free_port}\n")
        selected_port = free_port
    else:
        selected_port = target_port

    server_url = f"http://127.0.0.1:{selected_port}"
    print("=" * 65)
    print("  MathViz: Interactive Probability Studio")
    print(f"  Live Server URL: {server_url}")
    print("=" * 65)
    print(f"Opening {server_url} in your browser...\n")

    # Automatically launch browser to the exact free port
    open_browser_after_delay(server_url, 1.2)

    uvicorn.run("backend.app:app", host="127.0.0.1", port=selected_port, reload=False)
