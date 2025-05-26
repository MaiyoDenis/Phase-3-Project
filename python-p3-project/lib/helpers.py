# lib/helpers.py

from models import Session, Customer, Service, Order, Location, OrderStatusHistory
from datetime import datetime, date
import re

def exit_program():
    print("Thank you for using LaundryConnect CLI!")
    exit()

# ====== Customer Helpers ======

def view_all_customers():
    session = Session()
    customers = Customer.get_all(session)
    
    if not customers:
        print("\nNo customers found.")
        return
    
    print("\n===== All Customers =====")
    for customer in customers:
        print(f"ID: {customer.id} | Name: {customer.name} | Phone: {customer.phone}")
    
    session.close()

def find_customer_by_id():
    session = Session()
    
    try:
        id = int(input("\nEnter customer ID: "))
        customer = Customer.find_by_id(session, id)
        
        if customer:
            print(f"\nCustomer ID: {customer.id}")
            print(f"Name: {customer.name}")
            print(f"Phone: {customer.phone}")
            print(f"Email: {customer.email}")
            print(f"Address: {customer.address}")
        else:
            print(f"\nNo customer found with ID {id}")
    except ValueError:
        print("\nInvalid ID. Please enter a number.")
    
    session.close()

def find_customer_by_phone():
    session = Session()
    
    phone = input("\nEnter customer phone number: ")
    customer = Customer.find_by_phone(session, phone)
    
    if customer:
        print(f"\nCustomer ID: {customer.id}")
        print(f"Name: {customer.name}")
        print(f"Phone: {customer.phone}")
        print(f"Email: {customer.email}")
        print(f"Address: {customer.address}")
    else:
        print(f"\nNo customer found with phone number {phone}")
    
    session.close()

def add_customer():
    session = Session()
    
    print("\n===== Add New Customer =====")
    
    try:
        name = input("Enter customer name: ")
        phone = input("Enter phone number: ")
        email = input("Enter email (optional): ") or None
        address = input("Enter address (optional): ") or None
        
        customer = Customer.create(session, name, phone, email, address)
        print(f"\nCustomer added successfully with ID: {customer.id}")
    
    except ValueError as e:
        print(f"\nError: {str(e)}")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    
    session.close()

def update_customer():
    session = Session()
    
    try:
        id = int(input("\nEnter customer ID to update: "))
        customer = Customer.find_by_id(session, id)
        
        if not customer:
            print(f"\nNo customer found with ID {id}")
            return
        
        print("\nCurrent customer details:")
        print(f"Name: {customer.name}")
        print(f"Phone: {customer.phone}")
        print(f"Email: {customer.email}")
        print(f"Address: {customer.address}")
        
        print("\nEnter new details (leave blank to keep current value):")
        
        name = input("Name: ") or customer.name
        phone = input("Phone: ") or customer.phone
        email = input("Email: ") or customer.email
        address = input("Address: ") or customer.address
        
        updated_customer = Customer.update(session, id, name=name, phone=phone, email=email, address=address)
        
        if updated_customer:
            print("\nCustomer updated successfully!")
        else:
            print("\nFailed to update customer.")
            
    except ValueError as e:
        print(f"\nError: {str(e)}")
    
    session.close()

def delete_customer():
    session = Session()
    
    try:
        id = int(input("\nEnter customer ID to delete: "))
        customer = Customer.find_by_id(session, id)
        
        if not customer:
            print(f"\nNo customer found with ID {id}")
            return
        
        confirm = input(f"\nAre you sure you want to delete customer {customer.name}? (y/n): ")
        
        if confirm.lower() == 'y':
            if Customer.delete(session, id):
                print("\nCustomer deleted successfully!")
            else:
                print("\nFailed to delete customer.")
        else:
            print("\nDelete operation canceled.")
            
    except ValueError:
        print("\nInvalid ID. Please enter a number.")
    
    session.close()

