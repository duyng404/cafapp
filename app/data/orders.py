from app import db
from app.data.user import User


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d"), value.strftime("%H:%M:%S")]


order_menu = db.Table('order_menu',
                      db.Column('id', db.Integer, primary_key=True),
                      db.Column('order_id', db.Integer, db.ForeignKey('order.id')),
                      db.Column('menu_id', db.Integer, db.ForeignKey('menu.id'))
                     )


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Integer)
    destination = db.Column(db.String(50), nullable=False)
    contents = db.relationship('Menu', secondary=order_menu, lazy='subquery',
                               backref=db.backref('orders', lazy=True))
    owner = db.Column(db.String(120), db.ForeignKey('user.username'), nullable=False)

    @property
    def serialize(self):
        return {
            'id'        : self.id,
            'created'   : dump_datetime(self.created),
            'owner'     : self.owner,
            'contents'  : [item.name for item in self.contents]
        }


class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))
    price = db.Column(db.Numeric)

    @property
    def serialize(self):
        return {
            'id'          : self.id,
            'name'        : self.name,
            'description' : self.description,
            'price'       : self.price
        }
