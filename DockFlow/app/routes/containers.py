from flask import Blueprint, render_template
containers_bp = Blueprint("containers", __name__, url_prefix="/containers")
@containers_bp.get("/")
def index():
    return render_template("containers.html", page="Containers")
