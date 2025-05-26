# lib/db/seed.py

from models import Base, engine, Session, Customer, Service, Order, Location
from datetime import datetime, date, timedelta

def seed_database():
    # Create all tables
    Base.metadata.create_all(engine)
    
    # Create a session
    session = Session()
    
    # Check if data already exists
    if session.query(Service).count() > 0:
        print("Database already seeded. Skipping...")
        session.close()
        return
    
    print("Seeding database...")
    
    # Seed services
    services = [
        {
            "name": "Standard Wash & Iron",
            "description": "Regular clothes washing with premium detergents and expert ironing.",
            "price_per_unit": 200,
            "unit": "kg"
        },
        {
            "name": "Express Service",
            "description": "Same day service for urgent laundry needs. Available 7 days a week.",
            "price_per_unit": 350,
            "unit": "kg"
        },
        {
            "name": "Dry Cleaning",
            "description": "Professional dry cleaning for suits, coats, and delicate fabrics.",
            "price_per_unit": 500,
            "unit": "item"
        }
    ]
    
    for service_data in services:
        service = Service(
            name=service_data["name"],
            description=service_data["description"],
            price_per_unit=service_data["price_per_unit"],
            unit=service_data["unit"]
        )
        session.add(service)
    
    # Seed locations
    locations = [
        {
            "name": "LaundryConnect Main Branch",
            "address": "123 Mombasa Rd, Nairobi",
            "phone": "+254 700 123456",
            "email": "main@laundryconnect.co.ke"
        },
        {
            "name": "LaundryConnect Westlands",
            "address": "456 Waiyaki Way, Westlands",
            "phone": "+254 700 234567",
            "email": "westlands@laundryconnect.co.ke"
        }
    ]
    
    for location_data in locations:
        location = Location(
            name=location_data["name"],
            address=location_data["address"],
            phone=location_data["phone"],
            email=location_data["email"]
        )
        session.add(location)
    
    # Seed customers
    customers = [
        {
            "name": "John Doe",
            "phone": "0712345678",
            "email": "john@example.com",
            "address": "123 Mombasa Rd, Nairobi"
        },
        {
            "name": "Jane Smith",
            "phone": "0723456789",
            "email": "jane@example.com",
            "address": "456 Ngong Rd, Nairobi"
        },
        {
            "name": "Michael Wanjau",
            "phone": "0734567890",
            "email": "michael@example.com",
            "address": "789 Thika Rd, Nairobi"
        }
    ]
    
    for customer_data in customers:
        customer = Customer(
            name=customer_data["name"],
            phone=customer_data["phone"],
            email=customer_data["email"],
            address=customer_data["address"]
        )
        session.add(customer)
    
    # Commit to get IDs
    session.commit()
    
    # Get the created records
    customers = session.query(Customer).all()
    services = session.query(Service).all()
    
    # Seed orders
    yesterday = date.today() - timedelta(days=1)
    today = date.today()
    tomorrow = date.today() + timedelta(days=1)
    
    orders = [
        {
            "customer": customers[0],
            "service": services[0],
            "weight": 2,
            "pickup_date": tomorrow,
            "pickup_time": "morning",
            "special_instructions": "Please handle with care"
        },
        {
            "customer": customers[1],
            "service": services[1],
            "weight": 3,
            "pickup_date": tomorrow,
            "pickup_time": "afternoon",
            "special_instructions": None
        },
        {
            "customer": customers[2],
            "service": services[2],
            "weight": 2,
            "pickup_date": yesterday,
            "pickup_time": "evening",
            "special_instructions": "Suits need special care",
            "status": "processing"
        }
    ]
    
    for order_data in orders:
        # Calculate total price
        total_price = order_data["service"].price_per_unit * order_data["weight"]
        
        order = Order(
            customer_id=order_data["customer"].id,
            service_id=order_data["service"].id,
            weight=order_data["weight"],
            total_price=total_price,
            pickup_date=order_data["pickup_date"],
            pickup_time=order_data["pickup_time"],
            special_instructions=order_data["special_instructions"]
        )
        
        if "status" in order_data:
            order.status = order_data["status"]
        
        session.add(order)
    
    # Commit all changes
    session.commit()
    
    print("Database seeded successfully!")
    session.close()

if __name__ == "__main__":
    seed_database()