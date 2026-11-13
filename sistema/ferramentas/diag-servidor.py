"""Ponte de diagnóstico entre o Windows e a máquina virtual de teste.

Uso:  python diag-servidor.py <script.sh> <pasta de saída>
Dentro da VM (rede NAT do VirtualBox, onde o Windows é 10.0.2.2):
  curl 10.0.2.2:8089 -o d ; sh d
O GET devolve o script; o que a VM enviar por PUT fica guardado na pasta de saída.
Só escuta em 127.0.0.1.
"""
import http.server
import pathlib
import sys

script = pathlib.Path(sys.argv[1])
saida = pathlib.Path(sys.argv[2])
saida.mkdir(parents=True, exist_ok=True)


class Ponte(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        corpo = script.read_bytes().replace(b'\r\n', b'\n')
        self.send_response(200)
        self.send_header('Content-Length', str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_PUT(self):
        n = int(self.headers.get('Content-Length', 0))
        nome = pathlib.PurePosixPath(self.path).name or 'envio'
        (saida / nome).write_bytes(self.rfile.read(n))
        self.send_response(200)
        self.end_headers()

    def log_message(self, *a):
        pass


http.server.ThreadingHTTPServer(('127.0.0.1', 8089), Ponte).serve_forever()
