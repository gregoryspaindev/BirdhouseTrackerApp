import time
from datetime import datetime

from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user
from sqlalchemy import update

from . import db
from .models import Visit, Species, Birdhouse

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', first_name=current_user.first_name)


@main.route('/addvisit')
@login_required
def addVisit():
    birdhouse_list = Birdhouse.query.filter_by()
    species_list = Species.query.filter_by()
    return render_template('addvisit.html', birdhouse_list=birdhouse_list, species_list=species_list)


@main.route('/addvisit', methods=["POST"])
@login_required
def postAddVisit():
    visit_date = datetime.strptime(request.form.get('visit_date'), '%Y-%m-%d')
    birdhouse_id = request.form.get('birdhouse_id')
    user_id = int(current_user.get_id())

    species_id = request.form.get('species_id')
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
    cowbird_eggs_amount = request.form.get('cowbird_eggs')
    cowbird_live_young_amount = request.form.get('cowbird_live_young')
    cowbird_dead_young_amount = request.form.get('cowbird_dead_young')
    needs_repair = request.form.get('needs_repairs')
    if needs_repair is None:
        needs_repair = 0
    else:
        needs_repair = 1
    comments = request.form.get('comments')

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

    return redirect(url_for('main.profile'))


@main.route('/choose', methods=["POST"])
@login_required
def chooseVisit():
    birdhouse_list = Birdhouse.query.filter_by()
    birdhouse_id = request.form.get('birdhouse_id')
    visit_list = Visit.query.filter_by(birdhouse_id=birdhouse_id)
    return render_template('choose.html', birdhouse_list=birdhouse_list, visit_list=visit_list)


@main.route('/choose')
@login_required
def chooseBirdhouse():
    birdhouse_list = Birdhouse.query.filter_by()
    return render_template('choose.html', birdhouse_list=birdhouse_list)


@main.route('/view/<int:visit_id>')
@login_required
def viewVisit(visit_id):
    visit = Visit.query.filter_by(visit_id=visit_id).first()
    birdhouse = Birdhouse.query.filter_by(birdhouse_id=visit.birdhouse_id).first()
    birdhouse_nickname = birdhouse.nickname
    species = Species.query.filter_by(species_id=visit.species_id).first()
    species_name = species.species_name
    return render_template('view.html', visit=visit, birdhouse_nickname=birdhouse_nickname, species_name=species_name)


@main.route('/view/edit/<int:visit_id>', methods=['POST'])
@login_required
def editVisit(visit_id):
    visit = Visit.query.filter_by(visit_id=visit_id).first()
    birdhouse = Birdhouse.query.filter_by(birdhouse_id=visit.birdhouse_id).first()
    birdhouse_nickname = birdhouse.nickname
    species = Species.query.filter_by(species_id=visit.species_id).first()
    species_name = species.species_name
    birdhouse_list = Birdhouse.query.filter_by()
    species_list = Species.query.filter_by()
    return render_template('edit.html', visit=visit, birdhouse_nickname=birdhouse_nickname,
                           species_name=species_name, birdhouse_list=birdhouse_list,
                           species_list=species_list)


@main.route('/edit/<int:visit_id>', methods=["POST"])
@login_required
def postEditVisit(visit_id):
    visit_date = datetime.strptime(request.form.get('visit_date'), '%Y-%m-%d')
    birdhouse_id = request.form.get('birdhouse_id')
    user_id = int(current_user.get_id())

    species_id = request.form.get('species_id')
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
    cowbird_eggs_amount = request.form.get('cowbird_eggs')
    cowbird_live_young_amount = request.form.get('cowbird_live_young')
    cowbird_dead_young_amount = request.form.get('cowbird_dead_young')
    needs_repair = request.form.get('needs_repairs')
    if needs_repair is None:
        needs_repair = 0
    else:
        needs_repair = 1
    comments = request.form.get('comments')

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
    return redirect(url_for('main.viewVisit', visit_id=visit_id))


@main.route('/delete/<int:visit_id>', methods=["POST"])
@login_required
def deleteVisit(visit_id):
    visit = Visit.query.filter_by(visit_id=visit_id).first()
    db.session.delete(visit)
    db.session.commit()
    return redirect(url_for('main.profile'))
