from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

# conn = psycopg2.connect(
#     host=os.getenv("DB_HOST"),
#     user=os.getenv("DB_USER"),
#     password=os.getenv("DB_PASSWORD"),
#     port = "5432"
# )

conn = psycopg2.connect(
    host='localhost',
    user='postgres',
    password='123',
    port = "5432"
)

cur = conn.cursor()

## 2.0 CREATE DB SCHEMA #######################################################
cur.execute("DROP SCHEMA public CASCADE;")
cur.execute("CREATE SCHEMA IF NOT EXISTS public;")
cur.execute("""
CREATE TABLE users (
    username varchar(30),
    first_name varchar(30),
    last_name varchar(30),
    dob date,
	email varchar(255) NOT NULL,
    
    PRIMARY KEY (username)
);
""")

cur.execute("""
CREATE TABLE muscles (
    muscle varchar(20),
    body_part varchar(20),

    PRIMARY KEY (muscle),	
	CHECK (muscle IN (		
		'biceps', 'triceps',
        'lats', 'lower back',
        'upper chest', 'mid chest', 'lower chest',
		'abs', 'obliques',
		'quads', 'hamstrings', 'glutes', 'calves',
        'front delts', 'side delts', 'rear delts', 'traps'
	)),
	CHECK (body_part IN ('arms', 'back', 'chest', 'core', 'legs', 'shoulders'))	
);
""")

cur.execute("""
CREATE TABLE exercises (
    exercise varchar(50),
    target_muscle varchar,

    FOREIGN KEY (target_muscle) REFERENCES muscles (muscle),
    PRIMARY KEY (exercise)
);
""")

cur.execute("""
CREATE TABLE records (
	id serial PRIMARY KEY,
    username varchar NOT NULL,
	date date NOT NULL,
    exercise varchar NOT NULL,
	reps  integer NOT NULL CHECK (reps >= 1 AND reps <= 100),
	sets integer NOT NULL CHECK (sets >= 1 AND sets <= 100),
	weight NUMERIC(4, 1) NOT NULL,

    FOREIGN KEY (username) REFERENCES users (username),
    FOREIGN KEY (exercise) REFERENCES exercises (exercise),
	CONSTRAINT unique_record UNIQUE (username, date, exercise, reps, sets, weight)
);
""")

## 3.0 INSERT DATA ############################################################
# Insert into MUSCLES
for e in ['biceps', 'triceps']:
    cur.execute("INSERT INTO muscles VALUES (%s, %s)",(e, 'arms'))

for e in ['lats', 'lower back']:
    cur.execute("INSERT INTO muscles VALUES (%s, %s)",(e, 'back'))

for e in ['upper chest', 'mid chest', 'lower chest']:
    cur.execute("INSERT INTO muscles VALUES (%s, %s)",(e, 'chest'))

for e in ['abs', 'obliques']:
    cur.execute("INSERT INTO muscles VALUES (%s, %s)",(e, 'core'))

for e in ['quads', 'hamstrings', 'glutes', 'calves']:
    cur.execute("INSERT INTO muscles VALUES (%s, %s)",(e, 'legs'))

for e in ['front delts', 'side delts', 'rear delts', 'traps']:
    cur.execute("INSERT INTO muscles VALUES (%s, %s)",(e, 'shoulders'))

# Insert into EXERCISES
exercises_data = [
    # Arms
    ("Bicep Curls (Dumbbell)", "biceps"),
    ("Hammer Curls (Dumbbell)", "biceps"),
    ("Tricep Dips", "triceps"),

    # Back
    ("Lat Pulldowns (Machine)", "lats"),
    ("Deadlifts (Barbell)", "lower back"),
    ("Bent Over Rows (Barbell)", "lats"),
    ("Hyperextensions", "lower back"),

    # Chest
    ("Bench Press (Barbell)", "mid chest"),
    ("Incline Press (Barbell)", "upper chest"),
    ("Decline Press (Barbell)", "lower chest"),
    ("Push-ups", "mid chest"),
    ("Chest Flyes", "mid chest"),

    # Core
    ("Crunches", "abs"),
    ("Russian Twists", "obliques"),
    ("Planks", "abs"),
    ("Bicycle Crunches", "abs"),

    # Legs
    ("Squats", "quads"),
    ("Lunges (Barbell)", "quads"),
    ("Leg Press", "quads"),
    ("Calf Raises (Dumbbell)", "calves"),

    # Shoulders
    ("Shoulder Press (Barbell)", "front delts"),
    ("Lateral Raises (Dumbbell)", "side delts"),
    ("Front Raises (Dumbbell)", "front delts"),
    ("Shrugs (Machine)", "traps")
]

for exercise, target_muscle in exercises_data:
    cur.execute("INSERT INTO exercises VALUES (%s, %s)", (exercise, target_muscle))

# Insert into USERS
users_data = [
    ("lorenpeve", "Lorenzo", "Peve", "1996-03-31", "lpeve01@gmail.com"),
    ("lexcooper", "Lex", "Cooper", "1999-11-16", "lexcooper@gmail.com")
]

for u in users_data:
    cur.execute("INSERT INTO users VALUES (%s, %s, %s, %s, %s)", u)


conn.commit()