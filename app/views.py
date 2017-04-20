import os
import io

from flask import render_template, flash, redirect, session, url_for, request, g, make_response
from flask_login import login_user, logout_user, current_user, login_required

from werkzeug import secure_filename

from app import app, db, lm
#from .forms import LoginForm
from .models import User, Product, Cafe

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', cafes=Cafe.query.all())

# Helper function for uploads

def allowed_file(filename):
    print(filename.rsplit('.',1)[1])
    return '.' in filename and filename.rsplit('.',1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/new_product', methods=['GET','POST'])
def new_product():
    if request.method == 'POST':
        print('1')
        file = request.files['file']
        print('2', file.filename)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(file.__dict__)
            try:
                newProduct = Product(
                    name=request.form['name'],
                    picture=file.stream.getvalue(),
                    price=request.form['price'],
                    active=True
                    )
            except AttributeError:
                flash('No transparancy allowed at the moment')
            db.session.add(newProduct)
            db.session.commit()
            cafes = Cafe.query.filter(Cafe.id._in(request.form['cafes'])).all()
            for cafe in cafes:
                cafe.addProduct(newProduct)
            return redirect(url_for('new_product'))
    return render_template(
        'product_listing.html',
        products=Product.query.all(),
        cafes=Cafe.query.all()
        )

@app.route('/product_photos/<int:id>.png')
def get_product_photo(id):
    '''
    Returns image with the provided ID.
    '''
    picture = Product.query.get_or_404(id).picture
    response = make_response(picture)
    response.headers['Content-Type'] = 'image/png'
    return response

@app.route('/product/<int:id>')
def get_product(id):
    product = Product.query.get_or_404(id)
    return product

@app.route('/edit_product/<int:id>', methods=['GET','POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        if product.name != request.form['name']:
            product.name = request.form['name']
        try:
            file = request.files['file']
        except:
            file = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            product.picture = file.stream.getvalue()
        if product.price != request.form['price']:
            product.price = request.form['price']
        if request.form.get('active'):
            product.active = True
        else:
            product.active = False
        db.session.commit()
    return render_template(
        'edit_product.html',
        product=product,
        cafes=Cafe.query.all()
    )

@app.route('/cafe/<int:id>')
def cafe(id=0):
    if id == 0:
        return index()
    else:
        cafe = Cafe.query.filter(Cafe.id == id).first()
        if cafe is None:
            flash('Inget cafe finns med id ' + str(id))
            return index()
        return render_template('display_products.html', cafe=cafe)

@app.route('/cafe/<int:id>/edit', methods=['GET','POST'])
def edit_cafe(id):
    cafe = Cafe.query.filter(Cafe.id == id).first()
    if request.method == 'POST':
        if cafe is None:
            new_cafe = Cafe(name=request.form['name'])
            db.session.add(new_cafe)
            db.session.commit()
            cafe = new_cafe
            id = cafe.id
        else:
            cafe.name = request.form['name']
            db.session.commit()
    return render_template('edit_cafe.html', cafe=cafe, attempted_id=id)
