import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from database import Base
from models import Item

# Create an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


class TestAPI(unittest.TestCase):
    def setUp(self):
        # Create the database and tables
        Base.metadata.create_all(bind=engine)
        self.client = TestClient(app)
        
        # Override the SessionLocal in main.py
        import main
        main.db = TestingSessionLocal()

    def tearDown(self):
        # Drop the database after the test
        Base.metadata.drop_all(bind=engine)

    def test_hello_world(self):
        response = self.client.get("/hello-world")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello World user!"})

    def test_hello_world_with_name(self):
        response = self.client.get("/hello-world?name=Test")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello World Test!"})

    def test_create_and_get_item(self):
        # Create an item
        test_item = {
            "id": 1,
            "name": "Test Item",
            "description": "Test Description",
            "price": 100,
            "on_offer": False
        }
        response = self.client.post("/item", json=test_item)
        self.assertEqual(response.status_code, 201)
        
        # Get the item
        response = self.client.get("/item/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Test Item")
        
    def test_get_all_items(self):
        # Create items
        test_items = [
            {
                "id": 1,
                "name": "Item 1",
                "description": "Description 1",
                "price": 100,
                "on_offer": False
            },
            {
                "id": 2,
                "name": "Item 2",
                "description": "Description 2",
                "price": 200,
                "on_offer": True
            }
        ]
        
        for item in test_items:
            self.client.post("/item", json=item)
        
        # Get all items
        response = self.client.get("/items")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)
    
    def test_update_item(self):
        # Create an item
        test_item = {
            "id": 1,
            "name": "Original Item",
            "description": "Original Description",
            "price": 100,
            "on_offer": False
        }
        self.client.post("/item", json=test_item)
        
        # Update the item
        updated_item = {
            "id": 1,
            "name": "Updated Item",
            "description": "Updated Description",
            "price": 200,
            "on_offer": True
        }
        response = self.client.put("/item/1", json=updated_item)
        self.assertEqual(response.status_code, 200)
        
        # Verify the update
        response = self.client.get("/item/1")
        self.assertEqual(response.json()["name"], "Updated Item")
        self.assertEqual(response.json()["price"], 200)
    
    def test_delete_item(self):
        # Create an item
        test_item = {
            "id": 1,
            "name": "Item to Delete",
            "description": "This will be deleted",
            "price": 100,
            "on_offer": False
        }
        self.client.post("/item", json=test_item)
        
        # Delete the item
        response = self.client.delete("/item/1")
        self.assertEqual(response.status_code, 200)
        
        # Verify the item is deleted
        response = self.client.get("/item/1")
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()