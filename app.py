# Import libraries
from flask import Flask, request, url_for, redirect, render_template

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation
@app.route("/", methods=["GET"])
def get_transactions():
    return render_template("transactions.html", transactions=transactions)

# Create operation
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method=="GET":
        return render_template("form.html")
    elif request.method=="POST":
        transaction = {
              'id': len(transactions)+1,
              'date': request.form['date'],
              'amount': float(request.form['amount'])
             }
        transactions.append(transaction)
        return redirect(url_for("get_transactions"))

# Update operation
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    if request.method=="GET":
        for transaction in transactions:
            if transaction["id"]==transaction_id:
                return render_template("edit.html", transaction=transaction)
    elif request.method=="POST":
        date = request.form['date']
        amount = float(request.form['amount'])
        for transaction in transactions:
            if transaction["id"]==transaction_id:
                transaction["date"]=date
                transaction["amount"]=amount
                break
        return redirect(url_for("get_transactions"))
    else:
        return "Transaction not found"

# Delete operation
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    for transaction in transactions:
        if transaction["id"]==transaction_id:
            transactions.remove(transaction)
            break
    return redirect(url_for("get_transactions"))

# Search function
@app.route("/search", methods=["GET", "POST"])
def search_transactions():
    if request.method=="POST":
        min = float(request.form['min_amount'])
        max = float(request.form['max_amount'])
        # Implement with list comprehension: new_list = [expression for transaction in transactions if condition]
        filtered_transactions=[transaction for transaction in transactions if 
            transaction["amount"] >= min and transaction["amount"] <= max]
        return render_template("transactions.html", transactions=filtered_transactions)
    elif request.method=="GET":
        return render_template("search.html")

# Balance function
@app.route("/balance")
def total_balance():
    total_balance=0.0
    for transaction in transactions:
        total_balance += transaction["amount"]
    balance = "Total Balance: {}".format(str(total_balance))
    return render_template("transactions_balance.html", transactions=transactions, balance=balance)

# Run the Flask app
if __name__=="__main__":
    app.run(debug=True)