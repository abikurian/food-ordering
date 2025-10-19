# backend/app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from config import get_connection
from datetime import datetime
# --- Flask App Setup ---
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = "my_super_secret_key_123"  # Required for session management

# ================================
# --- ROUTES ---
# ================================

# --- HOME / RESTAURANTS ---
@app.route('/')
def home():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM restaurants")
    restaurants = cur.fetchall()
    conn.close()

    current_year = datetime.now().year  # Pass current year
    return render_template('menu.html', restaurants=restaurants, current_year=current_year)


# --- RESTAURANT MENU ---
@app.route('/restaurant/<int:rid>')
def restaurant_menu(rid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM restaurants WHERE restaurant_id=%s", (rid,))
    restaurant = cur.fetchone()

    cur.execute("SELECT * FROM menu WHERE restaurant_id=%s", (rid,))
    items = cur.fetchall()

    conn.close()
    return render_template('order.html', restaurant=restaurant, items=items)


# --- CART MANAGEMENT ---

# Add item to cart
@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    item_id = int(request.form['item'])

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM menu WHERE item_id=%s", (item_id,))
    item = cur.fetchone()
    conn.close()

    # Convert price to float
    item['price'] = float(item['price'])

    # Get cart from session
    cart = session.get('cart', [])

    # If item already exists in cart, increase quantity
    for c in cart:
        if c['item_id'] == item_id:
            c['quantity'] += 1
            break
    else:
        # Add new item with quantity 1
        item['quantity'] = 1
        cart.append(item)

    session['cart'] = cart
    flash(f"Added {item['item_name']} to cart!")
    return redirect(request.referrer)


# View cart
@app.route('/cart')
def view_cart():
    cart = session.get('cart', [])
    total = sum(i['price'] * i['quantity'] for i in cart)
    return render_template('cart.html', cart=cart, total=total)


# Remove item from cart
@app.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    item_index = int(request.form['item_id'])
    cart = session.get('cart', [])
    if 0 <= item_index < len(cart):
        removed_item = cart.pop(item_index)
        session['cart'] = cart
        flash(f"Removed {removed_item['item_name']} from cart.")
    return redirect(url_for('view_cart'))


# Checkout / Place Order
@app.route('/cart/checkout', methods=['POST'])
def checkout():
    cart = session.get('cart', [])
    if not cart:
        flash("Cart is empty!")
        return redirect(url_for('home'))

    customer_id = 1  # Temporary fixed customer
    total = sum(i['price'] * i['quantity'] for i in cart)

    conn = get_connection()
    cur = conn.cursor()

    # Insert into orders table
    cur.execute(
        "INSERT INTO orders (customer_id, total_amount, status) VALUES (%s, %s, %s)",
        (customer_id, total, 'Completed')
    )
    order_id = cur.lastrowid

    # Insert each item into order_items table
    for item in cart:
        subtotal = item['price'] * item['quantity']
        cur.execute(
            "INSERT INTO order_items (order_id, item_id, quantity, subtotal) VALUES (%s, %s, %s, %s)",
            (order_id, item['item_id'], item['quantity'], subtotal)
        )

    conn.commit()
    conn.close()

    # Clear cart after checkout
    session.pop('cart', None)
    flash(f"Order placed successfully! Your Order ID is {order_id}.")
    return redirect(url_for('home'))


# --- VIEW PAST ORDERS ---
@app.route('/orders')
def view_orders():
    customer_id = 1  # Temporary fixed customer

    conn = get_connection()
    cur = conn.cursor()

    # Fetch all orders for the customer
    cur.execute("SELECT * FROM orders WHERE customer_id=%s ORDER BY order_id DESC", (customer_id,))
    orders = cur.fetchall()

    # Fetch items for each order
    orders_with_items = []
    for order in orders:
        cur.execute("""
            SELECT m.item_name, oi.quantity, oi.subtotal 
            FROM order_items oi
            JOIN menu m ON oi.item_id = m.item_id
            WHERE oi.order_id=%s
        """, (order['order_id'],))
        items = cur.fetchall()
        orders_with_items.append({'order': order, 'order_items': items})

    conn.close()
    return render_template('orders.html', orders=orders_with_items)


# ================================
# --- RUN APP ---
# ================================
if __name__ == '__main__':
    app.run(debug=True)
