# 1. Import Flask
from flask import Flask, jsonify, render_template, redirect
import pymongo
import scrape_mars

# 2. Create an app
app = Flask(__name__)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db

# 3. Define static routes

@app.route("/")
def index():
    finding = db.collection.find_one()
    return render_template('index.html', scrapedict=finding)

@app.route("/scrape")
def scrape():    
    data = scrape_mars.scrape()
    db.collection.update({}, data, upsert=True)
    return redirect("http://localhost:5000/", code=302)

@app.route("/contact")
def contact():
    email = "weiming.sun@outlook.com"
    return ("Questions? Comments? Complaints? Shoot an email to "+ email +".")

# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)