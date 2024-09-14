# Rastak E-commerce

Rastak E-commerce is a Django-based e-commerce platform that supports multiple product categories, shopping carts, customer accounts, orders, and key performance indicators (KPIs) for tracking the business performance. The project is hosted on [GitHub](https://github.com/armanrasta/Rastak-ecommerce.git).

## Features

- **Customer Accounts**: Separate user and customer login systems. Customers can register, log in, and manage their profiles.
- **Product Management**: Add products with multiple images and organize them into categories and subcategories. Each product can have associated colors and stock levels.
- **Shopping Cart**: Customers can add products to their shopping carts, adjust quantities, and proceed to checkout.
- **Orders**: Orders are created during the checkout process. Customers can view their order history.
- **KPIs**: Daily and periodic KPIs, such as total revenue, repeat customers, and cart abandonment rate, are calculated to monitor business performance.
- **Admin Panel**: Customizable Django admin interface with KPI reports, order management, and product tracking.

## Key Performance Indicators (KPIs)

1. **Total Revenue**
2. **Total Orders**
3. **New Customers**
4. **Cart Abandonment Rate**
5. **Average Order Value**
6. **Customer Lifetime Value**
7. **Churn Rate**
8. **Repeat Purchase Rate**
9. **Purchase Frequency**
10. **Inventory Turnover**

## Technologies Used

- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (or configure your preferred database)
- **Other**: Celery (for background tasks), Redis (for task queue), Chart.js(for DailyKPI charts)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/armanrasta/Rastak-ecommerce.git
   cd Rastak-ecommerce
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser for the Django admin:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the server:
   ```bash
   python manage.py runserver
   ```

7. Open your browser and navigate to:
   ```
   http://127.0.0.1:8000/
   ```

## Usage

- Access the admin panel at `/admin` to manage products, customers, orders, and KPIs.
- Customers can browse products, add them to their cart, and complete orders.
- KPIs are updated daily using Celery and can be viewed in the admin panel.

## Background Task Setup

This project uses Celery and Redis to calculate DailyKPIs in the background.

1. Install Redis:
   ```bash
   sudo apt-get install redis-server
   ```

2. Run Redis:
   ```bash
   redis-server
   ```

3. Start Celery worker:
   ```bash
   celery -A rastak_ecommerce worker --loglevel=info
   ```

4. Start Celery beat for periodic tasks:
   ```bash
   celery -A rastak_ecommerce beat --loglevel=info
   ```