def view_customer_orders():
    session = Session()
    
    try:
        id = int(input("\nEnter customer ID: "))
        customer = Customer.find_by_id(session, id)
        
        if not customer:
            print(f"\nNo customer found with ID {id}")
            return
        
        orders = Order.find_by_customer(session, id)
        
        if not orders:
            print(f"\nNo orders found for customer {customer.name}")
            return
        
        print(f"\n===== Orders for {customer.name} =====")
        for order in orders:
            service = Service.find_by_id(session, order.service_id)
            print(f"Order ID: {order.id} | Service: {service.name} | Status: {order.status} | Total: {order.total_price}")
        
    except ValueError:
        print("\nInvalid ID. Please enter a number.")
    
    session.close()

# ====== Service Helpers ======

def view_all_services():
    session = Session()
    services = Service.get_all(session)
    
    if not services:
        print("\nNo services found.")
        return
    
    print("\n===== All Services =====")
    for service in services:
        print(f"ID: {service.id} | Name: {service.name} | Price: {service.price_per_unit}/{service.unit}")
    
    session.close()

def find_service_by_id():
    session = Session()
    
    try:
        id = int(input("\nEnter service ID: "))
        service = Service.find_by_id(session, id)
        
        if service:
            print(f"\nService ID: {service.id}")
            print(f"Name: {service.name}")
            print(f"Description: {service.description}")
            print(f"Price: {service.price_per_unit} per {service.unit}")
        else:
            print(f"\nNo service found with ID {id}")
    except ValueError:
        print("\nInvalid ID. Please enter a number.")
    
    session.close()

def add_service():
    session = Session()
    
    print("\n===== Add New Service =====")
    
    try:
        name = input("Enter service name: ")
        description = input("Enter description: ")
        
        while True:
            try:
                price = float(input("Enter price per unit: "))
                if price <= 0:
                    print("Price must be positive.")
                    continue
                break
            except ValueError:
                print("Invalid price. Please enter a number.")
        
        unit = input("Enter unit (kg/item): ")
        if unit.lower() not in ['kg', 'item']:
            print("Unit must be 'kg' or 'item'. Defaulting to 'kg'.")
            unit = 'kg'
        
        service = Service.create(session, name, price, unit, description)
        print(f"\nService added successfully with ID: {service.id}")
    
    except ValueError as e:
        print(f"\nError: {str(e)}")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    
    session.close()

def update_service():
    session = Session()
    
    try:
        id = int(input("\nEnter service ID to update: "))
        service = Service.find_by_id(session, id)
        
        if not service:
            print(f"\nNo service found with ID {id}")
            return
        
        print("\nCurrent service details:")
        print(f"Name: {service.name}")
        print(f"Description: {service.description}")
        print(f"Price: {service.price_per_unit} per {service.unit}")
        
        print("\nEnter new details (leave blank to keep current value):")
        
        name = input("Name: ") or service.name
        description = input("Description: ") or service.description
        
        price_input = input(f"Price per {service.unit}: ")
        if price_input:
            try:
                price = float(price_input)
                if price <= 0:
                    print("Price must be positive. Keeping current value.")
                    price = service.price_per_unit
            except ValueError:
                print("Invalid price. Keeping current value.")
                price = service.price_per_unit
        else:
            price = service.price_per_unit
        
        unit_input = input("Unit (kg/item): ") or service.unit
        if unit_input.lower() not in ['kg', 'item']:
            print("Unit must be 'kg' or 'item'. Keeping current value.")
            unit = service.unit
        else:
            unit = unit_input
        
        updated_service = Service.update(
            session, id, 
            name=name, 
            description=description, 
            price_per_unit=price, 
            unit=unit
        )
        
        if updated_service:
            print("\nService updated successfully!")
        else:
            print("\nFailed to update service.")
            
    except ValueError as e:
        print(f"\nError: {str(e)}")
    
    session.close()

def delete_service():
    session = Session()
    
    try:
        id = int(input("\nEnter service ID to delete: "))
        service = Service.find_by_id(session, id)
        
        if not service:
            print(f"\nNo service found with ID {id}")
            return
        
        confirm = input(f"\nAre you sure you want to delete service {service.name}? (y/n): ")
        
        if confirm.lower() == 'y':
            if Service.delete(session, id):
                print("\nService deleted successfully!")
            else:
                print("\nFailed to delete service.")
        else:
            print("\nDelete operation canceled.")
            
    except ValueError:
        print("\nInvalid ID. Please enter a number.")
    
    session.close()

# ====== Order Helpers ======

