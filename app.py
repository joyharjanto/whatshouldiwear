from flask import Flask, request, redirect, url_for, render_template
from flask_sqlalchemy import SQLAlchemy
from opencage.geocoder import OpenCageGeocode
from pprint import pprint



app = Flask(__name__)

opencage_key = '22798f5e7e1e475c94fe1efd3f9b865f'
openweather_key = '94a75533eb9b0d50f5599add4552265d&'

@app.route('/', methods=['POST','GET'])
def home():
    if request.method == 'POST':
        address = request.form['content']
        print(address)
        suggestion = CashmereOrCotton(address)[0]
        a_description = CashmereOrCotton(address)[1]
        try:
            return render_template("base.html", suggestion=suggestion, address=address, a_description=a_description)
        except:
            return "um bug with form"
        # return render_template("base.html")
        # print(address)
    else:
        return render_template("base.html")

def CashmereOrCotton(address):

    geocoder = OpenCageGeocode(opencage_key)

    results = geocoder.geocode(address)
    lat = results[0]['geometry']['lat']
    lang = results[0]['geometry']['lng']

    url = 'https://api.openweathermap.org/data/2.5/weather?lat='+str(lat)+'&lon='+str(lang)+'&appid='+openweather_key+'&units='+'metric'
    r = requests.get(url).json()

    a_temp = r['main']['temp']
    print(a_temp)
    a_description = r['weather'][0]['description']
    # print(r['main']['temp'])
    # print(r['weather'][0]['description'])

    if a_temp <= 18:
        wear = "cashmere"
    else:
        wear = "cotton"

    return wear, a_description

if __name__ == "__main__":
    app.run(debug=True)
