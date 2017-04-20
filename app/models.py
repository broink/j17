from app import db

from flask import jsonify, url_for

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(128))
    cafe = db.Column(db.Integer)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(128))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


    def __repr__(self):
        return '<User %r>' % (self.username)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    added_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp_added = db.Column(db.DateTime)
    name = db.Column(db.String(128))
    descr = db.Column(db.Text)
    price = db.Column(db.Integer)
    picture = db.Column(db.BLOB)
    active = db.Column(db.Boolean)

    def __repr__(self):
        return '<Product %r>' % (self.name)

    def to_json(self):
        return jsonify({
            'name': self.name,
            'price': self.price,
            'picture_url': str(url_for('get_product_photo', id=self.id))
        })

class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    products = db.Column(db.Integer, db.ForeignKey('product.id'))

    def __repr__(self):
        return '<Cafe %r>' % (self.name)
