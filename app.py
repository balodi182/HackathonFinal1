from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/search_product', methods=['POST'])
def search_product():
    product_name = request.form['product_name']

    # Connect to SQLite database
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    # Execute SELECT query to search for product
    c.execute('''SELECT * FROM stock JOIN Shop ON Shop.ShopID = stock.ShopID WHERE stock.Name=?''', (product_name,))
    
    shop_info = c.fetchall()
    # Close database connection
    conn.close()

    if shop_info:
        return render_template('shop_info.html', shop_info=shop_info)
    else:
        return render_template('index1.html')

if __name__ == '__main__':
    app.run(debug=True)
