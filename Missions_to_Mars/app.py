from flask import Flask, render_template, redirect
import os
import pymongo
import scrape_mars

# Initiate Flask App
app = Flask(__name__)

# Initiate MongoDB
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
marsDB = client.mars_app
mars = marsDB.mars

RESOURCES = os.path.join('static', 'Resources')
app.config['UPLOAD_FOLDER'] = RESOURCES
logo = os.path.join(app.config['UPLOAD_FOLDER'], 'assets', 'MarsLogo.png')

# Routes
@app.route('/')
def index():
    marsData = mars.find_one()
    return render_template('index.html', logo = logo, marsData = marsData)

@app.route('/scrape')
def scrape():
    data = scrape_mars.scrape()
    mars.replace_one(
        {},
        data,
        upsert = True
    )
    return redirect('/', code = 302)

if __name__ == '__main__':
   app.run()