# Dripshop Pro

## Overview
Dripshop Pro is a **self-hosted Enterprise Resource Planning (ERP) system** designed specifically for **dropshipping businesses**. It streamlines operations like **order management, vendor coordination, inventory tracking, billing, analytics, and reporting** into a single, integrated platform.

## Features
- **User Management**: Role-based authentication for Admins, Merchants, Vendors, and Customers.
- **Product & Inventory Management**: Vendor-based stock tracking and product listings.
- **Order Management**: Multi-vendor order processing and fulfillment.
- **Billing & Invoicing**: Automated PDF invoice generation using wkhtmltopdf.
- **Reporting & Analytics**: Real-time insights into sales trends and vendor performance.
- **Dispute & Refund Handling**: Customer complaint resolution and refund tracking.

## Tech Stack
- **Backend**: Django (Python) with Django ORM & MySQL.
- **Frontend**: HTML, CSS, JavaScript (Bootstrap optional for responsiveness).
- **Database**: MySQL.
- **Security**: Django Auth System, JWT-based authentication.
- **Payments & Invoicing**: wkhtmltopdf for invoice generation, future Stripe/PayPal integration.

## Installation
### Prerequisites
- Python 3.8+
- MySQL Server
- wkhtmltopdf
- Virtual Environment (recommended)

### Setup Instructions
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/dripshop-pro.git
   cd dripshop-pro
   ```
2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Configure MySQL database settings in `settings.py`.
5. Apply migrations:
   ```sh
   python manage.py migrate
   ```
6. Create a superuser:
   ```sh
   python manage.py createsuperuser
   ```
7. Start the development server:
   ```sh
   python manage.py runserver
   ```

## Usage
- Access the admin panel: `http://127.0.0.1:8000/admin/`
- Register merchants, vendors, and products.
- Process orders and generate invoices automatically.
- Monitor analytics and manage disputes/refunds.

---
Developed with Django & MySQL to empower dropshipping businesses with an integrated ERP solution.
