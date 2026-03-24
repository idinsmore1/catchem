CREAT TABLE pokemon (
    id INTEGER PRIMARY KEY,
    name TEXT,
    display_name TEXT,
    height INTEGER,
    weight INTEGER,
    base_experience INTEGER,
    is_default BOOLEAN,
    order INTEGER,
    species_id INTEGER,
    stats_id INTEGER,
    FOREIGN KEY (species_id) REFERENCES species(id),
    FOREIGN KEY (stats_id) REFERENCES stats(id)
)

CREATE TABLE stats (
    poke_id INTEGER PRIMARY KEY,
    hp INTEGER,
    attack INTEGER,
    defense INTEGER,
    special_attack INTEGER,
    special_defense INTEGER,
    speed INTEGER,
    total INTEGER,
    effort_stat TEXT,
    effort_value INTEGER
);

CREATE TABLE moves (
    move_id INTEGER PRIMARY KEY,
    name TEXT,
    type TEXT,
    power INTEGER,
    pp INTEGER,
    accuracy INTEGER,
    damage_class TEXT
)

CREATE TABLE learnable_moves (
    id INTEGER PRIMARY KEY,
    version_group TEXT,
    poke_level INTEGER,
    method TEXT,
    FOREIGN KEY (move_id) REFERENCES moves(move_id)
)