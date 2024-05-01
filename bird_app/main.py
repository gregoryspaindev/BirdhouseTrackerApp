import time
from datetime import datetime

from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from sqlalchemy import update, TIMESTAMP

from . import db
from .models import Visit, Species, Birdhouse

main = Blueprint('main', __name__)
my_first_name = 'Gregory'


# route for the homepage for non-logged in users
@main.route('/')
def index():
    return render_template('index.html')


# route for the user home page.
@main.route('/user')
# @login_required
def user():
    return render_template('user.html', first_name=my_first_name)


# route to add a visit.
@main.route('/addvisit')
# @login_required
def add_visit():
    # start by getting the lists of birdhouses and species for dropdowns.
    birdhouse_list = Birdhouse.query.filter_by()
    species_list = Species.query.filter_by()
    return render_template('addvisit.html', birdhouse_list=birdhouse_list, species_list=species_list)


# route for submitting added visit
@main.route('/addvisit', methods=["POST"])
# @login_required
def post_add_visit():
    # get all the form data
    visit_date = datetime.strptime(request.form.get('visit_date'), '%Y-%m-%d')
    birdhouse_id = request.form.get('birdhouse_id')
    user_id = int(current_user.get_id())

    species_id = request.form.get('species_id')

    # if the user did not select a species, but instead typed one in, add that to the species table.
    # Once added, get the new species_id to save in visit.
    if species_id == "0":
        new_species_name = request.form.get('new_species')
        new_species = Species(species_name=new_species_name)
        db.session.add(new_species)
        db.session.commit()
        saved_new_species = Species.query.filter_by(species_name=new_species_name).first()
        species_id = saved_new_species.species_id

    species_eggs_amount = request.form.get('species_eggs')
    species_live_young_amount = request.form.get('species_live_young')
    species_dead_young_amount = request.form.get('species_dead_young')
    cowbird_eggs_amount = int(request.form.get('cowbird_eggs'))
    cowbird_live_young_amount = int(request.form.get('cowbird_live_young'))
    cowbird_dead_young_amount = int(request.form.get('cowbird_dead_young'))
    needs_repair = request.form.get('needs_repairs')
    comments = request.form.get('comments')

    # if there are any cowbird eggs or live or dead young, we will flag that in the birdhouse table.
    cowbird_flag = 0
    if cowbird_eggs_amount > 0 or cowbird_live_young_amount > 0 or cowbird_dead_young_amount > 0:
        cowbird_flag = 1

    # use this to flag the birdhouse if it needs repairs
    if needs_repair is None:
        needs_repair = 0
    else:
        needs_repair = 1

    # update the flag states in the birdhouse table
    birdhouse = Birdhouse.query.filter_by(birdhouse_id=birdhouse_id).first()
    birdhouse.repair_flag = needs_repair
    birdhouse.cowbird_flag = cowbird_flag
    db.session.commit()

    # create a new Visit object and save it to the visit table.
    new_visit = Visit(visit_date=visit_date,
                      birdhouse_id=birdhouse_id,
                      user_id=user_id,
                      species_id=species_id,
                      species_eggs_amount=species_eggs_amount,
                      species_live_young_amount=species_live_young_amount,
                      species_dead_young_amount=species_dead_young_amount,
                      cowbird_eggs_amount=cowbird_eggs_amount,
                      cowbird_live_young_amount=cowbird_live_young_amount,
                      cowbird_dead_young_amount=cowbird_dead_young_amount,
                      needs_repair=needs_repair,
                      comments=comments)
    db.session.add(new_visit)
    db.session.commit()

    # this one I'd like more time with. I want to display the saved visit so the user can verify, but there is a
    # potential bug if a user enters multiple visit to the same house on the same day.
    new_visit_test = Visit.query.filter_by(visit_date=visit_date,
                                           birdhouse_id=birdhouse_id,
                                           user_id=user_id).first()

    # send the user to the page for viewing a visit and load the new data they entered.
    return redirect(url_for('main.view_visit', visit_id=new_visit_test.visit_id))


# route to handle the chosen birdhouse. Display the list of visits to view, edit or delete visits.
@main.route('/choose', methods=["POST"])
# @login_required
def choose_visit():
    # load the list of birdhouses to choose from.
    birdhouse_list = Birdhouse.query.filter_by()
    birdhouse_id = request.form.get('birdhouse_id')
    visit_list = Visit.query.filter_by(birdhouse_id=birdhouse_id).order_by(Visit.visit_date.desc())
    return render_template('choose.html', birdhouse_list=birdhouse_list, visit_list=visit_list)


# route for a user to choose a birdhouse to view associated visits.
@main.route('/choose')
# @login_required
def choose_birdhouse():
    # load birdhouse list and display page
    birdhouse_list = Birdhouse.query.filter_by()
    return render_template('choose.html', birdhouse_list=birdhouse_list)


