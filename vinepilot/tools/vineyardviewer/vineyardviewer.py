import os
from io import BytesIO
from PIL import Image
from flask import Flask, render_template, request, send_file, url_for

from vinepilot.config import Project
from vinepilot.utils import Transform, load_image_as_numpy


class VineyardViewer():
    def __init__(self) -> None:
        #Webapp
        self.port: int = Project.port
        self.host_address: str = Project.host_address
        self.templates: str = os.path.normpath(os.path.join(Project.base_dir, "./vinepilot/tools/vineyardviewer/templates")) 
        self.app = Flask(__name__, template_folder = self.templates)

        #Routes
        self.app.route("/")(self.home)
        self.app.route("/load_virtual")(self.load_virtual)
        self.app.route("/button_plus100", methods=['POST'])(self.button_plus100)
        self.app.route("/submit_parameters", methods=['POST'])(self.submit_parameters)

        #Parameters
        self.vineyard_number: int = 0
        self.position: tuple = (0,0)
        self.rotation: float = 0.0
        self.zoom_factor: float = 1.0

        #Images
        self.virtual = None

    #Tools
    def build_virtual(self):
        test_img: str = "./vinepilot/data/vineyards/vineyard_000/vineyard_000.png"
        img = load_image_as_numpy(test_img)
        img = Transform.new_center(img, self.position)
        img = Transform.rotate(img, self.rotation)
        img = Transform.zoom(img, self.zoom_factor)
        return img

    def load_virtual(self):
        #Get image
        img_arr = self.build_virtual()
        img = Image.fromarray(img_arr)

        #Write image to buffer
        self.virtual = BytesIO()
        img.save(self.virtual, "PNG")
        self.virtual.seek(0)
        return send_file(self.virtual, mimetype="image/png", as_attachment=True, download_name="virtual.png")
        

    #Pages
    def home(self):
        return render_template("home.html",
                            vineyard_number = self.vineyard_number,
                            current_pos_y = self.position[0],
                            current_pos_x = self.position[1],
                            current_rotation = self.rotation,
                            virtual = url_for("load_virtual"))

    #Actions
    def button_plus100(self):
        self.vineyard_number += 100
        return self.home()
    
    def submit_parameters(self):
        self.position = (float(request.form.get("pos_y")), float(request.form.get("pos_x")))
        self.rotation = float(request.form.get("rotation"))
        return self.home()


    def show(self):
        self.app.run(host=self.host_address, port=self.port, debug=True)
