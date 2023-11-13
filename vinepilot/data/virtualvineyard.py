import os
import logging 

from http.server import SimpleHTTPRequestHandler, HTTPServer
from vinepilot.config import Project

img_path = os.path.abspath("./vinepilot/data/vineyards/vineyard_000/vineyard_1.svg")

class AnnotationGenerator():
    def __init__(self) -> None:
        #self.svg_file: str = svg_path
        self.annotations: list = [os.path.abspath("./vinepilot/data/vineyards/vineyard_000/vineyard_1.svg")]
        self.current: int = 0
        self.limit: int = len(self.annotations)

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.limit: 
            self.current += 1
            return self.annotations[self.current-1]
        else: raise StopIteration



class VineyardViewer():
    def __init__(self) -> None:
        self.annotation_generator = AnnotationGenerator()
        self.annotations: list = [a for a in self.annotation_generator]
        self.port: int = 8000
        self.html: str = ""
    
    def build(self):
        self.html += "<html><body><h1>VineyardViewer</h1>"
        for img in self.annotations: self.html += f'<img src="/{img}">'
        self.html += "</body></html>"

    class Server(SimpleHTTPRequestHandler):
        def __init__(self, content: str):
            self.content = content

        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self.content.encode())

    def show(self):
        self.build()
        adress = (" ", self.port)
        httpd = HTTPServer(adress, self.Server(content=self.html))
        logging.INFO(f"Running on port {self.port}.")
        httpd.serve_forever()