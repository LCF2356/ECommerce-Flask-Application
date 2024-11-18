from flask import Flask
import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # Ensure the .env file is loaded


print(f"MONGO_URI in test: {os.getenv('MONGODB_URI')}")

# (TestRoute) : Tests that the /home route returns a 405 status code for an invalid request method is used in this case a POST request.
class TestRoute(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)

        @app.route('/', methods=['GET'])
        def home():
            return "Home page"

        self.client = app.test_client()

    def test_invalid_method(self):
        # Sending a POST request to the GET-only route '/home'
        response = self.client.post('/')
        
        # Check that the response status code is 405 (Method Not Allowed)
        self.assertEqual(response.status_code, 405)


# ------------------------------------------------------------------------------------------------------------------------------

# (TestDatabaseRead): Tests if the MongoDB connection is working by using a ping.
class TestDatabaseRead(unittest.TestCase):
    def setUp(self):
        # Initialize Flask app for the test client
        self.app = Flask(__name__)  # Assuming the Flask app is here
        self.app.config['MONGODB_URI'] = os.getenv('MONGODB_URI') 
        self.app.testing = True  # Enable testing mode
        self.client = MongoClient(self.app.config['MONGODB_URI'])  # MongoDB client setup

    def tearDown(self):
        # Close the MongoDB client after the test to release resources
        self.client.close()

    def test_mongodb_connection(self):
        
        # Test if MongoDB is accessible by performing a 'ping' operation.
        # This test ensures that the app can connect to the MongoDB server.
    
        try:
            # Attempt to ping the MongoDB server
            result = self.client.admin.command('ping')
            self.assertTrue(result, "Failed to connect to MongoDB.")  # Assert the connection is successful
        except Exception as e:
            self.fail(f"MongoDB connection failed: {str(e)}")

# ------------------------------------------------------------------------------------------------------------------------------

# (TestDatabaseWrite):  This test will insert a new product document into the MongoDB database and 
# then verify if the document was successfully inserted.
class TestDatabaseWrite(unittest.TestCase):
    def setUp(self):
        
        # Setup the Flask app and MongoDB client for each test.
        # Connect to MongoDB directly and access the 'shopdb' database and 'products' collection.
    
        self.app = Flask(__name__)
        self.app.config['MONGODB_URI'] = os.getenv('MONGODB_URI')  
        self.app.testing = True
        # Initialize MongoDB client
        self.client = MongoClient(self.app.config['MONGODB_URI'])
        self.db = self.client.shopdb
        self.products_collection = self.db.products

    def tearDown(self):
        
        # Close the MongoDB client after the test to release resources.
    
        self.client.close()

    def test_insert_product(self):
        
        # Test the insertion of a new product into the MongoDB collection.
        # After inserting, check if the product exists in the database.
    
        # New product data
        new_product = {
            'name': 'Test Product',
            'tag': 'Electronics',
            'price': 99.99,
            'image_path': 'images/test_product.jpg'
        }

        # Inserting the product into the database
        result = self.products_collection.insert_one(new_product)

        # Checking if the product was inserted by querying the database
        inserted_product = self.products_collection.find_one({'_id': result.inserted_id})

        # Assert that the inserted product's details match the expected values
        self.assertIsNotNone(inserted_product, "Product was not inserted.")
        self.assertEqual(inserted_product['name'], new_product['name'])
        self.assertEqual(inserted_product['tag'], new_product['tag'])
        self.assertEqual(inserted_product['price'], new_product['price'])
        self.assertEqual(inserted_product['image_path'], new_product['image_path'])

        # # Clean up by removing the test product after the test
        # deletion_result = self.products_collection.delete_one({'_id': result.inserted_id})

        # # Assert that the deletion was successful
        # self.assertEqual(deletion_result.deleted_count, 1, "Failed to delete the test product.")


if __name__ == '__main__':
    unittest.main()
