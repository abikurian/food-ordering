# 🍔 Food Ordering System

![Food Ordering Banner](https://cdn-icons-png.flaticon.com/512/3075/3075977.png)  

A **Database-Driven Food Ordering Web Application** built with **Flask** and **MySQL**.  
Easily browse restaurants, add items to your cart, and place orders — all from a sleek, modern interface.  

---

## 🎯 Features

- Browse multiple restaurants and their menus.
- Add, remove, and manage items in the shopping cart.
- Place orders with real-time total calculation.
- View your order history with details of items and total cost.
- Clean, responsive, and professional UI with Bootstrap 5.
- Fully database-driven using **MySQL** and **PyMySQL**.

---

## 🛠 Technology Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3, Flask |
| Frontend | HTML5, CSS3, Bootstrap 5, Jinja2 Templates |
| Database | MySQL |
| ORM/Connector | PyMySQL |

---

## 🗂 Project Structure


---

## 💻 Setup & Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/food-ordering.git
cd food-ordering/backend

2. Create a virtual environment and install dependencies

python -m venv venv
venv\Scripts\activate       # Windows
# source venv/bin/activate  # macOS/Linux

pip install -r requirements.txt


3. Create the database

CREATE DATABASE food_ordering_db;
USE food_ordering_db;

-- Add tables: restaurants, menu, orders, order_items
-- Run SQL scripts from `database/init.sql`


4. Update config.py with your MySQL credentials:

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='yourpassword',
        database='food_ordering_db',
        cursorclass=pymysql.cursors.DictCursor
    )


5. Run the app

python app.py


Visit http://127.0.0.1:5000 in your browser.

📝 Future Improvements

User authentication with multiple customer accounts.

Payment gateway integration.

Search and filter restaurants by cuisine or rating.

Admin panel to add/update restaurants and menu items dynamically.