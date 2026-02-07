"""
CarPoint - A simple car inventory management system
"""
import json
import os
import logging
from typing import List, Optional, Dict

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class Car:
    """Represents a car in the inventory"""
    
    def __init__(self, car_id: str, make: str, model: str, year: int, price: float, status: str = "available"):
        self.car_id = car_id
        self.make = make
        self.model = model
        self.year = year
        self.price = price
        self.status = status
    
    def to_dict(self) -> Dict:
        """Convert car to dictionary for serialization"""
        return {
            "car_id": self.car_id,
            "make": self.make,
            "model": self.model,
            "year": self.year,
            "price": self.price,
            "status": self.status
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Car':
        """Create a Car instance from dictionary"""
        return cls(
            car_id=data["car_id"],
            make=data["make"],
            model=data["model"],
            year=data["year"],
            price=data["price"],
            status=data.get("status", "available")
        )
    
    def __str__(self) -> str:
        return f"Car({self.car_id}): {self.year} {self.make} {self.model} - ${self.price:.2f} [{self.status}]"


class CarPoint:
    """Manages a car inventory system"""
    
    VALID_STATUSES = {"available", "sold", "reserved", "maintenance"}
    
    def __init__(self, data_file: str = "carpoint_data.json"):
        self.data_file = data_file
        self.cars: Dict[str, Car] = {}
        self.load_data()
    
    def add_car(self, car: Car) -> bool:
        """Add a car to the inventory"""
        if car.car_id in self.cars:
            return False
        self.cars[car.car_id] = car
        self.save_data()
        return True
    
    def remove_car(self, car_id: str) -> bool:
        """Remove a car from the inventory"""
        if car_id not in self.cars:
            return False
        del self.cars[car_id]
        self.save_data()
        return True
    
    def get_car(self, car_id: str) -> Optional[Car]:
        """Get a car by ID"""
        return self.cars.get(car_id)
    
    def list_cars(self, status: Optional[str] = None) -> List[Car]:
        """List all cars, optionally filtered by status"""
        if status:
            return [car for car in self.cars.values() if car.status == status]
        return list(self.cars.values())
    
    def update_car_status(self, car_id: str, status: str) -> bool:
        """
        Update the status of a car
        
        Valid statuses: available, sold, reserved, maintenance
        """
        if car_id not in self.cars:
            return False
        if status not in self.VALID_STATUSES:
            logger.warning(f"Status '{status}' is not in valid statuses: {self.VALID_STATUSES}")
        self.cars[car_id].status = status
        self.save_data()
        return True
    
    def search_cars(self, make: Optional[str] = None, model: Optional[str] = None, 
                   year: Optional[int] = None) -> List[Car]:
        """Search for cars by make, model, or year"""
        results = list(self.cars.values())
        
        if make:
            results = [car for car in results if car.make.lower() == make.lower()]
        if model:
            results = [car for car in results if car.model.lower() == model.lower()]
        if year:
            results = [car for car in results if car.year == year]
        
        return results
    
    def save_data(self) -> None:
        """Save inventory to JSON file"""
        data = {car_id: car.to_dict() for car_id, car in self.cars.items()}
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self) -> None:
        """Load inventory from JSON file"""
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.cars = {car_id: Car.from_dict(car_data) 
                           for car_id, car_data in data.items()}
        except (json.JSONDecodeError, KeyError) as e:
            # If file is corrupted, start fresh
            logger.warning(f"Data file '{self.data_file}' is corrupted ({e}). Starting with empty inventory.")
            self.cars = {}


def main():
    """Example usage of the CarPoint system"""
    cp = CarPoint()
    
    # Add some sample cars
    car1 = Car("CAR001", "Toyota", "Camry", 2022, 25000.00)
    car2 = Car("CAR002", "Honda", "Civic", 2023, 28000.00)
    car3 = Car("CAR003", "Ford", "Mustang", 2021, 35000.00)
    
    cp.add_car(car1)
    cp.add_car(car2)
    cp.add_car(car3)
    
    # List all cars
    print("All cars in inventory:")
    for car in cp.list_cars():
        print(f"  {car}")
    
    # Search for cars
    print("\nToyota cars:")
    for car in cp.search_cars(make="Toyota"):
        print(f"  {car}")
    
    # Update car status
    cp.update_car_status("CAR001", "sold")
    
    # List available cars
    print("\nAvailable cars:")
    for car in cp.list_cars(status="available"):
        print(f"  {car}")


if __name__ == "__main__":
    main()
