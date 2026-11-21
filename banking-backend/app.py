import os
from decimal import Decimal, InvalidOperation
from flask import Flask, flash, redirect, render_template, request, session, url_for
from pymongo import MongoClient
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_prefix=1)
app.secret_key = os.environ['FLASK_SECRET_KEY']
client = MongoClient(os.environ.get('MONGO_URI', 'mongodb://localhost:27017/bank_app'))
db = client.get_default_database()
users = db.users
transactions = db.transactions
users.create_index('email', unique=True)


def amount_in_cents(value):
    try:
        amount = Decimal(value)
        if not amount.is_finite() or amount <= 0 or amount.as_tuple().exponent < -2:
            return None
        return int(amount * 100)
    except (InvalidOperation, TypeError, ValueError):
        return None


@app.route('/')
def home():
    return redirect(url_for('dashboard' if 'email' in session else 'login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        if not name or '@' not in email or len(password) < 8:
            flash('Enter a name, valid email, and password of at least 8 characters')
        elif users.find_one({'email': email}):
            flash('This email is already registered')
        else:
            users.insert_one({'name': name, 'email': email, 'password_hash': generate_password_hash(password), 'balance_cents': 0})
            flash('Registration successful. Please log in')
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        user = users.find_one({'email': email})
        if user and check_password_hash(user['password_hash'], request.form.get('password', '')):
            session.clear()
            session['email'] = email
            return redirect(url_for('dashboard'))
        flash('Invalid email or password')
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        return redirect(url_for('login'))
    user = users.find_one({'email': session['email']})
    if not user:
        session.clear()
        return redirect(url_for('login'))
    return render_template('dashboard.html', name=user['name'], balance=f"{user['balance_cents'] / 100:.2f}")


@app.route('/deposit', methods=['POST'])
def deposit():
    if 'email' not in session:
        return redirect(url_for('login'))
    cents = amount_in_cents(request.form.get('amount'))
    if cents is None:
        flash('Enter a positive amount with up to two decimal places')
    else:
        users.update_one({'email': session['email']}, {'$inc': {'balance_cents': cents}})
        transactions.insert_one({'email': session['email'], 'type': 'deposit', 'amount_cents': cents, 'created_at': __import__('datetime').datetime.now(__import__('datetime').timezone.utc)})
        flash('Deposit successful')
    return redirect(url_for('dashboard'))


@app.route('/withdraw', methods=['POST'])
def withdraw():
    if 'email' not in session:
        return redirect(url_for('login'))
    cents = amount_in_cents(request.form.get('amount'))
    if cents is None:
        flash('Enter a positive amount with up to two decimal places')
    elif users.update_one({'email': session['email'], 'balance_cents': {'$gte': cents}}, {'$inc': {'balance_cents': -cents}}).modified_count:
        transactions.insert_one({'email': session['email'], 'type': 'withdrawal', 'amount_cents': cents, 'created_at': __import__('datetime').datetime.now(__import__('datetime').timezone.utc)})
        flash('Withdrawal successful')
    else:
        flash('Insufficient balance')
    return redirect(url_for('dashboard'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
