from stipendium import app, db
from flask import (
        Flask, request, render_template, 
        url_for, flash, redirect, make_response,
        send_file
        )
from stipendium.forms import StipendForm, CenterForm
from stipendium.models import Stipend, Centers
from stipendium.stipend_utils import output, idifyer
from datetime import datetime, timedelta

# TODO: add flask optimize


@app.route('/', methods=['POST', 'GET'])
def add_stipend():
    form = StipendForm(request.form)
    stipends = Stipend.query.order_by(Stipend.id.desc())
    # this is to prevent error for empty bases
    try:
        len_queue = stipends[0]['id']
    except:
        len_queue = 0
    if request.method == 'POST' and form.validate():
        stipend = Stipend(
                intention    = form.intention.data,
                requester    = form.requester.data,
                priest_asked = form.priest_asked.data,
                origin       = form.origin.data,
                accepted     = datetime.today(),
                req_date     = form.req_date.data,
                amount       = form.amount.data,
                masses       = form.masses.data,
                closed       = None,
                )
        db.session.add(stipend)
        db.session.commit()
        return redirect(url_for('add_stipend'))
    return render_template(
            'add_stipend.html',
            form=form,
            stipends=stipends,
            len_queue=len_queue,
            title='Add Stipend',
            add='active'
            )

# @app.route('/stipends', methods=['GET'])
# def stipends():
    # stipends = Stipend.query.all()
    # return render_template(
            # 'stipends.html',
            # stipends=stipends,
            # title='Stipend List',
            # view='active'
            # )

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
            settings='active'
            )

@app.route('/print', methods=['GET'])
def print_book():
    return render_template(
            'print_book.html',
            title='Print',
            print='active'
            )


@app.route('/calendar', methods=['GET'])
def cal_view():
    def build_calendar() -> str:
        end, total, count = 17, [], 0
        for i in range(0, end):
            total.append(['','','','','','',''])
            # TODO: make a border between months
            d = 0
            while d <= 6:
                new_date = datetime.today()+timedelta(days=(i*7)+count)
                if int(new_date.strftime('%w')) != d:
                    d = int(new_date.strftime('%w'))
                total[i][d] = new_date.strftime('%d')
                d += 1
                count += 1
        return total
    return render_template(
            'calendar_view.html',
            title='Calendar',
            cal='active',
            calendar = build_calendar()
            )


@app.route('/print/<target>/<num>', methods=['GET', 'POST'])
def download_pdf(target, num):
    output.convert_html_to_pdf(
            output.build_printable_html(Stipend),
            "./stipendium/tmp/"+target+".pdf"
            )
    return send_file("./tmp/"+target+".pdf", as_attachment=True)

