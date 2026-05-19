from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a secure secret key

# Simple in-memory user database (in production, use a real database)
users_db = {}

# Sample data
transactions = [
    {
        'title': 'Salary Credit',
        'date': 'Today, 9:00 AM',
        'amount': 50000,
        'type': 'credit',
        'icon': 'wallet'
    },
    {
        'title': 'Shopping - Amazon',
        'date': 'Yesterday, 2:30 PM',
        'amount': -2500,
        'type': 'debit',
        'icon': 'shopping-cart'
    },
    {
        'title': 'Transfer to Savings',
        'date': 'May 15, 11:15 AM',
        'amount': -10000,
        'type': 'transfer',
        'icon': 'exchange-alt'
    },
    {
        'title': 'Electricity Bill',
        'date': 'May 14, 4:20 PM',
        'amount': -1500,
        'type': 'debit',
        'icon': 'bolt'
    },
    {
        'title': 'Freelance Payment',
        'date': 'May 13, 3:00 PM',
        'amount': 8000,
        'type': 'credit',
        'icon': 'laptop'
    }
]

linked_accounts = [
    {
        'name': 'Nepal Investment Bank',
        'number': '**** 4521',
        'status': 'verified',
        'icon': 'university'
    },
    {
        'name': 'Global IME Bank',
        'number': '**** 7832',
        'status': 'verified',
        'icon': 'landmark'
    },
    {
        'name': 'Khalti Wallet',
        'number': '**** 9876',
        'status': 'unverified',
        'icon': 'mobile-alt'
    }
]

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users_db:
            if check_password_hash(users_db[username]['password'], password):
                session['user_id'] = username
                flash('Login successful!', 'success')
                return redirect(url_for('wallet'))
            else:
                flash('Invalid password.', 'danger')
        else:
            flash('Username not found.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not password:
            flash('Username and password are required.', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'danger')
            return render_template('register.html')
        
        if username in users_db:
            flash('Username already exists.', 'danger')
            return render_template('register.html')
        
        # Create new user with hashed password
        users_db[username] = {
            'password': generate_password_hash(password)
        }
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/')
@login_required
def wallet():
    return render_template('wallet.html', transactions=transactions, linked_accounts=linked_accounts)

@app.route('/add-money')
@login_required
def add_money():
    return render_template('add_money.html', linked_accounts=linked_accounts)

@app.route('/withdraw-money')
@login_required
def withdraw_money():
    return render_template('withdraw_money.html', linked_accounts=linked_accounts)

@app.route('/linked-accounts')
@login_required
def linked_accounts():
    return render_template('linked_accounts.html', linked_accounts=linked_accounts)

@app.route('/wallet-summary')
@login_required
def wallet_summary():
    return render_template('wallet_summary.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
