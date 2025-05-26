markdown

# LaundryConnect CLI

A command-line interface application for managing a laundry service business. This Python application allows you to track customers, orders, services, and locations for your laundry business.

## Features

- Customer Management: Add, view, update, and delete customer records
- Order Management: Create orders, update order status, and track order history
- Service Management: Define laundry services with pricing
- Location Management: Track different business locations
- Reporting: Generate daily order reports and customer reports

## Installation

1. Clone this repository

git clone https://github.com/yourusername/laundry-connect-cli.git
cd laundry-connect-cli


2. Install dependencies

pipenv install


3. Activate the virtual environment

pipenv shell


4. Seed the database with initial data (optional)

python lib/db/seed.py


5. Run the application

python lib/cli.py
sql_more


## Database Models

The application uses SQLAlchemy ORM with the following models:

- **Customer**: Stores customer information (name, phone, email, address)
- **Service**: Defines available laundry services (name, description, price)
- **Order**: Tracks customer orders with status and details
- **Location**: Manages business locations
- **OrderStatusHistory**: Maintains a history of order status changes

## Usage

The CLI provides an intuitive menu-driven interface. Navigate through menus by entering the number corresponding to your choice.

### Main Menu

===== Main Menu =====

    Customer Management
    Order Management
    Service Management
    Location Management
    Reports
    Exit

angelscript


### Example Workflow

1. Add a customer
2. Add a service (if not already available)
3. Create an order for the customer
4. Update order status as it progresses
5. Generate reports to track business performance

## Development

- Models are located in `lib/models/`
- CLI interface is in `lib/cli.py`
- Helper functions are in `lib/helpers.py`
- Database seeding script is in `lib/db/seed.py`

## License

MIT License

6. Running the Application

To run the application:

    Install dependencies:

pipenv install
pipenv shell

    Seed the database (optional):

python lib/db/seed.py

    Run the CLI:

python lib/cli.py
