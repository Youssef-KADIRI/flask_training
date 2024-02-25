from pharmacies import app, db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    phone = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    hashed_password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, first_name, last_name, gender, birth_date, phone, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.birth_date = birth_date
        self.phone = phone
        self.email = email
        self.hashed_password = self.hash_password(password)
        self.is_admin = False

    def hash_password(self, plain_password):
        return bcrypt.generate_password_hash(plain_password).decode('utf-8')

    def check_password(self, plain_password):
        return bcrypt.check_password_hash(self.hashed_password, plain_password)

    def __str__(self):
        return f'User({self.first_name}, {self.last_name}, {self.gender}, {self.birth_date}, {self.email}, {self.hashed_password})'


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    areas = db.relationship('Area', backref='city', lazy=True)

    def __init__(self, name):
        self.name = name


class Area(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)

    def __init__(self, name, city_id):
        self.name = name
        self.city_id = city_id


with app.app_context():
    db.create_all()
