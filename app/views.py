import os
import io

from flask import render_template, flash, redirect, session, url_for, request, g, make_response, send_from_directory
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
            try:
                newProduct = Product(
                    name=request.form['name'],
                    #picture=file.stream.getvalue(), #cannot store transparent bytes
                    filename=filename,
                    price=request.form['price'],
                    active=True
                    )
                db.session.add(newProduct)
                db.session.commit()
                cafes = Cafe.query.filter(Cafe.id.in_([int(id) for id in request.form['cafes']])).all()
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(newProduct.id)+filename.split('.')[-1]))
                for cafe in cafes:
                    cafe.addProduct(newProduct)
            except AttributeError:
                flash('No transparancy allowed at the moment')
            return redirect(url_for('new_product'))
    return render_template(
        'product_listing.html',
        products=Product.query.all(),
        cafes=Cafe.query.all()
        )

@app.route('/product_photos/<int:id>')
def get_product_photo(id):
    '''
    Returns image with the provided ID.
    '''
    #picture = Product.query.get_or_404(id).picture
    #response = make_response(picture)
    #response.headers['Content-Type'] = 'image/png'
    #return response
    product = Product.query.get_or_404(id)
    return send_from_directory('/'.join(app.root_path.split('/')[:-1])+'/'+app.config['UPLOAD_FOLDER'], product.filename)

@app.route('/product/<int:id>')
def get_product(id):
    product = Product.query.get_or_404(id)
    return product

@app.route('/edit_product/<int:id>', methods=['GET','POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)

    if request.method == 'POST':
        print(request.form.__dict__)
        if product.name != request.form['name']:
            product.name = request.form['name']
        if 'file' not in request.files:
            print('no file uploaded')
        try:
            file = request.files['file']
        except:
            file = None
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            try:
                os.remove(app.config['UPLOAD_FOLDER'], product.filename)
            except:
                pass
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(id)+filename.split('.')[-1]))
            product.filename =  str(id)+filename.split('.')[-1]
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

@app.route('/delete_product', methods=['POST'])
def delete_product():
    id = int(request.form['delete_id'])
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return render_template(
        'product_listing.html',
        products=Product.query.all(),
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


# API-like functionality
@app.route('/api/cafe/<int:id>')
def api_get_cafe(id):
    cafe = Cafe.query.get_or_404(id)
    return cafe.to_json()

@app.route('/api/product/<int:id>')
def api_get_product(id):
    product = Product.query.get_or_404(id)
    return product.to_json()



