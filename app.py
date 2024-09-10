from flask import Flask, render_template, request, redirect
from flask_pymongo import PyMongo
import os
import math
import requests


# Initialize Flask app
app = Flask(__name__)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # Radius of the Earth in kilometers

    # Convert latitude and longitude from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    # Differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

# Function to fetch the coordinates using the IP address
def locationCoordinates():
    try:
        
        response = requests.get('https://ipinfo.io')
        data = response.json()
        loc = data['loc'].split(',')
        lat, long = float(loc[0]), float(loc[1])
        return lat ,long
    #lat, long
    except:
        #print("Internet Not available")
        return None

def check_in():
    try:
        latitude_check, longitude_check = locationCoordinates()
            # if latitude_check is None or longitude_check is None:
            #     return render_template('index.html', result="Unable to fetch coordinates via IP.")
        # else:
        #     latitude_check = float(request.form['latitude'])
        #     longitude_check = float(request.form['longitude'])

        # Validate latitude and longitude
        # if not (-90 <= latitude_check <= 90) or not (-180 <= longitude_check <= 180):
        #     return "Invalid latitude or longitude."

        # Define the city location and perimeter
        city_name = "Jeppiaar Institute of Technology"
        city_latitude = float(12.5322)
        city_longitude = float(79.5228)
        perimeter_meters = float(68.47)  # Perimeter in meters
        perimeter_km = float(perimeter_meters / 1000.0 ) # Convert to kilometers

        # Calculate the distance to the check-in point
        distance_to_point =float( haversine(city_latitude, city_longitude, latitude_check, longitude_check))
        valid_check_in = distance_to_point <= perimeter_km

        # Determine the result
        if valid_check_in:
            return "present"
        else:
            return "Absent"

        # Store result in a text file with username
    #     with open('check_in_results.txt', 'a') as file:
    #         file.write(f"Username: {username}, Latitude: {latitude_check}, Longitude: {longitude_check}, Status: {valid_status}\n")

    #     return render_template('index.html', result=result)

    except ValueError:
         return None
    #render_template('index.html', result="Please enter valid numerical values for latitude and longitude.")



# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/attendance_db"  # Replace with your MongoDB URI

# Initialize PyMongo
mongo = PyMongo(app)

# MongoDB Collection
attendance_collection = mongo.db.attendance

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to add student attendance data to MongoDB
@app.route('/add', methods=['POST'])
def add_student():
    if request.method == 'POST':
        # Retrieve form data
        register_no = request.form['register_no']
        name = request.form['name']
        dept = request.form['dept']
        present = check_in()
        # 'Present' if request.form.get('present') == 'on' else 'Absent'

        # Create a dictionary to hold the data
        student_data = {
            'register_no': register_no,
            'name': name,
            'dept': dept,
            'present': present
        }

        # Insert the data into MongoDB
        attendance_collection.insert_one(student_data)

    return redirect('/')  # Redirect back to the form page

# Start the Flask server
if __name__ == "__main__":
    app.run(debug=True)
