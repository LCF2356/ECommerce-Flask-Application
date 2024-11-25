from flask import Flask, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
import os


app = Flask(__name__)
load_dotenv() 



# MongoDB connection
mongo_username = os.getenv('MONGODB_USERNAME')
mongo_password = os.getenv('MONGODB_PASSWORD')
mongo_uri = os.getenv('MONGODB_URI')
database_name = "shopdb"

try:
    # Connect to the MongoDB server
    client = MongoClient(mongo_uri)
    print("Connected to MongoDB!")

    # Access the database
    db = client[database_name]

    # List all collections in the database
    collections = db.list_collection_names()
    print(f"Collections in {database_name}: {collections}")

except Exception as e:
    print("Error:", e)

# # Connect to MongoDB Atlas
# client = MongoClient(mongo_uri)
# db = client.shopdb
products_collection = db['products']

print("Databases:", client.list_database_names())  # List all databases
print("Collections in shopdb:", db.list_collection_names())  # List collections in the database


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


# Products page route
@app.route('/products')
def products():
    print("hi")
    # Retrieve products from MongoDB
    products = list(products_collection.find())
    print("Products fetched from MongoDB:", products)
    return render_template('products.html', products=products)

# Run the app
if __name__ == '__main__':
    app.run(debug=True) 
