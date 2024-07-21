from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

login_manager = LoginManager()
db = SQLAlchemy(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)

# models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    cart = db.relationship('Cart', backref='user', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# user

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if 'username' in data and 'password' in data:
        user = User.query.filter_by(username=data['username'], password=data['password']).first()
        if user:
            login_user(user)
            return jsonify({'message': 'Login successful!'}), 200
        return jsonify({'message': 'Invalid credentials!'}), 401
    return jsonify({'message': 'Invalid data!'}), 400

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful!'}), 200

# products

@app.route('/api/products/add', methods=['POST'])
@login_required
def add_product():
    data = request.json
    if 'name' in data and 'price' in data:
        product = Product(name=data['name'], price=data['price'], description=data.get('description', ''))
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'Product added!'}), 200
    return jsonify({'message': 'Invalid data!'}), 400

@app.route('/api/products/delete/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted!'}), 200
    return jsonify({'message': 'Product not found!'}), 404

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_produt_details(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'description': product.description
        }), 200
    return jsonify({'message': 'Product not found!'}), 404

@app.route('/api/products/update/<int:product_id>', methods=['PUT'])
@login_required
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found!'}), 404
    
    data = request.json
    if 'name' in data:
        product.name = data['name']
        
    if 'price' in data:
        product.price = data['price']
        
    if 'description' in data:
        product.description = data['description']
        
    db.session.commit()
    
    return jsonify({'message': 'Product updated!'}), 200

@app.route('/api/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    if not products:
        return jsonify({'message': 'No products found!'}), 404
    response = []
    for product in products:
        response.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
        })
    return jsonify(response), 200

# cart

@app.route('/api/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    user = User.query.get(int(current_user.id))
    product = Product.query.get(product_id)

    if user and product:
        cart = Cart(user_id=user.id, product_id=product.id)
        db.session.add(cart)
        db.session.commit()
        return jsonify({'message': 'Product added to cart!'}), 200
    return jsonify({'message': 'Failed to add item to the cart'}), 400

@app.route('/api/cart/remove/<int:product_id>', methods=['DELETE'])
@login_required
def remove_from_cart(product_id):
    cart = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    
    if cart:
        db.session.delete(cart)
        db.session.commit()
        return jsonify({'message': 'Product removed from cart!'}), 200
    return jsonify({'message': 'Failed to remove product'}), 400

@app.route('/api/cart', methods=['GET'])
@login_required
def get_cart():
    user = User.query.get(int(current_user.id))
    cart = user.cart
    response = []
    for item in cart:
        product = Product.query.get(item.product_id)
        response.append({
            'id': product.id,
            'user_id': user.id,
            'product_id': product.id,
            'product_name': product.name,
            'product_price': product.price,
        })
    return jsonify(response), 200
        
@app.route('/api/cart/checkout', methods=['POST'])
@login_required
def checkout():
    user = User.query.get(int(current_user.id))
    cart = user.cart
    total = 0
    
    if not cart:
        return jsonify({'message': 'Cart is empty!'}), 400

    items_to_remove = []
    for item in cart:
        product = Product.query.get(item.product_id)
        total += product.price
        items_to_remove.append(item)
    
    if total == 0:
        return jsonify({'message': 'Cart is empty!'}), 400

    for item in items_to_remove:
        db.session.delete(item)
    
    db.session.commit()
    
    return jsonify({'message': f'Checkout successful! Total: {total}'}), 200


if __name__ == '__main__':
    app.run(debug=True)