from stipendium import app, db
from flask import (
        Flask, request, render_template, 
        url_for, flash, redirect, make_response,
        send_file
        )
from stipendium.forms import (
        QueueForm, CenterForm, DeleteForm, LoginForm, AdduserForm
        )
from stipendium.models import (
        Queue, Centers, Trash, User, Activity
        )
from stipendium.stipend_utils import output, idifyer
from datetime import datetime, timedelta
from flask_login import LoginManager, login_required, login_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

# TODO: add flask-optimize
# TODO: we need to add a user name when logged in
# TODO: make default landing page for new users
# TODO: make activity log work only after there is user in place and after the first login
# TODO: make default login credentials for this, so that the user is "logged in" as admin for his own credential

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
        return User.query.get(int(user_id))


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/', methods=['POST', 'GET'])
def login():
    # form = LoginForm(request.form)
    # activity = Activity.query.all()
    # if request.method == 'POST' and form.validate():
        # user = User.query.filter_by(username=form.username.data).first()
        # if user:
            # if check_password_hash(user.password_hash, form.password.data):
                # login_user(user)
                # return redirect(url_for('add'))
            # else:
                # flash("Password is incorrect.")
        # else:
            # flash("Username or password are incorrect.")
    # flash("Default username is 'admin', and default password is 'iamadmin'.")
    # return render_template(
            # 'login.html',
            # form=form,
            # title='Login',
            # )
    # return redirect(url_for('add_user'))
    return redirect(url_for('add_stipend'))


# @app.route('/user/add', methods=['POST', 'GET'])
# def add_user():
    # form = AdduserForm(request.form)
    # if request.method == 'POST' and form.validate():
        # hashed_pwd = generate_password_hash(form.password.data, "sha256")
        # new_user = User(
                # name = form.name.data,
                # username = form.username.data,
                # password_hash = hashed_pwd,
                # )
        # db.session.add(new_user)
        # db.session.commit()
        # flash("New user has been made.")
        # return redirect(url_for('login'))
    # else:
        # flash("User already exists.")
    # return render_template(
            # 'new_user.html',
            # form=form,
            # title='Login',
            # )


@app.route('/add', methods=['POST', 'GET'])
# @login_required
def add_stipend():
    form = QueueForm(request.form)
    stipends = Queue.query.order_by(Queue.id.desc())
    try:
        len_queue = stipends[0]['id']
    except:
        len_queue = 0
    if request.method == 'POST' and form.validate():
        stipend = Queue(
                intention = form.intention.data,
                requester = form.requester.data,
                priest    = form.priest_asked.data,
                origin    = form.origin.data,
                accepted  = datetime.today(),
                req_date  = form.req_date.data,
                amount    = form.amount.data,
                masses    = form.masses.data,
                closed    = None,
                )
        db.session.add(stipend)
        db.session.commit()
        return redirect(url_for('add_stipend'))
    return render_template(
            'add_stipend.html',
            form=form,
            stipends=stipends[0:5],
            len_queue=len_queue,
            title='Add Queue',
            )


@app.route('/edit', methods=['POST', 'GET'])
def edit_stipends():
    delete_form = DeleteForm(request.form)
    stipends = Queue.query.order_by(Queue.id.desc())
    if request.method == 'POST' and delete_form.validate():
        stipend = Queue.query.filter_by(id=delete_form.id.data).first()
        deleted = Trash(
                stipend_id = stipend.id,
                intention = stipend.intention,
                requester = stipend.requester,
                priest_asked = stipend.priest_asked,
                origin = stipend.origin,
                accepted = stipend.accepted,
                req_date = stipend.req_date,
                amount = stipend.amount,
                masses = stipend.masses,
                trashed = datetime.now(),
                )
        db.session.add(deleted)
        Queue.query.filter_by(id=stipend.id).delete()
        db.session.commit()
        return redirect(url_for('edit_stipends'))
    return render_template(
            'edit_stipends.html',
            delete_form=delete_form,
            stipends=stipends,
            title='Add Queue',
            )


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    centers_form = CenterForm(request.form)
    centers = Centers.query.all()
    intentions_count = lambda x: x*30 # TODO: get this from config file
    if not request.method == 'POST':
        pass
    else:
        if centers_form.data and centers_form.validate():
            center = Centers(
                    # name             = centers_form.name.data.upper(),
                    fullname         = centers_form.fullname.data,
                    priests          = centers_form.priests.data,
                    address          = centers_form.address.data,
                    city             = centers_form.city.data,
                    state            = centers_form.state.data,
                    country          = centers_form.country.data,
                    intentions_count = intentions_count(centers_form.priests.data),
                    )
            db.session.add(center)
            db.session.commit()
            return redirect(url_for('settings'))
    return render_template(
            'settings.html',
            centers_form = centers_form,
            centers = centers,
            title='Settings',
            )


@app.route('/print', methods=['GET'])
def print_book():
    return render_template(
            'print_book.html',
            title='Print',
            )


# Put this on hold for right now:
@app.route('/calendar', methods=['GET'])
def cal_view():
    def build_calendar() -> str:
        end, total, count = 17, [], 0
        for i in range(0, end):
            total.append(['','','','','','',''])
            d = 0
            while d <= 6:
                new_date = datetime.today()+timedelta(days=(i*7)+count)
                if int(new_date.strftime('%w')) != d:
                    d = int(new_date.strftime('%w'))
                # use %-m for month number
                # TODO: make the border between months darker
                total[i][d] = [new_date.strftime('%d'), '']
                d += 1
                count += 1
        return total
    return render_template(
            'calendar_view.html',
            title='Calendar',
            calendar = build_calendar()
            )


@app.route('/print/<target>/<num>', methods=['GET', 'POST'])
def download_pdf(target, num):
    output.convert_html_to_pdf(
            output.build_printable_html(Queue),
            "./stipendium/tmp/"+target+".pdf"
            )
    return send_file("./tmp/"+target+".pdf", as_attachment=True)

