from stipendium import app
from flask import (
        Flask, request, render_template, 
        url_for, flash, redirect, make_response,
        send_file
        )
from stipendium.forms import StipendForm, CenterForm
from stipendium.models import Stipend, Centers
from stipendium.stipend_utils import output



@app.route('/', methods=['POST', 'GET'])
def add_stipend():
    form = StipendForm(request.form)
    if request.method == 'POST' and form.validate():
        stipend = Stipend(
                intention = form.intention.data,
                requester = form.requester.data,
                origin    = form.origin.data,
                accepted  = datetime.today(),
                req_date  = form.req_date.data,
                amount    = form.amount.data,
                masses    = form.masses.data,
                celebrant = '',
                closed    = None,
                )
        db.session.add(stipend)
        db.session.commit()
        return redirect(url_for('add_stipend'))
    return render_template(
            'add_stipend.html',
            form=form,
            title='Add Stipend',
            add='active'
            )

@app.route('/stipends', methods=['GET'])
def stipends():
    stipends = Stipend.query.all()
    return render_template(
            'stipends.html',
            stipends=stipends,
            title='Stipend List',
            view='active'
            )

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    # stipends = Stipend.query.all()
    # centers = Centers.query.all 
    centers_form = CenterForm(request.form)
    return render_template(
            'settings.html',
            # stipends=stipends,
            centers_form = centers_form,
            title='Settings',
            settings='active'
            )

@app.route('/print', methods=['GET'])
def print_book():
    stipends = Stipend.query.all()
    return render_template(
            'print_book.html',
            stipends=stipends,
            title='Print',
            print='active'
            )

@app.route('/print/<target>/<num>', methods=['GET', 'POST'])
def download_pdf(target, num):
    output.convert_html_to_pdf(
            output.build_printable_html(Stipend),
            "./stipendium/tmp/"+target+".pdf"
            )
    return send_file("./tmp/"+target+".pdf", as_attachment=True)

