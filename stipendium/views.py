from stipendium import app, db
from flask import (
        Flask, request, render_template, 
        url_for, flash, redirect, make_response,
        send_file
        )
from stipendium.forms import (
        QueueForm, CenterForm, DeleteForm, LoginForm
        )
from stipendium.models import Queue, Centers, Trash
from stipendium.stipend_utils import output, idifyer
from datetime import datetime, timedelta

# TODO: add flask optimize
# TODO: make default landing page for new users

@app.route('/', methods=['POST', 'GET'])
def log_on():
    # check if there is a database in databases
    form = LoginForm(request.form)
    try:
        users = Users.query.all()
        return render_template(
                'login.html',
                form=form,
                title='Login',
                )
    except:
        db.create_all()
        return render_template(
                'new_user.html',
                form=form,
                title='Login',
                )


@app.route('/add', methods=['POST', 'GET'])
# TODO: return new_instance() if no database
def add_stipend():
    form = QueueForm(request.form)
    stipends = Queue.query.order_by(Queue.id.desc())
    # this is to prevent error for empty bases
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

