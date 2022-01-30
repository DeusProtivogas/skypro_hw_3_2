from flask import Flask, jsonify

from database import *

app = Flask(__name__)

#  Для всех вьюшек - вводим id, получаем объект из таблицы
@app.route("/animal/<int:id>")
def animal_by_id(id):
    return jsonify(get_animal(id))

@app.route("/outcome_type/<int:id>")
def outcome_type_by_id(id):
    return jsonify(get_outcome_type(id))

@app.route("/outcome_subtype/<int:id>")
def outcome_subtype_by_id(id):
    return jsonify(get_outcome_subtype(id))

@app.route("/outcome/<int:id>")
def outcome_by_id(id):
    return jsonify(get_outcome(id))

@app.route("/colors/<int:id>")
def colors_by_id(id):
    return jsonify(get_colors(id))

@app.route("/animal_type/<int:id>")
def animal_type_by_id(id):
    return jsonify(get_animal_type(id))

@app.route("/breed/<int:id>")
def breed_by_id(id):
    return jsonify(get_breed(id))

restart_database()
app.run()


