from . import model
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
import flask_login
from . import db
from datetime import datetime

bp = Blueprint("main", __name__)

@bp.route('/')
def homepage():
        return render_template('index.html')# cambiar a index html 

@bp.route("/Catalog")
def catalog():
    animals = ( model.Animal.query.all() )
    return render_template("catalog.html", catalog=animals)

@bp.route("/Catalog", methods=["POST"] )
def catalog_filter():

    zone = request.form.get("Zone")

    if zone == "Savannah":
        Animal_zone = "Savannah"
    elif zone == "Aquarium":
        Animal_zone = "Aquarium"
    elif zone == "Aviary":
        Animal_zone = "Aviary"
    elif zone == "Reptilian":
        Animal_zone = "Reptilian"
    elif zone == "Farm":
        Animal_zone = "Farm"
    else:
        Animal_zone = None

    type = request.form.get("Type")

    if type == "Mammal":
        Animal_type = "Mammal"
    elif type == "Fish":
        Animal_type = "Fish"
    elif type == "Bird":
        Animal_type = "Bird"
    elif type == "Reptile":
        Animal_type = "Reptile"
    elif type == "Invertebrate":
        Animal_type = "Invertebrate"
    elif type == "Amphibiant":
        Animal_type = "Amphibiant"
    else:
        Animal_type = None


    if Animal_zone is None and Animal_type is None:
        animals = ( model.Animal.query.all() )

    elif Animal_zone is None and Animal_type is not None:
        animals = ( model.Animal.query.filter_by(type=Animal_type)  )

    elif Animal_zone is not None and Animal_type is None:
        animals = ( model.Animal.query.filter_by(zone=Animal_zone) )

    elif Animal_zone is not None and Animal_type is not None:
        animals = ( model.Animal.query.filter_by(zone=Animal_zone, type=Animal_type) )

    return render_template("catalog.html", catalog=animals)


@bp.route("/", methods=["POST"] )
def animal_browser_post():
    Animal_name = request.form.get("Name")

    animal = model.Animal.query.filter_by(name=Animal_name).first()
    if not animal:
        return redirect(url_for("main.homepage"))
        
    else:
        return redirect(url_for("main.animal", animal_id=animal.id))



@bp.route("/Animal/<int:animal_id>")
def animal(animal_id):
    animal = model.Animal.query.filter_by(id=animal_id).first()
    if not animal:
        abort(404, "Animal id {} not found".format(animal_id))
    
    events  = ( model.Activity.query.filter_by(zone=animal.zone).all() )

    return render_template("animal_template.html", animal=animal, events=events)

@bp.route("/Events")
def events():
    events = ( model.Activity.query.all() )
    return render_template("event_catalog.html", event_catalog = events)

@bp.route("/Events/<int:event_id>")
def event(event_id):
    current_time = datetime.now()
    event = model.Activity.query.filter_by(id=event_id).first()
    animals  = ( model.Animal.query.filter_by(zone=event.zone).all() )

    if not event:
        abort(404, "Event id {} not found".format(event_id))
    
    scheduled_events = ( model.Scheduled.query.filter_by(event_id=event_id).order_by(model.Scheduled.time_date.asc()).all())

    return render_template("event_template.html", event1=event, scheduled_events=scheduled_events, current_time=current_time, animals=animals)

@bp.route('/Map')
def map():
        return render_template('map.html')
  
@bp.route('/Manager')
@flask_login.login_required 
def manager():
        return render_template('manager_template.html')

@bp.route('/Customer')
@flask_login.login_required   
def customer():
    current_time = datetime.now()
    return render_template('customer_template.html', current_time = current_time)

@bp.route('/Reservation/<int:scheduled_id>')
@flask_login.login_required 
def reservation(scheduled_id):
    scheduled_event = model.Scheduled.query.filter_by(id=scheduled_id).first()
    return render_template('reservation_template.html', scheduled_event = scheduled_event)

@bp.route('/Reservation/<int:scheduled_id>', methods=["POST"])
@flask_login.login_required   
def reservation_post(scheduled_id):

    places = int(request.form.get("places"))
    user_id = request.form.get("user")

    # Encontrar scheduled y el user que es que quiere reservar
    scheduled = model.Scheduled.query.filter_by(id=scheduled_id).first()
    user = model.User.query.filter_by(id=user_id).first()
    plazas_actuales = scheduled.place

    # Chequear si los places que mete son los disponibles
    if scheduled.place >= places:

        new_reservation = model.Reservation(event_id=scheduled.id, user_id=user.id, date_time = datetime.now(), places=places)
        scheduled.place = plazas_actuales-places # Modificar las plazas 
        db.session.add(new_reservation)
        db.session.commit()
        return redirect(url_for("main.customer"))

    elif scheduled.place < places:
        flash("There are not enough places available")
        return redirect(url_for("main.reservation", scheduled_id=scheduled_id))

    return render_template('reservation_template.html') # Se puede quitar 


