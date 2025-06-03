from flask import Flask, render_template, jsonify
from update_logic import update_stock_prices, get_stock_data

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/update')
def update():
    log = update_stock_prices()
    return render_template('index.html')

@app.route('/data')
def data():
    stock_data = get_stock_data()  # This returns a list/dict with current stocks info
    return jsonify(stock_data)

if __name__ == '__main__':
    app.run(debug=False)
