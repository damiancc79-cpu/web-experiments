#!/usr/bin/env python3
"""
PISTA CALIENTE — Servidor web local para la pagina de coleccionistas Hot Wheels.

Uso:
    python3 server.py              # arranca en http://localhost:8080
    python3 server.py 3000         # arranca en http://localhost:3000

Detener:
    Ctrl + C
"""

import http.server
import socketserver
import sys
import os
import webbrowser
from datetime import datetime

# Puerto por defecto (se puede sobreescribir por argumento)
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Colores ANSI para que la terminal tenga la onda Hot Wheels
RED = "\033[91m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


class PistaCalienteHandler(http.server.SimpleHTTPRequestHandler):
    """Handler personalizado con logging estilo coleccionista y headers anti-cache."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        # Sin cache durante desarrollo, asi los cambios se ven al recargar
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        # Header propio del proyecto, solo por estilo
        self.send_header("X-Powered-By", "Pista-Caliente/1.0")
        super().end_headers()

    def log_message(self, format, *args):
        # Reformateamos el log para que se vea limpio y tematico
        ts = datetime.now().strftime("%H:%M:%S")
        method_path = format % args
        status_color = RESET
        # Colorizar segun status code (esta en args[1])
        try:
            code = int(args[1])
            if 200 <= code < 300:
                status_color = "\033[92m"  # verde
            elif 300 <= code < 400:
                status_color = YELLOW
            elif code >= 400:
                status_color = RED
        except (IndexError, ValueError):
            pass

        sys.stdout.write(
            f"{DIM}[{ts}]{RESET} {status_color}{method_path}{RESET}\n"
        )
        sys.stdout.flush()


def banner(port):
    lines = [
        "",
        f"{RED}{BOLD}  ____  ___ ____ _____  _      ____    _    _     ___ _____ _   _ _____ _____ {RESET}",
        f"{RED}{BOLD} |  _ \\|_ _/ ___|_   _|/ \\    / ___|  / \\  | |   |_ _| ____| \\ | |_   _| ____|{RESET}",
        f"{RED}{BOLD} | |_) || |\\___ \\ | | / _ \\  | |     / _ \\ | |    | ||  _| |  \\| | | | |  _|  {RESET}",
        f"{RED}{BOLD} |  __/ | | ___) || |/ ___ \\ | |___ / ___ \\| |___ | || |___| |\\  | | | | |___ {RESET}",
        f"{RED}{BOLD} |_|   |___|____/ |_/_/   \\_\\ \\____/_/   \\_\\_____|___|_____|_| \\_| |_| |_____|{RESET}",
        "",
        f"  {YELLOW}//{RESET} El hogar de los coleccionistas Hot Wheels",
        f"  {YELLOW}//{RESET} Servidor de desarrollo local",
        "",
        f"  {BOLD}URL local:{RESET}     {RED}http://localhost:{port}/{RESET}",
        f"  {BOLD}URL red:{RESET}       {DIM}http://0.0.0.0:{port}/{RESET}",
        f"  {BOLD}Directorio:{RESET}    {DIM}{DIRECTORY}{RESET}",
        "",
        f"  {DIM}Detener: Ctrl + C{RESET}",
        f"  {DIM}{'-' * 78}{RESET}",
        "",
    ]
    print("\n".join(lines))


def run():
    # Permitir reusar el puerto (evita 'Address already in use' al reiniciar)
    socketserver.TCPServer.allow_reuse_address = True

    handler = PistaCalienteHandler

    try:
        with socketserver.TCPServer(("0.0.0.0", PORT), handler) as httpd:
            banner(PORT)
            # Abrir navegador automaticamente (opt-out con env var)
            if os.environ.get("NO_BROWSER") != "1":
                try:
                    webbrowser.open(f"http://localhost:{PORT}/")
                except Exception:
                    pass
            httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}  // Servidor detenido. Hasta la proxima vuelta.{RESET}\n")
        sys.exit(0)
    except OSError as e:
        if e.errno == 48:
            print(
                f"\n{RED}  // Error: el puerto {PORT} ya esta en uso.{RESET}\n"
                f"  {DIM}Prueba con otro puerto: python3 server.py 3000{RESET}\n"
            )
        else:
            print(f"\n{RED}  // Error: {e}{RESET}\n")
        sys.exit(1)


if __name__ == "__main__":
    run()
