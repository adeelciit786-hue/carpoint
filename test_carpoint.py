"""
Tests for the CarPoint system
"""
import unittest
import os
import json
from carpoint import Car, CarPoint


class TestCar(unittest.TestCase):
    """Test the Car class"""
    
    def test_car_creation(self):
        """Test creating a car"""
        car = Car("CAR001", "Toyota", "Camry", 2022, 25000.00)
        self.assertEqual(car.car_id, "CAR001")
        self.assertEqual(car.make, "Toyota")
        self.assertEqual(car.model, "Camry")
        self.assertEqual(car.year, 2022)
        self.assertEqual(car.price, 25000.00)
        self.assertEqual(car.status, "available")
    
    def test_car_to_dict(self):
        """Test car serialization"""
        car = Car("CAR001", "Toyota", "Camry", 2022, 25000.00)
        data = car.to_dict()
        self.assertEqual(data["car_id"], "CAR001")
        self.assertEqual(data["make"], "Toyota")
        self.assertEqual(data["status"], "available")
    
    def test_car_from_dict(self):
        """Test car deserialization"""
        data = {
            "car_id": "CAR001",
            "make": "Toyota",
            "model": "Camry",
            "year": 2022,
            "price": 25000.00,
            "status": "available"
        }
        car = Car.from_dict(data)
        self.assertEqual(car.car_id, "CAR001")
        self.assertEqual(car.make, "Toyota")


class TestCarPoint(unittest.TestCase):
    """Test the CarPoint inventory system"""
    
    def setUp(self):
        """Set up test environment"""
        self.test_file = "test_carpoint.json"
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        self.carpoint = CarPoint(self.test_file)
    
    def tearDown(self):
        """Clean up test environment"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_add_car(self):
        """Test adding a car to inventory"""
        car = Car("CAR001", "Toyota", "Camry", 2022, 25000.00)
        result = self.carpoint.add_car(car)
        self.assertTrue(result)
        self.assertEqual(len(self.carpoint.cars), 1)
        self.assertIn("CAR001", self.carpoint.cars)
    
    def test_add_duplicate_car(self):
        """Test adding a duplicate car ID"""
        car1 = Car("CAR001", "Toyota", "Camry", 2022, 25000.00)
        car2 = Car("CAR001", "Honda", "Civic", 2023, 28000.00)
        self.carpoint.add_car(car1)
        result = self.carpoint.add_car(car2)
        self.assertFalse(result)
        self.assertEqual(len(self.carpoint.cars), 1)
    
    def test_remove_car(self):
        """Test removing a car from inventory"""
        car = Car("CAR001", "Toyota", "Camry", 2022, 25000.00)
        self.carpoint.add_car(car)
        result = self.carpoint.remove_car("CAR001")
        self.assertTrue(result)
        self.assertEqual(len(self.carpoint.cars), 0)
    
    def test_remove_nonexistent_car(self):
        """Test removing a car that doesn't exist"""
        result = self.carpoint.remove_car("CAR999")
        self.assertFalse(result)
    
    def test_get_car(self):
        """Test getting a car by ID"""
        car = Car("CAR001", "Toyota", "Camry", 2022, 25000.00)
        self.carpoint.add_car(car)
        retrieved = self.carpoint.get_car("CAR001")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.car_id, "CAR001")
    
    def test_list_cars(self):
        """Test listing all cars"""
        car1 = Car("CAR001", "Toyota", "Camry", 2022, 25000.00)
        car2 = Car("CAR002", "Honda", "Civic", 2023, 28000.00)
        self.carpoint.add_car(car1)
        self.carpoint.add_car(car2)
        cars = self.carpoint.list_cars()
        self.assertEqual(len(cars), 2)
    
    def test_list_cars_by_status(self):
        """Test listing cars by status"""
        car1 = Car("CAR001", "Toyota", "Camry", 2022, 25000.00, "available")
        car2 = Car("CAR002", "Honda", "Civic", 2023, 28000.00, "sold")
        self.carpoint.add_car(car1)
        self.carpoint.add_car(car2)
        available_cars = self.carpoint.list_cars(status="available")
        self.assertEqual(len(available_cars), 1)
        self.assertEqual(available_cars[0].car_id, "CAR001")
    
    def test_update_car_status(self):
        """Test updating car status"""
        car = Car("CAR001", "Toyota", "Camry", 2022, 25000.00)
        self.carpoint.add_car(car)
        result = self.carpoint.update_car_status("CAR001", "sold")
        self.assertTrue(result)
        updated_car = self.carpoint.get_car("CAR001")
        self.assertEqual(updated_car.status, "sold")
    
    def test_search_cars_by_make(self):
        """Test searching cars by make"""
        car1 = Car("CAR001", "Toyota", "Camry", 2022, 25000.00)
        car2 = Car("CAR002", "Honda", "Civic", 2023, 28000.00)
        car3 = Car("CAR003", "Toyota", "Corolla", 2021, 22000.00)
        self.carpoint.add_car(car1)
        self.carpoint.add_car(car2)
        self.carpoint.add_car(car3)
        toyota_cars = self.carpoint.search_cars(make="Toyota")
        self.assertEqual(len(toyota_cars), 2)
    
    def test_search_cars_by_year(self):
        """Test searching cars by year"""
        car1 = Car("CAR001", "Toyota", "Camry", 2022, 25000.00)
        car2 = Car("CAR002", "Honda", "Civic", 2023, 28000.00)
        self.carpoint.add_car(car1)
        self.carpoint.add_car(car2)
        cars_2022 = self.carpoint.search_cars(year=2022)
        self.assertEqual(len(cars_2022), 1)
        self.assertEqual(cars_2022[0].car_id, "CAR001")
    
    def test_data_persistence(self):
        """Test that data is saved and loaded correctly"""
        car = Car("CAR001", "Toyota", "Camry", 2022, 25000.00)
        self.carpoint.add_car(car)
        
        # Create a new instance to test loading
        carpoint2 = CarPoint(self.test_file)
        self.assertEqual(len(carpoint2.cars), 1)
        loaded_car = carpoint2.get_car("CAR001")
        self.assertIsNotNone(loaded_car)
        self.assertEqual(loaded_car.make, "Toyota")


if __name__ == "__main__":
    unittest.main()
