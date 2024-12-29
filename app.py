from flask import Flask, render_template, request, redirect, url_for
import csv
import os

app = Flask(__name__)

# Define the path to the CSV file
PORTFOLIO_FILE = 'portfolio.csv'

# Function to read the portfolio data from the CSV file
def get_portfolio_data():
    portfolio = []
    if os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                asset = {
                    'name': row[0],
                    'type': row[1],
                    'amount': float(row[2]),
                    'cost_price': float(row[3]),
                    'current_price': float(row[4]),
                }
                portfolio.append(asset)
    return portfolio

# Function to update the portfolio data in the CSV file
def update_portfolio_data(portfolio):
    with open(PORTFOLIO_FILE, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'type', 'amount', 'cost_price', 'current_price'])  # Write header
        for asset in portfolio:
            writer.writerow([asset['name'], asset['type'], asset['amount'], asset['cost_price'], asset['current_price']])

# Function to calculate total investment and profit/loss
def calculate_totals(portfolio):
    total_invested = 0
    total_value = 0
    total_profit_loss = 0
    for asset in portfolio:
        total_invested += asset['amount'] * asset['cost_price']
        total_value += asset['amount'] * asset['current_price']
        total_profit_loss += (asset['current_price'] - asset['cost_price']) * asset['amount']
    
    return total_invested, total_value, total_profit_loss

# Home route: Display the portfolio, total investment, and profit/loss
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'add_asset' in request.form:
            # Add a new asset to the portfolio
            new_asset = {
                'name': request.form['new_name'],
                'type': request.form['new_type'],
                'amount': float(request.form['new_amount']),
                'cost_price': float(request.form['new_cost_price']),
                'current_price': float(request.form['new_current_price']),
            }
            portfolio = get_portfolio_data()
            portfolio.append(new_asset)
            update_portfolio_data(portfolio)
            return redirect(url_for('index'))  # Redirect to reload data

        # Collect the updated portfolio data from the form (for editing existing data)
        updated_portfolio = []
        for i in range(len(request.form.getlist('name'))):
            updated_portfolio.append({
                'name': request.form.getlist('name')[i],
                'type': request.form.getlist('type')[i],
                'amount': float(request.form.getlist('amount')[i]),
                'cost_price': float(request.form.getlist('cost_price')[i]),
                'current_price': float(request.form.getlist('current_price')[i])
            })
        
        # Update the CSV file with new data
        update_portfolio_data(updated_portfolio)
        return redirect(url_for('index'))  # Redirect to the same page to reload updated data

    # Get the portfolio data to display
    portfolio = get_portfolio_data()

    # Calculate totals (total invested, total value, profit/loss)
    total_invested, total_value, total_profit_loss = calculate_totals(portfolio)
    
    return render_template('index.html', portfolio=portfolio, 
                           total_invested=total_invested, total_value=total_value, 
                           total_profit_loss=total_profit_loss)

if __name__ == '__main__':
    app.run(debug=True)
