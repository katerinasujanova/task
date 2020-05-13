from flask import Flask, render_template
from flask_bootstrap import Bootstrap 
import scraper

app = Flask(__name__, template_folder='templates')
Bootstrap(app)

@app.route('/')
def index():
    return render_template(
        'index.html'
    )

@app.route('/products', methods=["GET", "POST"])
def products():
    data = scraper.get_data(description=False)
    return render_template(
        'products.html',
        data=data
    )

@app.route('/products/<phone_id>', methods=["GET", "POST"])
def phone(phone_id):
    data = scraper.get_phone_data(phone_id)
    return render_template(
        'phone.html',
        data=data
    )

if __name__ == '__main__':
    app.run(debug=True)