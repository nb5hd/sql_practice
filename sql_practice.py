# Nikhil Bhaip
# sql_practice.py
import psycopg2

conn = psycopg2.connect(database="nikhil", user="postgres", password = "", host = "localhost", port = "5432")

print "Opened database successfully"

cur = conn.cursor()


#Check if cars table already exists
cur.execute("SELECT EXISTS(SELECT * FROM information_schema.tables where table_name=%s)",
 ('cars',))
cars_exists = cur.fetchone()[0]

# If cars_table does not exist, then create a table and populate from CSV
if(cars_exists != True):
    cur.execute("""CREATE TABLE cars(
      id serial NOT NULL,
      mpg FLOAT8,
      cylinders INTEGER,
      displacement INTEGER,
      horsepower INTEGER,
      weight INTEGER,
      acceleration FLOAT8,
      model_year INTEGER,
      name TEXT
      )""")


    cur.execute("""
      COPY cars(mpg,cylinders,displacement,horsepower,weight,acceleration,
        model_year, name) 
       FROM '/Users/nikhil/Documents/Riparian/sql_practice/auto_data.csv' 
       DELIMITER ',' CSV HEADER;
     """)
    print "cars table was successfully created and populated"
else:
    print "cars table has already been created and populated"


cur.execute("SELECT name, model_year FROM cars WHERE model_year >= 80")
rows = cur.fetchall()

print "The following cars were introduced after the year 1980: \n"

for row in rows:
     print "NAME = ", row[1]
     print "MODEL_YEAR = 19"+ str(row[2])
     print "\n"

car_specs = ["mpg", "horsepower", "weight", "acceleration"]

cur.execute("""SELECT AVG(mpg), AVG(horsepower), AVG(weight), AVG(acceleration)
 FROM cars WHERE model_year >= 80""")
rows = cur.fetchall()

for i in range(len(car_specs)):
    print ("The average " + car_specs[i] + " for cars introduced in the 1980's is "
       + "{0:.2f}".format(rows[0][i]))


conn.commit()
conn.close()
