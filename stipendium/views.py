from stipendium import app, db 
from flask import (
        request, render_template, url_for,
        redirect, send_file
        ) 
from stipendium.models import (
        Queue, Center, Trash, Priest, PersonalQueue
        )
from stipendium.forms import (
        PriestForm, QueueForm, CenterForm, DeleteForm
        )
from stipendium.stipend_utils import output
from datetime import datetime, timedelta
import csv, os
from sqlalchemy import and_
from wtforms import SelectField

with app.test_request_context():
    db.create_all()

# otherwise the tables will not exist
from stipendium.stipend_utils import assigner


@app.route('/', methods=['POST', 'GET'])
def login(): # TODO: make another route for adding a user
    return redirect(url_for('add_stipend'))


@app.route('/add', methods=['POST', 'GET'])
def add_stipend():
    form = QueueForm(request.form)
    priests = Priest.query.order_by(Priest.id.desc())
    priest_to_choose = [(priest.id, priest.lastname) for priest in priests]
    form.priest_asked.choices = priest_to_choose
    priest_to_choose.insert(0, (0, ''))
    stipends = Queue.query.filter(Queue.personal == False).order_by(
            Queue.id.desc()
            )
    try:
        len_queue = stipends[0]['id']
    except:
        len_queue = 0
    if request.method == 'POST' and form.validate():
        submit_date = ''
        if form.submitted.data == None:
            submit_date = datetime.today()
        else:
            submit_date = form.submitted.data
        stipend = Queue(
                intention = form.intention.data,
                dead      = form.dead.data,
                requester = form.requester.data,
                priest    = form.priest_asked.data,
                origin    = form.origin.data,
                accepted  = submit_date,
                req_date  = form.req_date.data,
                amount    = form.amount.data,
                masses    = form.masses.data,
                personal  = False,
                )
        db.session.add(stipend)
        db.session.commit()
        return redirect(url_for('add_stipend'))
    return render_template(
            'add_stipend.html',
            heading="Add Stipend",
            form=form,
            stipends=stipends[0:5],
            len_queue=len_queue,
            title='Add Queue',
            )

