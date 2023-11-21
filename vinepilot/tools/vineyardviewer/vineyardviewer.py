import os
from flask import Flask, render_template
from vinepilot.config import Project


class VineyardViewer():
    def __init__(self) -> None:
        #Webapp
        self.port: int = Project.port
        self.host_address: str = Project.host_address
        self.templates: str = os.path.normpath(os.path.join(Project.base_dir, "./vinepilot/tools/vineyardviewer/templates")) 
        self.app = Flask(__name__, template_folder = self.templates)

        #Routes
        self.app.route("/")(self.home)
        self.app.route("/button_plus100", methods=['POST'])(self.button_plus100)

        #Parameters
        self.vineyard_number: int = 0

    #Pages
    def home(self):
        return render_template("home.html",
                            vineyard_number = self.vineyard_number)

    #Actions
    def button_plus100(self):
        self.vineyard_number += 100
        return self.home()

    def show(self):
        self.app.run(host=self.host_address, port=self.port, debug=True)
