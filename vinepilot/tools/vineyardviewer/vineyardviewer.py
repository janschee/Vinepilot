import os
import json

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
        self.static: str = os.path.normpath(os.path.join(Project.base_dir, "./vinepilot/tools/vineyardviewer/static")) 
        self.app = Flask(__name__, template_folder = self.templates, static_folder = self.static)

        #Routes
        self.app.route("/")(self.home)
        self.app.route("/load_virtual")(self.load_virtual)
        self.app.route("/button_frame_plus_100", methods=['POST'])(self.button_frame_plus_100)
        self.app.route("/button_frame_minus_100", methods=['POST'])(self.button_frame_minus_100)
        self.app.route("/button_frame_plus_10", methods=['POST'])(self.button_frame_plus_10)
        self.app.route("/button_frame_minus_10", methods=['POST'])(self.button_frame_minus_10)
        self.app.route("/submit_parameters", methods=['POST'])(self.submit_parameters)
        self.app.route("/set_frame", methods=['POST'])(self.set_frame)

        #Parameters
        self.vineyard_number: int = 0
        self.position: tuple = (0,0)
        self.rotation: float = 0.0
        self.zoom_factor: float = 1.0
        self.frame: int = 0

        #Images
        self.virtual = None

        #Database
        self.vineyards: str = Project.vineyards_dir
        self.trajectory: dict = json.load(open(os.path.join(self.vineyards, "./vineyard_000/trajectory_000.json"), "r"))

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
    
    def switch_frame(self, step_size):
        self.frame += int(step_size)

    def update_parameters(self):
        for waypoint in self.trajectory["waypoints"]:
            if int(waypoint["frame"]) == self.frame:
                self.position = waypoint["position"]
                self.rotation = waypoint["rotation"]
                break

    def save_parameters(self):
        for i, waypoint in enumerate(self.trajectory["waypoints"]):
            if int(waypoint["frame"]) == self.frame:
                self.trajectory["waypoints"][i]["position"] = self.position
                self.trajectory["waypoints"][i]["rotation"] = self.position
                break
        
        #If frame has no annotations yet
        #TODO: Generate new entry

    #Pages
    def home(self):
        self.update_parameters()
        return render_template("home.html",
                            vineyard_number = self.vineyard_number,
                            current_pos_y = self.position[0],
                            current_pos_x = self.position[1],
                            current_rotation = self.rotation,
                            current_zoom_factor = self.zoom_factor,
                            current_frame = self.frame,
                            virtual = url_for("load_virtual"))

    #Actions
    def submit_parameters(self):
        self.position = (float(request.form.get("pos_y")), float(request.form.get("pos_x")))
        self.rotation = float(request.form.get("rotation"))
        self.zoom_factor = float(request.form.get("zoom_factor"))
        return self.home()
    
    def button_frame_plus_100(self):
        self.switch_frame(step_size=100)
        return self.home()

    def button_frame_minus_100(self):
        self.switch_frame(step_size=-100)
        return self.home()

    def button_frame_plus_10(self):
        self.switch_frame(step_size=10)
        return self.home()

    def button_frame_minus_10(self):
        self.switch_frame(step_size=-10)
        return self.home()
    
    def set_frame(self):
        self.frame = int(request.form.get("frame"))
        return self.home()

    def show(self):
        self.app.run(host=self.host_address, port=self.port, debug=True)
