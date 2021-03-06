# Setting Up Flask
from flask import Flask
from flask import render_template
from flask import jsonify
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
server = Flask(__name__)

import os
import sqlite3 as sql

# Importing Other Modules
import requests
import datetime

# Importing Custom Modules
from app import main

@server.route('/hello')
def hello():
    return 'Hello World!'

# Serving HTML Pages/Templates

@server.route('/')
def home():
    return render_template('index.html', name='Visitor')
    
@server.route('/name/<name>')
def name(name=None):
    return render_template('index.html', name=name)
    
@server.route('/sample')
def sample():
    return render_template('map.html')
    
@server.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# Responding to Requests with Data

@server.route('/reflect/<name>')
def reflect(name=None):
    r = {'name': name}
    return jsonify(r)
    
@server.route('/weather')
def weather():
    w = main.get_weather()
    return jsonify(w)
    
@server.route('/location_image/<search>')
def location_image(search):
    geo_url = "https://maps.googleapis.com/maps/api/geocode/json"
    geo_query = {
        "address": search
    }
    geo_res = requests.request("GET", geo_url, params=geo_query);
    geo_data = geo_res.json();
    loc = geo_data['results'][0]['geometry']['location'];
    url = "https://maps.googleapis.com/maps/api/streetview"
    querystring = {
        "size": "600x600",
        "location": str(loc['lat']) + "," + str(loc['lng']),
        "heading": "90",
        "pitch": "0"
    }
    response = requests.request("GET", url, params=querystring)
    return response.url;
    
#Pick a place to rate
@server.route('/new_rating')
def new_rating():
   con = sql.connect("locations.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from locations")
   
   rows = cur.fetchall(); 
   return render_template("new_rating.html",rows = rows)