# route to display a previously added visit. can edit from there. The visit_id is passed in the url.
@main.route('/view/<int:visit_id>')
# @login_required
def view_visit(visit_id):
    # get the visit data, birdhouse nickname and species name and pass them to the view
    visit = Visit.query.filter_by(visit_id=visit_id).first()
    birdhouse = Birdhouse.query.filter_by(birdhouse_id=visit.birdhouse_id).first()
    birdhouse_nickname = birdhouse.nickname
    species = Species.query.filter_by(species_id=visit.species_id).first()
    species_name = species.species_name
    return render_template('view.html', visit=visit, birdhouse_nickname=birdhouse_nickname, species_name=species_name)


# route to handle loading existing data and form data for editing
@main.route('/view/edit/<int:visit_id>', methods=['POST'])
# @login_required
def edit_visit(visit_id):
    # get the visit data, birdhouse nickname and species name and pass them to the view
    visit = Visit.query.filter_by(visit_id=visit_id).first()
    birdhouse = Birdhouse.query.filter_by(birdhouse_id=visit.birdhouse_id).first()
    birdhouse_nickname = birdhouse.nickname
    species = Species.query.filter_by(species_id=visit.species_id).first()
    species_name = species.species_name

    # get the list of birdhouses and species and pass those to the view
    birdhouse_list = Birdhouse.query.filter_by()
    species_list = Species.query.filter_by()
    return render_template('edit.html', visit=visit, birdhouse_nickname=birdhouse_nickname,
                           species_name=species_name, birdhouse_list=birdhouse_list,
                           species_list=species_list)


# route to handle submitting an edit
@main.route('/edit/<int:visit_id>', methods=["POST"])
# @login_required
def post_edit_visit(visit_id):
    # get all the form data
    visit_date = datetime.strptime(request.form.get('visit_date'), '%Y-%m-%d')
    birdhouse_id = request.form.get('birdhouse_id')
    user_id = int(current_user.get_id())

    species_id = request.form.get('species_id')

    # if the user did not select a species, but instead typed one in, add that to the species table.
    # Once added, get the new species_id to save in visit.
    if species_id == "0":
        new_species_name = request.form.get('new_species')
        new_species = Species(species_name=new_species_name)
        db.session.add(new_species)
        db.session.commit()
        saved_new_species = Species.query.filter_by(species_name=new_species_name).first()
        species_id = saved_new_species.species_id

    species_eggs_amount = request.form.get('species_eggs')
    species_live_young_amount = request.form.get('species_live_young')
    species_dead_young_amount = request.form.get('species_dead_young')
    cowbird_eggs_amount = int(request.form.get('cowbird_eggs'))
    cowbird_live_young_amount = int(request.form.get('cowbird_live_young'))
    cowbird_dead_young_amount = int(request.form.get('cowbird_dead_young'))
    needs_repair = request.form.get('needs_repairs')
    comments = request.form.get('comments')

    # if there are any cowbird eggs or live or dead young, we will flag that in the birdhouse table.
    cowbird_flag = 0
    if cowbird_eggs_amount > 0 or cowbird_live_young_amount > 0 or cowbird_dead_young_amount > 0:
        cowbird_flag = 1

    # use this to flag the birdhouse if it needs repairs
    if needs_repair is None:
        needs_repair = 0
    else:
        needs_repair = 1

    # update the flag states in the birdhouse table
    birdhouse = Birdhouse.query.filter_by(birdhouse_id=birdhouse_id).first()
    birdhouse.repair_flag = needs_repair
    birdhouse.cowbird_flag = cowbird_flag
    db.session.commit()

    # update existing visit data
    existing_visit = Visit.query.filter_by(visit_id=visit_id).first()
    existing_visit.visit_date = visit_date
    existing_visit.birdhouse_id = birdhouse_id
    existing_visit.user_id = user_id
    existing_visit.species_id = species_id
    existing_visit.species_eggs_amount = species_eggs_amount
    existing_visit.species_live_young_amount = species_live_young_amount
    existing_visit.species_dead_young_amount = species_dead_young_amount
    existing_visit.cowbird_eggs_amount = cowbird_eggs_amount
    existing_visit.cowbird_live_young_amount = cowbird_live_young_amount
    existing_visit.cowbird_dead_young_amount = cowbird_dead_young_amount
    existing_visit.needs_repair = needs_repair
    existing_visit.comments = comments

    db.session.commit()

    # redirect to the view visit page so user can verify their information
    return redirect(url_for('main.view_visit', visit_id=visit_id))


# route to handle a 'delete' click
@main.route('/delete/<int:visit_id>', methods=["POST"])
# @login_required
def delete_visit(visit_id):
    # get the visit, delete it, and redirect to the user page
    visit = Visit.query.filter_by(visit_id=visit_id).first()
    db.session.delete(visit)
    db.session.commit()
    return redirect(url_for('main.user'))


# @main.route('/statistics')
# @login_required
# def view_statistics():
#     birdhouse_list = Birdhouse.query.filter_by()
#     return render_template('choose.html', birdhouse_list=birdhouse_list)
