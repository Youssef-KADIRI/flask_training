from pharmacies import app, db
from flask import render_template, redirect, url_for, request, flash
from pharmacies.models import User, City, Area
from pharmacies.forms import (RegisterForm, LoginForm, AddCityForm, EditCityForm,
                              DeleteCityForm, AddAreaForm, EditAreaForm, DeleteAreaForm)
from flask_login import login_user, current_user, logout_user, login_required
from functools import wraps


def admin_required(f):
    @login_required
    @wraps(f)
    def wrap(*args, **kwargs):
        if current_user.is_admin:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('user_page_404'))

    return wrap


def user_required(f):
    @login_required
    @wraps(f)
    def wrap(*args, **kwargs):
        if not current_user.is_admin:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('admin_page_404'))

    return wrap


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        gender = form.gender.data
        birth_date = form.birth_date.data
        phone = form.phone.data
        email = form.email.data
        password = form.password.data
        new_user = User(first_name=first_name,
                        last_name=last_name,
                        gender=gender,
                        birth_date=birth_date,
                        phone=phone,
                        email=email,
                        password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        login_user(user)
        if user.is_admin:
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('user_index'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@admin_required
def dashboard():
    number_of_cities = City.query.count()
    number_of_areas = Area.query.count()
    return render_template('admin/dashboard.html',
                           number_of_cities=number_of_cities,
                           number_of_areas=number_of_areas)


@app.route('/admin/cities', methods=['GET'])
@admin_required
def cities_page():
    add_city_form = AddCityForm()
    edit_city_form = EditCityForm()
    delete_city_form = DeleteCityForm()
    cities = City.query.filter_by().all()
    return render_template('admin/cities.html',
                           add_city_form=add_city_form,
                           edit_city_form=edit_city_form,
                           delete_city_form=delete_city_form,
                           cities=cities)


@app.route('/admin/cities/add', methods=['POST'])
@admin_required
def add_city():
    name = request.form['name']
    city = City(name=name)
    try:
        db.session.add(city)
        db.session.commit()
    except:
        print("Something went wrong")
    return redirect(url_for('cities_page'))


@app.route('/admin/cities/edit/<int:id>', methods=['POST'])
@admin_required
def edit_city(id):
    city = City.query.filter_by(id=id).first()
    name = request.form["name"]
    if city:
        city.name = name
        db.session.commit()
    else:
        print("City not found")
    return redirect(url_for('cities_page'))


@app.route('/admin/cities/delete/<int:id>', methods=['POST'])
@admin_required
def delete_city(id):
    city = City.query.filter_by(id=id).first()
    if city:
        try:
            db.session.delete(city)
            db.session.commit()
        except:
            print("Something went wrong")
    else:
        print('city not found')
    return redirect(url_for('cities_page'))


@app.route('/admin/areas')
@admin_required
def areas_page():
    add_area_form = AddAreaForm()
    edit_area_form = EditAreaForm()
    delete_area_form = DeleteAreaForm()
    areas = Area.query.all()
    cities = City.query.all()
    return render_template('admin/areas.html',
                           add_area_form=add_area_form,
                           edit_area_form=edit_area_form,
                           delete_area_form=delete_area_form,
                           areas=areas,
                           cities=cities)


@app.route('/admin/areas/add', methods=['POST'])
@admin_required
def add_area():
    name = request.form['name']
    city_id = request.form['city_id']
    area = Area(name, city_id)
    try:
        db.session.add(area)
        db.session.commit()
    except:
        print("Something went wrong")
    return redirect(url_for('areas_page'))

@app.route('/admin/areas/edit/<int:id>', methods=['POST'])
@admin_required
def edit_area(id):
    area = Area.query.filter_by(id=id).first()
    name = request.form["name"]
    city_id = request.form["city_id"]
    if area:
        try:
            area.name = name
            area.city_id = city_id
            db.session.commit()
        except:
            print("Something went wrong")
    else:
        print("Area not found")
    return redirect(url_for('areas_page'))


@app.route('/admin/areas/delete/<int:id>', methods=['POST'])
@admin_required
def delete_area(id):
    area = Area.query.filter_by(id=id).first()
    if area:
        db.session.delete(area)
        db.session.commit()
    else:
        print('area not found')
    return redirect(url_for('areas_page'))


@app.route('/admin/404')
@admin_required
def admin_page_404():
    return render_template('admin/404.html')


@app.route('/user')
@user_required
def user_index():
    return render_template('user/index.html')


@app.route('/user/404')
@admin_required
def user_page_404():
    return render_template('admin/404.html')