#Rate form  
@server.route('/rate/<place_id>')
def rate_page(place_id):
   con = sql.connect("locations.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("select * from locations WHERE id=(?)",(place_id,))
   
   rows = cur.fetchall(); 
   return render_template('rate.html',location=place_id,rows=rows)
   
@server.route('/rate',methods = ['POST', 'GET'])
def rate():
   if request.method == 'POST':
      
      try:
         title = request.form['title']
         review = request.form['review']
         rating = request.form['rating']
         name = request.form['name']
         date = datetime.date.today()
         location = request.form['place']
         msg = " "
         with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO ratings VALUES (?,?,?,?,?,?)",(title,review,rating,name,date,location) )
            con.commit()
            msg = "success"
      except:
         con.rollback()
         msg = "error"
      
      finally:
         return render_template("result.html",msg=msg)
         con.close()
         
#Returns list of locations
@server.route('/locations')
def location():
   con = sql.connect("locations.db")
   con.row_factory = sql.Row

   cur = con.cursor()
   cur.execute("select * from locations")
   
   rows = cur.fetchall(); 
   return render_template("locations.html",rows = rows)
 
#Returns the ratings for a specific place         
@server.route('/ratings/<place_id>')
def ratings(place_id):
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("select * from ratings WHERE location=(?)",(place_id,))
   
   con2 = sql.connect("locations.db")
   con2.row_factory = sql.Row
   cur2 = con2.cursor()
   cur2.execute("select * from locations WHERE id=(?)",(place_id,))
   
   
   rows = cur.fetchall(); 
   rows2 = cur2.fetchall();
   return render_template("ratings.html",rows = rows,rows2 = rows2)
   

   
  
#To make our lives easier
  
@server.before_first_request
def create_ratings():
    con = sql.connect("database.db")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS ratings (title text, review text, rating int, name text, date datetime, location text);")
    cursor.execute("INSERT INTO ratings VALUES (?,?,?,?,?,?)",("Great Quiet Coffeehouse","The atmosphere was great! It's very close to campus, and the coffee is awesome.","5","CS Student",2017-11-18,"ChIJZWZ6QRMsDogRpCk7IQyoP8g") )
    cursor.execute("INSERT INTO ratings VALUES (?,?,?,?,?,?)",("Very historic building","Great example of Mies' work!","4","Arkie",2017-11-18,"ChIJz8uyCg0sDogRD7rGqlEJIXA") )   
    con.commit()
    
    con = sql.connect("locations.db")
    cursor = con.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS locations (name text, id text, type text);")
    cursor.execute("INSERT INTO locations VALUES (?,?,?)",("S. R. Crown Hall","ChIJz8uyCg0sDogRD7rGqlEJIXA","study") )
    cursor.execute("INSERT INTO locations VALUES (?,?,?)",("Lao Sze Chuan","ChIJvbgep2EsDogR6A601lrlnYg","restaurant") )
    cursor.execute("INSERT INTO locations VALUES (?,?,?)",("Buffalo Wings and Rings","ChIJqXBBmzksDogR8pDe_sK-74Q","restaurant") )
    cursor.execute("INSERT INTO locations VALUES (?,?,?)",("Chicago Home of Chicken and Waffles","ChIJ_0VX-vgrDogRnZLnFyFz2DE","restaurant") )
    cursor.execute("INSERT INTO locations VALUES (?,?,?)",("Reggie's Chicago","ChIJVUmkEX0sDogRzm1DQOACx-g","restaurant") )
    cursor.execute("INSERT INTO locations VALUES (?,?,?)",("Maria's Packaged Goods and Bar","ChIJNdcMrkksDogRS_COh3n2vNA","restaurant") )
    cursor.execute("INSERT INTO locations VALUES (?,?,?)",("nana","ChIJZTa9XjgsDogRhJhoNLqx6A0","restaurant") )
    cursor.execute("INSERT INTO locations VALUES (?,?,?)",("MingHin Cuisine","ChIJe19TdGEsDogRnqHzxT0P3PU","restaurant") )
    cursor.execute("INSERT INTO locations VALUES (?,?,?)",("Chi Cafe","ChIJWQcymWEsDogRKMRtP1XzEfU","restaurant") )
    cursor.execute("INSERT INTO locations VALUES (?,?,?)",("Margaret T. Burroughs Beach and Park","ChIJrTkqEI4rDogRfvrJkQYExR8","park") )
    cursor.execute("INSERT INTO locations VALUES (?,?,?)",("Palmisano Park","ChIJ59crbk8sDogRWuHEWkIGRpk","park") )
    cursor.execute("INSERT INTO locations VALUES (?,?,?)",("McGuane Park","ChIJabfBA0YsDogRaZz7dURkFhc","park") )
    cursor.execute("INSERT INTO locations VALUES (?,?,?)",("Burnham Park","ChIJ9YjrWtsrDogR9nXINKPJejM","park") )
    cursor.execute("INSERT INTO locations VALUES (?,?,?)",("Ellis Park","ChIJdyk-JPIrDogRw89XyCiAELA","park") )
    cursor.execute("INSERT INTO locations VALUES (?,?,?)",("Armour Square Park","ChIJmaLdhRQsDogRuLEiq-h3d6A","park") )
    cursor.execute("INSERT INTO locations VALUES (?,?,?)",("Awake with Pearl Coffee Cafe","ChIJCTu5dXAsDogRtPcKzEZHPfE","cafe") )
    cursor.execute("INSERT INTO locations VALUES (?,?,?)",("Sip and Savor Chicago","ChIJaVC9w_0rDogR5r4ABW6rbkI","cafe") )
    cursor.execute("INSERT INTO locations VALUES (?,?,?)",("Bridgeport Coffee House","ChIJQwv5skksDogR2Ix6vBgNPQs","cafe") )
    cursor.execute("INSERT INTO locations VALUES (?,?,?)",("Jackalope Coffee and Tea House","ChIJOVdXgEcsDogR-M5ZgDeSswk","cafe") )
    cursor.execute("INSERT INTO locations VALUES (?,?,?)",("Dunkin Donuts","ChIJe0StBUcsDogRiv2PwuXBaVg","cafe") )
    cursor.execute("INSERT INTO locations VALUES (?,?,?)",("Mariano's Bronzeville","ChIJr16JMPgrDogRJn8yKYSvTjk","cafe") )
    con.commit()

    