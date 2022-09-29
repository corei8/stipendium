from stipendium import app
from flask import (
        Flask, request, render_template, 
        url_for, flash, redirect, make_response
        )

from stipendium.forms import StipendForm 
from stipendium.models import Stipend
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

@app.route('/print', methods=['GET'])
def print_book():
    output.convert_html_to_pdf(
            output.build_printable_html(Stipend),
            "./stipendium/tmp/test.pdf"
            )
    stipends = Stipend.query.all()
    return render_template(
            'print_book.html',
            stipends=stipends,
            title='Print',
            print='active'
            )