def view_all_orders():
    session = Session()
    orders = Order.get_all(session)
    
    if not orders:
        print("\nNo orders found.")
        return
    
    print("\n===== All Orders =====")
    for order in orders:
        customer = Customer.find_by_id(session, order.customer_id)
        service = Service.find_by_id(session, order.service_id)
        print(f"ID: {order.id} | Customer: {customer.name} | Service: {service.name} | Status: {order.status} | Total: {order.total_price}")
    
    session.close()

def find_order_by_id():
    session = Session()
    
    try:
        id = int(input("\nEnter order ID: "))
        order = Order.find_by_id(session, id)
        
        if not order:
            print(f"\nNo order found with ID {id}")
            return
        
        customer = Customer.find_by_id(session, order.customer_id)
        service = Service.find_by_id(session, order.service_id)
        
        print(f"\nOrder ID: {order.id}")
        print(f"Customer: {customer.name} (ID: {customer.id})")
        print(f"Service: {service.name} (ID: {service.id})")
        print(f"Weight: {order.weight} {service.unit}")
        print(f"Total Price: {order.total_price}")
        print(f"Status: {order.status}")
        print(f"Pickup Date: {order.pickup_date}")
        print(f"Pickup Time: {order.pickup_time}")
        print(f"Special Instructions: {order.special_instructions or 'None'}")
        print(f"Created At: {order.created_at}")
        
    except ValueError:
        print("\nInvalid ID. Please enter a number.")
    
    session.close()

