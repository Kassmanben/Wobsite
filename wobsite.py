import random
import flask as f
from flask_sslify import SSLify
from flask import Flask, request, render_template
import phone
import login_tools

app = Flask(__name__)
#sslify = SSLify(app)
app.secret_key = str(random.random() + random.random())
app.url_map.strict_slashes = False
login_tools.sql.make_database()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/<string:page_name>/')
def static_page(page_name):
    return render_template('static/%s.html' % page_name)


@app.route('/get-estimate-or-apply')
@app.route('/products')
@app.route('/products/<product>')
def products(product=''):
    if product == '':
        return render_template('products.html')
    return render_template('products/{}.html'.format(product ))



@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        name = login_tools.get_username(f.session)
        if name == False:
            return render_template('login/login.html')
        if name != False:
            return logout()
        
    if request.method == 'POST':
        return login_tools.login_url(request, f.session)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    if request.method == 'POST':
        try:
            del f.session['username']
        except KeyError:
            pass
        return home()
    if request.method == 'GET':
        return render_template('login/logout.html')

#------------------------------PHONE SYSTEM----------------------#

@app.route('/ivr')
def ivr():
    return phone.ivr(request)

@app.route('/call_router/', methods = ['GET', 'POST'])
def call_router():
    return phone.call_router(request)
    
if __name__ == "__main__":
    app.run()