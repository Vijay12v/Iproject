from pymongo import MongoClient
import pandas as pd

# MongoDB connection
mongo_uri = "mongodb://localhost:27017/attendance_db"  # Replace with your MongoDB URI
client = MongoClient(mongo_uri)

# Access the database and collection
db = client['attendance_db']
collection = db['attendance']

# Query the collection
data = list(collection.find())

# Convert to DataFrame
df = pd.DataFrame(data)

# Optionally, remove the _id field if you don't want it in the Excel file
if '_id' in df.columns:
    df.drop('_id', axis=1, inplace=True)

# Save DataFrame to Excel
excel_file = 'attendance_data.xlsx'
df.to_excel(excel_file, index=False)

print(f"Data has been successfully exported to {excel_file}")