@bp.route('/Event Featured')
@flask_login.login_required  
def event_featured():
    events = ( model.Activity.query.all() )
    return render_template('event_featured.html', events = events)

@bp.route('/Event Featured/<int:event_id>')
@flask_login.login_required 
def change_event(event_id):
    events = ( model.Activity.query.all() )
    event = model.Activity.query.filter_by(id=event_id).first()

    if not event:
        abort(404, "Event id {} not found".format(event_id))
    
    if event.featured == False:
        event.featured = True
        db.session.commit()
    else:
        event.featured = False
        db.session.commit()
    
    return redirect(url_for("main.event_featured", events=events))

@bp.route('/EditReservations')
@flask_login.login_required   
def edit_reservations():
    current_time = datetime.now() 
    return render_template('edit_reservations_template.html', current_time=current_time)

@bp.route('/EditReservations/<int:reservation_id>')
@flask_login.login_required 
def delete_reservation(reservation_id):

    reservation = model.Reservation.query.filter_by(id=reservation_id).first()
    reservation.scheduled.place = reservation.scheduled.place + reservation.places
    db.session.delete(reservation) 
    db.session.commit()
    return redirect(url_for("main.edit_reservations")) 

@bp.route('/Event Featured/<int:event_id>', methods=["POST"])
@flask_login.login_required   
def add_scheduled(event_id):

    date = request.form.get("Date")
    time = request.form.get("Time")
    event = model.Activity.query.filter_by(id=event_id).first()
    places = request.form.get("Places")
    price = request.form.get("Price")

    datetime = str(date) + " " + str(time)

    # Check if the scheduled is already at the database
    scheduled_event = model.Scheduled.query.filter_by(event_id=event.id, time_date= datetime).first()
    if scheduled_event:
        flash("Sorry, that events is already scheduled at the date and time")
        return redirect(url_for("main.event_featured"))

    new_scheduled = model.Scheduled(event_id=event.id, time_date=datetime, price=price, place=places)
    db.session.add(new_scheduled)
    db.session.commit()
    flash("Succesfully added the scheduled activity")
    return redirect(url_for("main.event_featured"))
 
@bp.route("/AddAnimal")
@flask_login.login_required 
def add_animal():
    animals = ( model.Animal.query.all() )
    return render_template('add_animal.html', animals = animals)

@bp.route("/AddAnimal", methods=["POST"])
@flask_login.login_required 
def add_animal_post():
    Animal_name = request.form.get("Name")
    Animal_info = request.form.get("Information")
    Animal_zone = request.form.get("Zone")
    Animal_img = request.form.get("Image")
    Image = "imagenes/catalog/" + Animal_img

    type = request.form.get("Type")

    if type == "Mammal":
        Animal_type = "Mammal"
    elif type == "Fish":
        Animal_type = "Fish"
    elif type == "Bird":
        Animal_type = "Bird"
    elif type == "Reptile":
        Animal_type = "Reptile"
    elif type == "Invertebrate":
        Animal_type = "Invertebrate"
    elif type == "Amphibiant":
        Animal_type = "Amphibiant"

    animal = model.Animal.query.filter_by(name=Animal_name).first()
    # If the animal is already in the database 
    if animal:
        flash("Sorry, the animal you provided is already registered")
        return redirect(url_for("main.add_animal"))

    new_animal = model.Animal(name=Animal_name, info=Animal_info, zone=Animal_zone, type=Animal_type, img=Image)
    db.session.add(new_animal)
    db.session.commit()
    return redirect(url_for("main.add_animal"))


@bp.route("/AddActivity")
@flask_login.login_required 
def add_activity():
    activities = ( model.Activity.query.all() )
    return render_template('add_activity.html', activities = activities)

@bp.route("/AddActivity", methods=["POST"])
@flask_login.login_required 
def add_activity_post():
    Activity_title = request.form.get("Title")
    Activity_info = request.form.get("Information")
    Activity_zone = request.form.get("Zone")
    Activity_age = request.form.get("Age")
    Activity_featured = request.form.get("Featured")

    if Activity_featured == "YES":
        featured = True
    else:
        featured = False

    activity = model.Activity.query.filter_by(title=Activity_title).first()
    # If the activity is already in the database 
    if activity:
        flash("Sorry, the activity you provided is already registered")
        return redirect(url_for("main.add_activity"))

    new_activity = model.Activity(title=Activity_title, info=Activity_info, zone=Activity_zone, age=Activity_age, featured=featured)
    db.session.add(new_activity)
    db.session.commit()
    return redirect(url_for("main.add_activity"))