import os
import json

from io import BytesIO
from PIL import Image
from flask import Flask, render_template, request, send_file, url_for

#from vinepilot.model.data import VinePilotSegmentationDataset #Circular import
from vinepilot.config import Project


class VineyardViewer():
    def __init__(self) -> None:
        #Paths
        self.templates: str = os.path.normpath(os.path.join(Project.base_dir, "./vinepilot/tools/vineyardviewer/templates")) 
        self.static: str = os.path.normpath(os.path.join(Project.base_dir, "./vinepilot/tools/vineyardviewer/static")) 
        self.trajectory_path = os.path.abspath(os.path.join(Project.vineyards_dir, "./vineyard_000/trajectory_000.json"))

        #Webapp
        self.port: int = Project.port
        self.host_address: str = Project.host_address
        self.app = Flask(__name__, template_folder = self.templates, static_folder = self.static)

        #Routes
        self.app.route("/")(self.home)
        self.app.route("/load_virtual")(self.load_virtual)
        self.app.route("/load_real")(self.load_real)
        self.app.route("/button_frame_plus_100", methods=['POST'])(self.button_frame_plus_100)
        self.app.route("/button_frame_minus_100", methods=['POST'])(self.button_frame_minus_100)
        self.app.route("/button_frame_plus_10", methods=['POST'])(self.button_frame_plus_10)
        self.app.route("/button_frame_minus_10", methods=['POST'])(self.button_frame_minus_10)
        self.app.route("/button_save", methods=['POST'])(self.button_save)
        self.app.route("/submit_parameters", methods=['POST'])(self.submit_parameters)
        self.app.route("/set_frame", methods=['POST'])(self.set_frame)

        #Parameters
        self.vineyard_number: int = 0
        self.position: list = None
        self.rotation: float = None
        self.zoom_factor: float = None
        self.frame: int = 0

        #Images
        self.virtual = None
        self.real = None

        #Database
        with open(self.trajectory_path, "r") as f: self.trajectory = json.load(f)
        self.dataset = VinePilotSegmentationDataset()

    #Tools
    def load_virtual(self):
        #Get image
        _, img_arr = self.dataset.get_item_by_frame(self.frame)
        img = Image.fromarray(img_arr)
        self.virtual = BytesIO()
        img.save(self.virtual, "PNG")
        self.virtual.seek(0)
        return send_file(self.virtual, mimetype="image/png", as_attachment=True, download_name="virtual.png")
    
    def load_real(self):
        img_arr, _ = self.dataset.get_item_by_frame(self.frame)
        img = Image.fromarray(img_arr)
        self.real = BytesIO()
        img.save(self.real, "PNG")
        self.real.seek(0)
        return send_file(self.real, mimetype="image/png", as_attachment=True, download_name="real.png")

    def switch_frame(self, step_size):
        self.frame += int(step_size)

    def load_parameters(self):
        self.zoom_factor = self.trajectory["zoom"]
        if str(self.frame) not in self.trajectory["waypoints"].keys():
            self.position = [0,0]
            self.rotation = 0
            self.trajectory["waypoints"].update({str(self.frame): {"position": [0,0], "rotation": 0}})
            self.trajectory["waypoints"] = dict(sorted(self.trajectory["waypoints"].items()))

        else:
            self.position = self.trajectory["waypoints"][str(self.frame)]["position"]
            self.rotation = self.trajectory["waypoints"][str(self.frame)]["rotation"]

        self.dataset.overwrite_trajectory(new_trajectory=self.trajectory)

    def save_parameters(self):
        self.trajectory["zoom"] = self.zoom_factor
        self.trajectory["waypoints"][str(self.frame)]["position"] = self.position
        self.trajectory["waypoints"][str(self.frame)]["rotation"] = self.rotation
        self.dataset.overwrite_trajectory(new_trajectory=self.trajectory)

    #Pages
    def home(self):
        self.load_parameters()
        return render_template("home.html",
                            vineyard_number = self.vineyard_number,
                            current_pos_y = self.position[0],
                            current_pos_x = self.position[1],
                            current_rotation = self.rotation,
                            current_zoom_factor = self.zoom_factor,
                            current_frame = self.frame,
                            virtual = url_for("load_virtual"),
                            real = url_for("load_real"))

    #Actions
    def submit_parameters(self):
        self.position = [float(request.form.get("pos_y")), float(request.form.get("pos_x"))]
        self.rotation = float(request.form.get("rotation"))
        self.zoom_factor = float(request.form.get("zoom_factor"))
        self.save_parameters()
        #self.app.logger.debug(str(self.trajectory))
        return self.home()
    
    def set_frame(self):
        self.frame = int(request.form.get("frame"))
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
    
    def button_save(self):
        test_target = os.path.abspath(os.path.join(Project.vineyards_dir, "./vineyard_000/new_trajectory_000.json"))
        with open(test_target, "w") as f: json.dump(self.trajectory, f, indent=2)
        self.app.logger.info("File saved!")
        return self.home()

    def show(self):
        self.app.run(host=self.host_address, port=self.port, debug=True)
