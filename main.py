from flask import Flask, render_template, request, redirect, jsonify
import json
import uuid

app = Flask(__name__)

def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hire')
def hire():
    dresses = load_json('data/hire_dresses.json')
    return render_template('hire.html', dresses=dresses)

@app.route('/buy')
def buy():
    dresses = load_json('data/buy_dresses.json')
    return render_template('buy.html', dresses=dresses)

@app.route('/checkout')
def checkout():
    cart = load_json('data/user_carts.json')
    total = sum(item['price'] for item in cart)
    return render_template('checkout.html', cart=cart, total=total)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    item = request.json
    cart = load_json('data/user_carts.json')
    cart.append(item)
    save_json('data/user_carts.json', cart)
    return jsonify({'status': 'success'})

@app.route('/submit_cash', methods=['POST'])
def submit_cash():
    info = request.form
    cart = load_json('data/user_carts.json')
    receipt_no = str(uuid.uuid4())[:8]
    order = {
        "receipt": receipt_no,
        "method": "Cash on Delivery",
        "address": info['address'],
        "order": cart
    }
    orders = load_json('data/orders.json')
    orders.append(order)
    save_json('data/orders.json', orders)
    message = f"Order #{receipt_no}\nAddress: {info['address']}\nItems: {len(cart)}\nTotal incl R20 delivery."
    whatsapp_url = f"https://wa.me/27696345791?text={message.replace(' ', '%20')}"
    return redirect(whatsapp_url)

@app.route('/submit_eft', methods=['POST'])
def submit_eft():
    info = request.form
    receipt_no = str(uuid.uuid4())[:8]
    order = {
        "receipt": receipt_no,
        "method": "EFT",
        "reference": info['reference'],
        "name": info['name'],
        "phone": info['phone']
    }
    orders = load_json('data/orders.json')
    orders.append(order)
    save_json('data/orders.json', orders)
    message = f"EFT Payment\nRef: {info['reference']}\nName: {info['name']}\nPhone: {info['phone']}\nOrder: #{receipt_no}"
    whatsapp_url = f"https://wa.me/27696345791?text={message.replace(' ', '%20')}"
    return redirect(whatsapp_url)

if __name__ == '__main__':
    app.run(debug=True)
