import random
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Security Token Key
API_KEY = "TopSecretAPIKey"


# Cafe DB Model Mapping configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        """Serializes database record rows into standard key-value dictionary formats."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    """Renders the Premium Developer Console Interactivity Center."""
    return render_template("index.html")


# ==========================================
# --- HTTP GET - READ ENDPOINTS ----------
# ==========================================

@app.route("/api/v1/random", methods=["GET"])
def get_random_cafe():
    """Returns a random cafe item from database records."""
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    if not all_cafes:
        return jsonify(error={"NotFound": "No records present inside system database indexes."}), 404
    random_cafe = random.choice(all_cafes)
    return jsonify(cafe=random_cafe.to_dict()), 200


@app.route("/api/v1/all", methods=["GET"])
def get_all_cafes():
    """Returns all cafe records saved within database repositories."""
    result = db.session.execute(db.select(Cafe).order_by(Cafe.name))
    all_cafes = result.scalars().all()
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes]), 200


@app.route("/api/v1/search", methods=["GET"])
def search_cafe():
    """Filters data entries matching explicit location keywords query strings."""
    loc = request.args.get("loc")
    if not loc:
        return jsonify(error={"BadRequest": "Missing required location 'loc' query argument."}), 400
        
    result = db.session.execute(db.select(Cafe).where(Cafe.location.like(f"%{loc}%")))
    cafes = result.scalars().all()
    if cafes:
        return jsonify(cafes=[cafe.to_dict() for cafe in cafes]), 200
    return jsonify(error={"NotFound": f"No cafe matching location search metric target key '{loc}' discovered."}), 404


# ==========================================
# --- HTTP POST - CREATE ENDPOINTS --------
# ==========================================

@app.route("/api/v1/add", methods=["POST"])
def post_new_cafe():
    """Adds a new cafe entry record to data repositories."""
    try:
        # Pull values either from Form Data or Raw JSON inputs for advanced versatility
        data = request.form if request.form else request.get_json()
        
        new_cafe = Cafe(
            name=data.get("name"),
            map_url=data.get("map_url"),
            img_url=data.get("img_url"),
            location=data.get("location"),
            has_sockets=bool(int(data.get("sockets", 0))),
            has_toilet=bool(int(data.get("toilet", 0))),
            has_wifi=bool(int(data.get("wifi", 0))),
            can_take_calls=bool(int(data.get("calls", 0))),
            seats=data.get("seats"),
            coffee_price=data.get("coffee_price"),
        )
        db.session.add(new_cafe)
        db.session.commit()
        return jsonify(response={"success": "Successfully initialized the new cafe element resource asset."}), 201
    except Exception as e:
        return jsonify(error={"BadRequest": "Invalid or incomplete parameter payload mapping keys configuration."}), 400


# ==========================================
# --- HTTP PATCH - UPDATE ENDPOINTS -------
# ==========================================

@app.route("/api/v1/update-price/<int:cafe_id>", methods=["PATCH"])
def patch_cafe_price(cafe_id):
    """Updates target asset valuation metrics parameters data fields."""
    new_price = request.args.get("new_price")
    if not new_price:
        return jsonify(error={"BadRequest": "Missing required parameter 'new_price' inside request string arguments."}), 400
        
    cafe = db.session.get(Cafe, cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": f"Successfully patched cafe ID {cafe_id} coffee evaluation parameters."}), 200
    return jsonify(error={"NotFound": f"Resource mapping for cafe structural target ID index {cafe_id} not found."}), 404


# ==========================================
# --- HTTP DELETE - REMOVE ENDPOINTS ------
# ==========================================

@app.route("/api/v1/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):
    """Removes a target listing from the database system registries using authorization verification keys."""
    api_key = request.args.get("api-key")
    if api_key != API_KEY:
        return jsonify(error={"Forbidden": "Operation rejected. Secure authorization token authentication credentials missing or invalid."}), 403
        
    cafe = db.session.get(Cafe, cafe_id)
    if cafe:
        db.session.delete(cafe)
        db.session.commit()
        return jsonify(response={"success": f"Successfully removed cafe resource record node with database index identifier {cafe_id}."}), 200
    return jsonify(error={"NotFound": f"Asset element structure with reference identifier target index {cafe_id} not found."}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5004)