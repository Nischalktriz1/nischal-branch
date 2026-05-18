from flask import Flask, render_template

app = Flask(__name__)

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

@app.route('/')
def wallet():
    return render_template('wallet.html', transactions=transactions, linked_accounts=linked_accounts)

@app.route('/add-money')
def add_money():
    return render_template('add_money.html', linked_accounts=linked_accounts)

@app.route('/withdraw-money')
def withdraw_money():
    return render_template('withdraw_money.html', linked_accounts=linked_accounts)

@app.route('/linked-accounts')
def linked_accounts():
    return render_template('linked_accounts.html', linked_accounts=linked_accounts)

@app.route('/wallet-summary')
def wallet_summary():
    return render_template('wallet_summary.html', transactions=transactions)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
