from app import db


class User(db.Model):
    username = db.Column(db.String(120), unique=True, nullable=False, primary_key=True)
    phonenumber = db.Column(db.String(11), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    orders = db.relationship('Order', backref='user', lazy=True)

    @property
    def serialize(self):
        return {
            'username'      : self.username,
            'phonenumber'   : self.phonenumber,
            'is_admin'      : self.is_admin,
            'orders'        : self.serialize_orders
        }

    @property
    def serialize_orders(self):
        return [item.serialize for item in self.orders]
