import os
import logging
import cairosvg

from http.server import SimpleHTTPRequestHandler, HTTPServer
from vinepilot.config import Project


class VineyardAnimator():
    def __init__(self, vineyard_number: int) -> None:
        self.vineyard_dir: str = os.path.normpath(os.path.join(Project.vineyards_dir, f"./vineyard_{str(vineyard_number).zfill(3)}"))
        self.svg_path: str = self.vineyard_dir + f"/vineyard_{str(vineyard_number).zfill(3)}.svg"
        self.png_path: str = self.vineyard_dir + f"/vineyard_{str(vineyard_number).zfill(3)}.png"
        self.current: int = 0
        self.limit: int = 1 #Only for development

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.limit: 
            self.current += 1
            cairosvg.svg2png(url=self.svg_path, write_to=self.png_path)
            return self.png_path
        else: raise StopIteration



class VineyardViewer():
    def __init__(self) -> None:
        self.port: int = Project.port
        self.host_address: str = Project.host_address
        self.html: str = ""
        self.frames: list[str] = []
    
    def build(self):
        self.html += "<html><body><h1>VineyardViewer</h1>"
        for i, frame in enumerate(self.frames): 
            self.html += f"<h3>Frame {i}</h3>"
            self.html += f'''<img src="file://{frame}" alt="frame_{i}">'''
        self.html += "</body></html>"

    class Server(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, *kwargs)
            self.content = ""

        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self.content.encode())

    def show(self, vineyard_number: int):
        animator = VineyardAnimator(vineyard_number=vineyard_number)
        self.frames = [frame for frame in animator]
        self.build()
        server_address = (self.host_address, self.port)
        server = self.Server
        server.content = self.html
        httpd = HTTPServer(server_address, server)
        logging.info(f"VineyardViewer is running on https://{self.host_address}:{self.port}.")
        httpd.serve_forever()