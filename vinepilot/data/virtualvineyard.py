import os
import logging
import cairosvg

from flask import Flask, render_template
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
    app = Flask(__name__)

    def __init__(self) -> None:
        self.port: int = Project.port
        self.host_address: str = Project.host_address
        self.vineyard_number: int = 0

    @app.route("/")
    def serve(self, **kwargs):
        return render_template("./vineyardviewer.html",
                               vineyardnumber = self.vineyard_number)
    
    def show(self):
        self.app.run(host=self.host_address, port=self.port, debug=True)
