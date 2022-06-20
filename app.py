"""Flask app for Cupcakes"""
from flask import Flask, jsonify, request
#url_for, render_template, redirect, flash

#from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///cupcakes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

# Having the Debug Toolbar show redirects explicitly is often useful;
# however, if you want to turn it off, you can uncomment this line:
#
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

#toolbar = DebugToolbarExtension(app)

@app.get('/api/cupcakes')
def list_all_cupcakes():
    """return JSON {'cupcakes': [{id, flavor, size, rating, image_url}, ...]}"""

    cupcakes = Cupcake.query.all()
    serialized = [c.serialize() for c in cupcakes]

    return jsonify(cupcakes=serialized)

@app.get('/api/cupcakes/<int:cupcake_id>')
def list_single_cupcake(cupcake_id):
    """return JSON {'cupcake': [{id, flavor, size, rating, image_url}"""

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)

@app.post('/api/cupcakes')
def create_new_cupcake():
    """return JSON for new cupcake {'cupcake': [{id, flavor, size, rating, image_url}"""

    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image_url = request.json['image_url'] or None

    new_cupcake = Cupcake(
                        flavor=flavor,
                        size=size,
                        rating=rating,
                        image_url=image_url
                        )
    db.session.add(new_cupcake)
    db.session.commit()

    serialized = new_cupcake.serialize()

    return (jsonify(cupcake=serialized), 201)

@app.patch('/api/cupcakes/<int:cupcake_id>')
def update_capcake(cupcake_id):
    """ this updates cupcake and returns JSON for one
        cupcake with the updated info
        example: {'cupcake': [{id, flavor, size, rating, image_url} """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    if request.json.get('flavor'):
        cupcake.flavor = request.json['flavor']
    if request.json.get('size'):
        cupcake.size = request.json['size']
    if request.json.get('rating'):
        cupcake.rating = request.json['rating']
    if request.json.get('image_url'):
        cupcake.image_url = request.json['image_url']

    #cupcake.flavor = request.json.get('flavor', cupcake.flavor)

    db.session.commit()

    serialized = cupcake.serialize()

    return jsonify(cupcake=serialized)

@app.delete('/api/cupcakes/<int:cupcake_id>')
def delete_cupcake(cupcake_id):
    """ deletes a cupcake form the data base returns
    JSON with the id of the deleted cupcake
    example : {deleted: [cupcake-id]}  """

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    #db.session.query(Cupcake).filter(Cupcake.id==cupcake_id).delete()

    db.session.commit()

    return jsonify({"deleted": cupcake_id})


    ## for key in request.json
        ## cupcake[key] = request.json[key]