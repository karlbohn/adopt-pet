from flask import Flask, render_template, redirect, flash, url_for, jsonify
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_adoption_agency'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'ihaveasecret'
app.app_context().push()

connect_db(app)
db.create_all()

@app.route('/')
def list_pets():
    """Homepage showing list of all pets"""

    pets = Pet.query.all()
    
    return render_template('home.html', pets=pets)

@app.route('/add', methods=["GET", "POST"])
def show_add_form():
    """Shows form to add a new pet"""

    form = AddPetForm()
    if form.validate_on_submit():
        new_pet = Pet(name=form.name.data,
                      species=form.species.data,
                      photo_url=form.photo_url.data,
                      age=form.age.data,
                      notes=form.notes.data)
        db.session.add(new_pet)
        db.session.commit()
        flash(f'{new_pet.name} added')
        return redirect(url_for('list_pets'))
    else:
        return render_template("add_pet.html", form=form)

@app.route("/<int:pet_id>", methods=["GET","POST"])
def edit_pet(pet_id):
    """Edit pet"""

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        pet.notes = form.notes.data
        pet.available = form.available.data
        pet.photo_url = form.photo_url.data
        db.session.commit()
        flash(f"{pet.name} updated.")
        return redirect(url_for('list_pets'))

    else:
        return render_template("edit_pet.html", form=form, pet=pet)


@app.route("/api/pets/<int:pet_id>", methods=['GET'])
def api_get_pet(pet_id):
    """Return basic info about pet in JSON."""

    pet = Pet.query.get_or_404(pet_id)
    info = {"name": pet.name, "age": pet.age}

    return jsonify(info)