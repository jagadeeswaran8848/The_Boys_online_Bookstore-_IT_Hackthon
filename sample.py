from flask import Flask, render_template, redirect, url_for, request, session
from flask_session import Session
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SECRET_KEY'] = 'your_secret_key'  

Session(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['product']  

users = db['users']

col = db['books']  
col.delete_many({})  

sample_products = [
     {'name': 'Book 1', 'description': 'Description for Book 1', 'price': 20.99, 'image_url': 'https://via.placeholder.com/150', 'genre': 'Fiction'},
    {'name': 'Book 2', 'description': 'Description for Book 2', 'price': 15.99, 'image_url': 'https://via.placeholder.com/150', 'genre': 'Mystery'},
    {'name': 'Book 3', 'description': 'Description for Book 3', 'price': 25.99, 'image_url': 'https://via.placeholder.com/150', 'genre': 'Science Fiction'},
    {'name': 'Book 4', 'description': 'Description for Book 4', 'price': 18.50, 'image_url': 'https://via.placeholder.com/150', 'genre': 'Fantasy'},
    {'name': 'Book 5', 'description': 'Description for Book 5', 'price': 22.75, 'image_url': 'https://via.placeholder.com/150', 'genre': 'Horror'},
    {'name': 'Book 6', 'description': 'Description for Book 6', 'price': 19.99, 'image_url': 'https://via.placeholder.com/150', 'genre': 'Thriller'},
    {'name': 'Book 7', 'description': 'Description for Book 7', 'price': 16.49, 'image_url': 'https://via.placeholder.com/150', 'genre': 'Historical Fiction'},
    {'name': 'Book 8', 'description': 'Description for Book 8', 'price': 27.99, 'image_url': 'https://via.placeholder.com/150', 'genre': 'Biography'},
    {'name': 'Book 9', 'description': 'Description for Book 9', 'price': 23.25, 'image_url': 'https://via.placeholder.com/150', 'genre': 'Self-Help'},
    {'name': 'Book 10', 'description': 'Description for Book 10', 'price': 15.99, 'image_url': 'https://via.placeholder.com/150', 'genre': 'Adventure'}
    ]
col.insert_many(sample_products)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = users.find_one({'username': username, 'password': password})

        if user:
            session['user_id'] = str(user['_id'])
            return redirect(url_for('home'))

        error_message = 'Invalid username or password. Please try again.'
        return render_template('login.html', error_message=error_message)

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        existing_user = users.find_one({'username': username})

        if existing_user:
            error_message = 'Username already taken. Please choose a different username.'
            return render_template('signup.html', error_message=error_message)

        new_user = {'username': username, 'password': password}
        user_id = users.insert_one(new_user).inserted_id

        session['user_id'] = str(user_id)
        return redirect(url_for('home'))

    return render_template('signup.html')

@app.route('/products')
def products():
    product_data = col.find()
    return render_template('products.html', products=product_data)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity'))

        product = products.find_one({"_id": ObjectId(product_id)})

        if 'cart' not in session:
            session['cart'] = []

        product_in_cart = next((item for item in session['cart'] if item['product_id'] == str(product_id)), None)

        if product_in_cart:
            product_in_cart['quantity'] += quantity
        else:
            session['cart'].append({
                'product_id': str(product_id),
                'name': product['name'],
                'price': product['price'],
                'quantity': quantity
            })

        return redirect(url_for('cart'))

    cart_items = session.get('cart', [])

    total_price = sum(item['price'] * item['quantity'] for item in cart_items)

    return render_template('cart.html', items=cart_items, total_price=total_price)

if __name__ == '__main__':
    app.run(debug=True)
