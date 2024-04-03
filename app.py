from flask import Flask, render_template, request, redirect, url_for
import razorpay
app = Flask(__name__)

# Initialize Razorpay client
client = razorpay.Client(auth=("rzp_live_eBt3QMKkLRSXI1", "0kWpmXB3x8RjgA1ihwTaL6Hk"))

# Route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the menu page
@app.route('/menu', methods=['GET', 'POST'])
def menu():
    # Define your menu items as lists of dictionaries
    menu_special = [
        {'name': 'Paneer Butter Masala', 'price': 300},
        {'name': 'Palak Paneer', 'price': 270},
        {'name': 'Aloo Gobi', 'price': 220},
        {'name': 'Chana Masala', 'price': 230},
        {'name': 'Dal Tadka', 'price': 210}
    ]

    roti_special = [
        {'name': 'Roti Platter with Dips', 'price': 40},
        {'name': 'Roti Curry Combo', 'price': 80},
        {'name': 'Roti Basket', 'price': 60},
        {'name': 'Masala Roti', 'price': 30},
        {'name': 'Roti (Normal)', 'price': 15}
    ]

    if request.method == 'POST':
        # Get the selected items and quantities from the request
        selected_items = request.form.getlist('menu_item')
        quantities = {item: int(request.form.get(f'quantity[{item}]', 0)) for item in selected_items}

        # Calculate the total price
        total_price = calculate_total_price(selected_items, quantities)

        # Render the order page with the selected items and total price
        return render_template('order.html', selected_items=selected_items, quantities=quantities, total_price=total_price)

    return render_template('menu.html', menu_special=menu_special, roti_special=roti_special)

@app.route('/about')
def about():
    return render_template('about.html')





@app.route('/order', methods=['POST'])
def order():
    # Define the item_prices dictionary
    item_prices = {
        'Paneer Butter Masala': 300,
        'Palak Paneer': 270,
        'Aloo Gobi': 220,
        'Chana Masala': 230,
        'Dal Tadka': 210,
        'Roti Platter with Dips': 40,
        'Roti Curry Combo': 80,
        'Roti Basket': 60,
        'Masala Roti': 30,
        'Roti (Normal)': 15
    }

    # Get the selected menu items and quantities from the request
    selected_items = request.form.getlist('menu_item')
    quantities = {item: int(request.form.get(f'quantity[{item}]', 0)) for item in selected_items}

    # Calculate the total price based on the selected items and quantities
    total_price = calculate_total_price(selected_items, quantities)
    total_price = float(total_price)

    # Create a list of dictionaries containing item, quantity, and price
    order_details = []
    for item, quantity in quantities.items():
        if quantity > 0:
            price = item_prices.get(item, 0)
            order_details.append({'name': item, 'quantity': quantity, 'price': price})

    return render_template('order.html', order_details=order_details, total_price=total_price)


# @app.route('/payment', methods=['POST'])
# def payment():
#     # Get the total price from the order page
#     total_price = request.form.get('total_price')

#     # Create order data for Razorpay
#     data = {
#         "amount": int(float(total_price) * 100),  # Convert the price to paise
#         "currency": "INR",
#         "receipt": "#11",
#         "partial_payment": False
#     }

#     # Create an order with Razorpay
#     payment = client.order.create(data=data)
#     order_id = payment['id']

#     # Render the payment page with the order details
#     return render_template('payment.html', order_id=order_id, amount=data['amount'])
@app.route('/payment', methods=['GET'])
def payment():
    total_price = request.args.get('total_price', 0)
    # Render the payment template with the total price
    return render_template('payment.html', total_price=total_price)

# Function to calculate the total price
def calculate_total_price(selected_items, quantities):
    total_price = 0
    # Assuming you have a dictionary of item prices
    item_prices = {
        'Paneer Butter Masala': float(300),
        'Palak Paneer':float(270),
        'Aloo Gobi': float(220),
        'Chana Masala': float(230),
        'Dal Tadka': float(210),
        'Roti Platter with Dips': float(40),
        'Roti Curry Combo': float(80),
        'Roti Basket': float(60),
        'Masala Roti': float(30),
        'Roti (Normal)': float(15)
    }

    for item, quantity in quantities.items():
        if quantity > 0:
            total_price += item_prices.get(item, 0) * quantity

    return total_price


@app.route('/place_order', methods=['POST'])
def place_order():
    # Get the order details from the request
    selected_items = request.form.getlist('menu_item')
    quantities = {item: int(request.form.get(f'quantity[{item}]', 0)) for item in selected_items}
    parcel_option = request.form.get('parcel-option', False)

    # Calculate the total price
    total_price = calculate_total_price(selected_items, quantities)

    # Store the order in a database or process it as needed
    # ...

    # Optionally, you can clear the order data from the session

    # Redirect to the payment page
    return redirect(url_for('payment', total_price=total_price))


@app.route('/remove_item/<item>', methods=['GET'])
def remove_item(item):
    item_prices = {
        'Paneer Butter Masala': float(300),
        'Palak Paneer':float(270),
        'Aloo Gobi': float(220),
        'Chana Masala': float(230),
        'Dal Tadka': float(210),
        'Roti Platter with Dips': float(40),
        'Roti Curry Combo': float(80),
        'Roti Basket': float(60),
        'Masala Roti': float(30),
        'Roti (Normal)': float(15)
    }
    # Remove the item from the order data
    selected_items = request.args.getlist('selected_items')
    quantities = {item: int(request.args.get(f'quantity[{item}]', 0)) for item in selected_items}

    if item in selected_items:
        selected_items.remove(item)
        del quantities[item]

    # Recalculate the total price
    total_price = calculate_total_price(selected_items, quantities)
    order_details = []
    for item, quantity in quantities.items():
        if quantity > 0:
            price = item_prices.get(item, 0)
            order_details.append({'name': item, 'quantity': quantity, 'price': price})

    return render_template('order.html', order_details=order_details, total_price=total_price)
#     return render_template('order.html', selected_items=selected_items, quantities=quantities, total_price=total_price, item_prices=item_prices)
if __name__ == '__main__':
    app.run(debug=True)