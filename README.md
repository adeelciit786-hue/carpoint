# CarPoint - Car Inventory Management System

A simple and efficient car dealership inventory management system written in Python.

## Features

- **Add Cars**: Add new cars to the inventory with unique IDs
- **Remove Cars**: Remove cars from the inventory
- **Search**: Search for cars by make, model, or year
- **Status Management**: Track car status (available, sold, etc.)
- **Data Persistence**: Automatically saves and loads inventory data

## Installation

No external dependencies required. Just clone the repository:

```bash
git clone https://github.com/adeelciit786-hue/carpoint.git
cd carpoint
```

## Usage

### Basic Example

```python
from carpoint import Car, CarPoint

# Create a CarPoint instance
cp = CarPoint()

# Add a car
car = Car("CAR001", "Toyota", "Camry", 2022, 25000.00)
cp.add_car(car)

# List all cars
for car in cp.list_cars():
    print(car)

# Search for cars
toyota_cars = cp.search_cars(make="Toyota")

# Update car status
cp.update_car_status("CAR001", "sold")
```

### Running the Demo

```bash
python carpoint.py
```

## API Reference

### Car Class

```python
Car(car_id: str, make: str, model: str, year: int, price: float, status: str = "available")
```

### CarPoint Class

- `add_car(car: Car) -> bool`: Add a car to inventory
- `remove_car(car_id: str) -> bool`: Remove a car from inventory
- `get_car(car_id: str) -> Optional[Car]`: Get a car by ID
- `list_cars(status: Optional[str] = None) -> List[Car]`: List all cars
- `update_car_status(car_id: str, status: str) -> bool`: Update car status
- `search_cars(make, model, year) -> List[Car]`: Search for cars

## Testing

Run the test suite:

```bash
python -m unittest test_carpoint.py
```

## Data Storage

Data is automatically saved to `carpoint_data.json` in the current directory.

## License

MIT License
