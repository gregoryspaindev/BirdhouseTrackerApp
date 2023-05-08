from datetime import datetime

from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, current_user

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
