# Flask Birdhouse Tracker App
### Author: Gregory Spain
### Date May 11, 2023

This app is for Audubon Miami Valley and their program
to track birdhouses. It was created for WDD 3500 Python
for Web Development at Clark State College.

To use, create a virtual environment, and download the
following dependencies:

1. flask
2. flask_login
3. flask_sqlalchemy
4. db
5. werkzeug

Then you can set the App environment variable with the
following PowerShell command:

$env:FLASK_APP="bird_app"

In __init__.py there are 2 areas to fill in your own data:
the flask secret key and the database connection string.

Then run the app "flask run".

I have included a db_setup.sql script that can be run in
MySQL to create the entire db schema.

The Database schema is as follows:

## birdhouse
birdhouse_id int NOT NULL unique auto_increment PRIMARY KEY,
nickname varchar(100) NOT NULL unique,
repair_flag bool NOT NULL,
cowbird_flag bool NOT NULL

## species
species_id int NOT NULL unique auto_increment PRIMARY KEY,
species_name varchar(100) NOT NULL unique

## user
user_id	int	NOT NULL unique auto_increment PRIMARY KEY,
email varchar(100) NOT NULL unique,
password varchar(100) NOT NULL,
first_name varchar(100) NOT NULL,
last_name varchar(100) NOT NULL

## visit
visit_id int NOT NULL unique auto_increment PRIMARY KEY,
visit_date date NOT NULL,
birdhouse_id int NOT NULL,
user_id int NOT NULL,
species_id int NOT NULL,
species_eggs_amount int NOT NULL,
species_live_young_amount int NOT NULL,
species_dead_young_amount int NOT NULL,
cowbird_eggs_amount int NOT NULL,
cowbird_live_young_amount int NOT NULL,
cowbird_dead_young_amount int NOT NULL,
needs_repair bool default false,
comments varchar(5000) default 'none',
foreign key (birdhouse_id) references birdhouse(birdhouse_id),
foreign key (user_id) references user(user_id),
foreign key (species_id) references species(species_id)