@app.route('/priest/add', methods=['POST', 'GET'])
# TODO change "priest" in this context to the name of the user
def add_personal_stipend():
    form = QueueForm(request.form)
    priests = Priest.query.order_by(Priest.id.desc())
    priest_to_choose = [(priest.id, priest.lastname) for priest in priests]
    form.priest_asked.choices = priest_to_choose
    # stipends = Queue.query.order_by(Queue.id.desc())
    stipends = Queue.query.filter(Queue.personal == True)
    try:
        len_queue = stipends[0]['id']
    except:
        len_queue = 0
    if request.method == 'POST' and form.validate():
        submit_date = ''
        if form.submitted.data == None:
            submit_date = datetime.today()
        else:
            submit_date = form.submitted.data
        stipend = Queue(
                intention = form.intention.data,
                dead      = form.dead.data,
                requester = form.requester.data,
                priest    = form.priest_asked.data,
                origin    = form.origin.data,
                accepted  = submit_date,
                req_date  = form.req_date.data,
                amount    = form.amount.data,
                masses    = form.masses.data,
                personal  = True,
                )
        db.session.add(stipend)
        db.session.commit()
        return redirect(url_for('add_personal_stipend'))
    return render_template(
            'add_stipend.html',
            heading="Add Personal Stipend",
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
                stipend_id   = stipend.id,
                intention    = stipend.intention,
                dead         = stipend.dead,
                requester    = stipend.requester,
                priest_asked = stipend.priest,
                origin       = stipend.origin,
                accepted     = stipend.accepted,
                req_date     = stipend.req_date,
                amount       = stipend.amount,
                masses       = stipend.masses,
                trashed      = datetime.now(),
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


@app.route('/edit/stipend/stipendID=<stipend_id>', methods=['GET', 'POST'])
def edit_stipend_by_id(stipend_id):
    stipend = Queue.query.filter_by(id=stipend_id).first()
    form = QueueForm(
            intention    = stipend.intention,
            dead         = stipend.dead,
            requester    = stipend.requester,
            priest_asked = stipend.priest,
            origin       = stipend.origin,
            submitted    = stipend.accepted,
            req_date     = stipend.req_date,
            amount       = stipend.amount,
            masses       = stipend.masses
            )
    edited_form = QueueForm(request.form)
    if request.method == 'POST' and edited_form.validate():
        Queue.query.filter_by(id=stipend_id).update(
                {
                    'intention' : edited_form.intention.data,
                    'dead'      : edited_form.dead.data,
                    'requester' : edited_form.requester.data,
                    'priest'    : edited_form.priest_asked.data,
                    'origin'    : edited_form.origin.data,
                    'accepted'  : edited_form.submitted.data,
                    'req_date'  : edited_form.req_date.data,
                    'amount'    : edited_form.amount.data,
                    'masses'    : edited_form.masses.data,
                    }
                )
        db.session.commit()
        return redirect(url_for('edit_stipends'))
    return render_template(
            'edit_single_stipend.html',
            form=form,
            title='Edit',
            ) 


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    center_form = CenterForm(request.form)
    centers = Center.query.all()
    # intentions_count = lambda x: x*30
    centers_to_choose = [(cntr.id, cntr.name) for cntr in centers]
    priest_form = PriestForm(request.form)
    priest_form.center.choices = centers_to_choose
    if not request.method == 'POST':
        pass
    elif center_form.data and center_form.validate():
        center = Center(
                name    = center_form.name.data,
                address = center_form.address.data,
                city    = center_form.city.data,
                state   = center_form.state.data,
                country = center_form.country.data,
                )
        db.session.add(center)
        db.session.commit()
        return redirect(url_for('settings'))
    elif priest_form.data and priest_form.validate():
        add_priest = Priest(
                firstname = priest_form.firstname.data,
                lastname  = priest_form.lastname.data,
                rank      = priest_form.rank.data,
                center    = priest_form.center.data,
                )
        db.session.add(add_priest)
        db.session.commit()
        return redirect(url_for('settings'))
    return render_template(
            'settings.html',
            center_form = center_form,
            priest_form = priest_form,
            title='Settings',
            )


@app.route('/print', methods=['GET'])
def print_book():
    return render_template(
            'print_book.html',
            title='Print',
            )


# TODO make this infinite. That means Javascript 😲
@app.route('/calendar', methods=['GET'])
def cal_view():

    def build_calendar() -> str:
        end, total, count = 52, [], 0 # a year of stipends
        for i in range(0, end):
            total.append(['','','','','','',''])
            d = 0
            while d <= 6:
                new_date = datetime.today()+timedelta(days=(i*7)+count)
                if int(new_date.strftime('%w')) != d:
                    d = int(new_date.strftime('%w'))
                total[i][d] = [new_date.strftime("%a, %b %d, '%-y"), '']
                d += 1
                count += 1
        return total

    def prep_stipends() -> list:
        events = Queue.query.order_by(Queue.req_date.desc())
        ready_events = [
                [
                    stpd.intention, 
                    stpd.req_date.strftime("%a, %b %d, '%-y")
                    ] for stpd in events
                ]
        return ready_events

    return render_template(
            'calendar_view.html',
            title='Calendar',
            events=prep_stipends(),
            calendar=build_calendar()
            )


@app.route('/download_csv', methods=['GET', 'POST'])
# NOTE this is only temporary
def download_csv():
    stipends = Queue.query.order_by(Queue.id.desc())
    csv_file = 'downloads/backup.csv'
    #! there might be a more efficient way for this
    if not os.path.exists(csv_file):
        with open('stipendium/downloads/backup.csv', 'w'): pass
    with open('stipendium/downloads/backup.csv', 'w') as csv_target:
        filewriter = csv.writer(csv_target, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for entry in stipends:
            filewriter.writerow([
                entry.id,
                entry.intention,
                entry.dead,
                entry.requester,
                entry.priest,
                entry.origin,
                entry.accepted,
                entry.req_date,
                entry.amount,
                entry.masses,
                ])
    return send_file(csv_file, as_attachment=True)

@app.route('/download_db', methods=['GET', 'POST'])
def download_db():
    return send_file('/databases/book.db', as_attachment=True)

@app.route('/print/<target>/<num>', methods=['GET', 'POST'])
def download_pdf(target, num):
    output.convert_html_to_pdf(
            output.build_printable_html(Queue),
            "./stipendium/tmp/"+target+".pdf"
            )
    return send_file("./tmp/"+target+".pdf", as_attachment=True)

