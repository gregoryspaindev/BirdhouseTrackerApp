create schema birdapp;

use birdapp;

CREATE TABLE visit
(
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
);


CREATE TABLE species
(
	species_id int NOT NULL unique auto_increment PRIMARY KEY,
    species_name varchar(100) NOT NULL unique
);


CREATE TABLE birdhouse
(
	birdhouse_id int NOT NULL unique auto_increment PRIMARY KEY,
    nickname varchar(100) NOT NULL unique,
    repair_flag bool NOT NULL,
    cowbird_flag bool NOT NULL
);


CREATE TABLE user
(
	user_id	int	NOT NULL unique auto_increment,
	email varchar(100) NOT NULL unique,
	password varchar(100) NOT NULL,
	first_name varchar(100) NOT NULL,
	last_name varchar(100) NOT NULL,
	PRIMARY KEY (user_id)
);

insert into birdhouse values (birdhouse_id, "Test House", false, false);

insert into species VALUES (species_id, "Bluebird");

commit;