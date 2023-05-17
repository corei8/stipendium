from xhtml2pdf import pisa
import re
from datetime import datetime
import sys


output_filename="./tmp/test.pdf"

def wrap_tag(tag: str, inner, css_class="") -> str:
    """Convert input to string and wrap in html tag, including classes."""
    return "<"+tag+" class=\""+css_class+"\">"+str(inner)+"</"+tag+">"

def human_date(to_convert):
    """Convert datetime to month dd, yyy"""
    try:
        return datetime.strftime(to_convert, "%b %d, %Y")
    except TypeError:
        return "&mdash;"

def generate_stipends(place, table, num):
    stipends = table.query()
    # order by date
    # order by place
    # add stipends according to number
    return portion

def make_grey(index: int, css_class_1: str, css_class_2: str):
    if index%2 == 0:
        return css_class_1
    else:
        return css_class_2

def html_headings():
    return wrap_tag("thead",
            wrap_tag("th", "Intention", css_class="w-150")+\
            wrap_tag("th", "Requested By", css_class="w-125")+\
            wrap_tag("th", "Requested Date", css_class="w-100")+\
            wrap_tag("th", "#", css_class="w-025")+\
            wrap_tag("th", "Taken By", css_class="w-150")+\
            wrap_tag("th", "mm-dd-yyyy", css_class="w-100")
            )

def build_printable_html(table):
    """Render HTML table as PDF"""
    base = table.query.all() # NOTE: this is temporary
    headings = html_headings()
    with open('./stipendium/stipend_utils/html/template.html', 'r') as f:
        content, combined, i = [], "", 1
        for entry in base:
            gray_row = make_grey(i, "grey center", " center")
            content.append([
                wrap_tag("td", entry.intention, css_class=gray_row),
                wrap_tag("td", entry.requester, css_class=gray_row),
                wrap_tag("td", human_date(entry.req_date), css_class=gray_row),
                wrap_tag("td", entry.masses, css_class=gray_row+" br-right"),
                wrap_tag("td", "", css_class=gray_row),
                wrap_tag("td", "", css_class=gray_row),
                ])
            i+=1
        complete_content = ""
        for row in content:
            for item in row:
                combined += item
            gray_row = make_grey(i, "grey-row", "")
            complete_content += wrap_tag("tr", combined, css_class=gray_row)
            combined = ""
            i+=1
        total = headings+wrap_tag("tbody", complete_content)
        added_header = re.sub('<% HEADER %>', 'Brooksville', f.read())
        return re.sub('<% CONTENT %>', total, added_header)


def convert_html_to_pdf(source_html, output_filename):
    result_file = open(output_filename, 'w+b')
    pisa_status = pisa.CreatePDF(
            source_html,
            dest=result_file
            )
    result_file.close()
    return pisa_status.err