def add_order():
    session = Session()
    
    print("\n===== Add New Order =====")
    
    try:
        # Get customer
        while True:
            customer_input = input("Enter customer ID or phone number: ")
            
            if customer_input.isdigit():
                customer = Customer.find_by_id(session, int(customer_input))
            else:
                customer = Customer.find_by_phone(session, customer_input)
            
            if customer:
                print(f"Selected customer: {customer.name}")
                break
            else:
                print("Customer not found.")
                create_new = input("Would you like to create a new customer? (y/n): ")
                if create_new.lower() == 'y':
                    name = input("Enter customer name: ")
                    phone = input("Enter phone number: ")
                    email = input("Enter email (optional): ") or None
                    address = input("Enter address (optional): ") or None
                    
                    try:
                        customer = Customer.create(session, name, phone, email, address)
                        print(f"Customer created with ID: {customer.id}")
                        break
                    except ValueError as e:
                        print(f"Error: {str(e)}")
        
        # Get service
        view_all_services()
        while True:
            try:
                service_id = int(input("\nSelect service ID: "))
                service = Service.find_by_id(session, service_id)
                
                if service:
                    print(f"Selected service: {service.name} ({service.price_per_unit} per {service.unit})")
                    break
                else:
                    print("Service not found. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        # Get weight
        while True:
            try:
                weight = float(input(f"\nEnter weight in {service.unit}: "))
                if weight <= 0:
                    print("Weight must be positive.")
                    continue
                break
            except ValueError:
                print("Invalid weight. Please enter a number.")
        
        # Get pickup date
        while True:
            pickup_date_str = input("\nEnter pickup date (YYYY-MM-DD): ")
            try:
                pickup_date = datetime.strptime(pickup_date_str, '%Y-%m-%d').date()
                if pickup_date < date.today():
                    print("Pickup date cannot be in the past.")
                    continue
                break
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD.")
        
        # Get pickup time
        while True:
            print("\nPickup Time Options:")
            print("1. Morning (8:00 AM - 12:00 PM)")
            print("2. Afternoon (12:00 PM - 4:00 PM)")
            print("3. Evening (4:00 PM - 8:00 PM)")
            
            try:
                time_choice = int(input("\nSelect pickup time option: "))
                if time_choice == 1:
                    pickup_time = "morning"
                    break
                elif time_choice == 2:
                    pickup_time = "afternoon"
                    break
                elif time_choice == 3:
                    pickup_time = "evening"
                    break
                else:
                    print("Invalid choice. Please select 1, 2, or 3.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        # Get special instructions
        special_instructions = input("\nEnter special instructions (optional): ") or None
        
        # Create order
        order = Order.create(
            session,
            customer.id,
            service.id,
            weight,
            pickup_date,
            pickup_time,
            special_instructions
        )
        
        print(f"\nOrder created successfully with ID: {order.id}")
        print(f"Total price: {order.total_price}")
        
    except ValueError as e:
        print(f"\nError: {str(e)}")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
        session.rollback()
    
    session.close()

def update_order_status():
    session = Session()
    
    try:
        id = int(input("\nEnter order ID to update: "))
        order = Order.find_by_id(session, id)
        
        if not order:
            print(f"\nNo order found with ID {id}")
            return
        
        print(f"\nCurrent status: {order.status}")
        print("\nAvailable statuses:")
        print("1. placed")
        print("2. pickup")
        print("3. processing")
        print("4. delivery")
        print("5. completed")
        
        choice = input("\nSelect new status (1-5): ")
        
        status_map = {
            "1": "placed",
            "2": "pickup",
            "3": "processing",
            "4": "delivery",
            "5": "completed"
        }
        
        if choice in status_map:
            new_status = status_map[choice]
            
            if new_status == order.status:
                print(f"\nOrder is already in '{new_status}' status.")
                return
            
            updated_order = Order.update(session, id, status=new_status)
            
            if updated_order:
                print(f"\nOrder status updated to '{new_status}' successfully!")
            else:
                print("\nFailed to update order status.")
        else:
            print("\nInvalid choice.")
        
    except ValueError:
        print("\nInvalid ID. Please enter a number.")
    
    session.close()

def delete_order():
    session = Session()
    
    try:
        id = int(input("\nEnter order ID to delete: "))
        order = Order.find_by_id(session, id)
        
        if not order:
            print(f"\nNo order found with ID {id}")
            return
        
        customer = Customer.find_by_id(session, order.customer_id)
        
        confirm = input(f"\nAre you sure you want to delete order {id} for customer {customer.name}? (y/n): ")
        
        if confirm.lower() == 'y':
            if Order.delete(session, id):
                print("\nOrder deleted successfully!")
            else:
                print("\nFailed to delete order.")
        else:
            print("\nDelete operation canceled.")
            
    except ValueError:
        print("\nInvalid ID. Please enter a number.")
    
    session.close()

def view_order_history():
    session = Session()
    
    try:
        id = int(input("\nEnter order ID: "))
        order = Order.find_by_id(session, id)
        
        if not order:
            print(f"\nNo order found with ID {id}")
            return
        
        history = OrderStatusHistory.get_all_by_order(session, id)
        
        if not history:
            print(f"\nNo status history found for order {id}")
            return
        
        print(f"\n===== Status History for Order {id} =====")
        for entry in history:
            print(f"Status: {entry.status} | Timestamp: {entry.timestamp}")
        
    except ValueError:
        print("\nInvalid ID. Please enter a number.")
    
    session.close()

# ====== Location Helpers ======

def view_all_locations():
    session = Session()
    locations = Location.get_all(session)
    
    if not locations:
        print("\nNo locations found.")
        return
    
    print("\n===== All Locations =====")
    for location in locations:
        print(f"ID: {location.id} | Name: {location.name} | Address: {location.address}")
    
    session.close()

def find_location_by_id():
    session = Session()
    
    try:
        id = int(input("\nEnter location ID: "))
        location = Location.find_by_id(session, id)
        
        if location:
            print(f"\nLocation ID: {location.id}")
            print(f"Name: {location.name}")
            print(f"Address: {location.address}")
            print(f"Phone: {location.phone}")
            print(f"Email: {location.email}")
        else:
            print(f"\nNo location found with ID {id}")
    except ValueError:
        print("\nInvalid ID. Please enter a number.")
    
    session.close()

def add_location():
    session = Session()
    
    print("\n===== Add New Location =====")
    
    try:
        name = input("Enter location name: ")
        address = input("Enter address: ")
        phone = input("Enter phone number: ")
        email = input("Enter email (optional): ") or None
        
        location = Location.create(session, name, address, phone, email)
        print(f"\nLocation added successfully with ID: {location.id}")
    
    except ValueError as e:
        print(f"\nError: {str(e)}")
    except Exception as e:
        print(f"\nAn error occurred: {str(e)}")
    
    session.close()

def update_location():
    session = Session()
    
    try:
        id = int(input("\nEnter location ID to update: "))
        location = Location.find_by_id(session, id)
        
        if not location:
            print(f"\nNo location found with ID {id}")
            return
        
        print("\nCurrent location details:")
        print(f"Name: {location.name}")
        print(f"Address: {location.address}")
        print(f"Phone: {location.phone}")
        print(f"Email: {location.email}")
        
        print("\nEnter new details (leave blank to keep current value):")
        
        name = input("Name: ") or location.name
        address = input("Address: ") or location.address
        phone = input("Phone: ") or location.phone
        email = input("Email: ") or location.email
        
        updated_location = Location.update(
            session, id, 
            name=name, 
            address=address, 
            phone=phone, 
            email=email
        )
        
        if updated_location:
            print("\nLocation updated successfully!")
        else:
            print("\nFailed to update location.")
            
    except ValueError as e:
        print(f"\nError: {str(e)}")
    
    session.close()

def delete_location():
    session = Session()
    
    try:
        id = int(input("\nEnter location ID to delete: "))
        location = Location.find_by_id(session, id)
        
        if not location:
            print(f"\nNo location found with ID {id}")
            return
        
        confirm = input(f"\nAre you sure you want to delete location {location.name}? (y/n): ")
        
        if confirm.lower() == 'y':
            if Location.delete(session, id):
                print("\nLocation deleted successfully!")
            else:
                print("\nFailed to delete location.")
        else:
            print("\nDelete operation canceled.")
            
    except ValueError:
        print("\nInvalid ID. Please enter a number.")
    
    session.close()

# ====== Report Helpers ======

def generate_daily_orders_report():
    session = Session()
    
    print("\n===== Daily Orders Report =====")
    
    try:
        date_str = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
        
        if date_str:
            report_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            report_date = date.today()
        
        # Find all orders for the date
        orders = session.query(Order).filter(
            Order.created_at >= datetime.combine(report_date, datetime.min.time()),
            Order.created_at <= datetime.combine(report_date, datetime.max.time())
        ).all()
        
        if not orders:
            print(f"\nNo orders found for {report_date}")
            return
        
        total_revenue = sum(order.total_price for order in orders)
        orders_by_status = {}
        
        for order in orders:
            status = order.status
            if status not in orders_by_status:
                orders_by_status[status] = []
            orders_by_status[status].append(order)
        
        print(f"\nDate: {report_date}")
        print(f"Total Orders: {len(orders)}")
        print(f"Total Revenue: {total_revenue}")
        
        print("\nOrders by Status:")
        for status, status_orders in orders_by_status.items():
            print(f"  {status.capitalize()}: {len(status_orders)}")
        
        print("\nDetailed Orders:")
        for order in orders:
            customer = Customer.find_by_id(session, order.customer_id)
            service = Service.find_by_id(session, order.service_id)
            print(f"ID: {order.id} | Customer: {customer.name} | Service: {service.name} | Status: {order.status} | Total: {order.total_price}")
        
    except ValueError as e:
        print(f"\nError: {str(e)}")
    
    session.close()

def generate_customer_report():
    session = Session()
    
    try:
        id = int(input("\nEnter customer ID: "))
        customer = Customer.find_by_id(session, id)
        
        if not customer:
            print(f"\nNo customer found with ID {id}")
            return
        
        orders = Order.find_by_customer(session, id)
        
        print(f"\n===== Customer Report: {customer.name} =====")
        print(f"Phone: {customer.phone}")
        print(f"Email: {customer.email or 'N/A'}")
        print(f"Address: {customer.address or 'N/A'}")
        
        if not orders:
            print("\nNo orders found for this customer.")
            return
        
        total_spent = sum(order.total_price for order in orders)
        
        print(f"\nTotal Orders: {len(orders)}")
        print(f"Total Spent: {total_spent}")
        
        print("\nOrder History:")
        for order in orders:
            service = Service.find_by_id(session, order.service_id)
            print(f"ID: {order.id} | Date: {order.created_at.date()} | Service: {service.name} | Status: {order.status} | Total: {order.total_price}")
        
    except ValueError:
        print("\nInvalid ID. Please enter a number.")
    
    session.close()