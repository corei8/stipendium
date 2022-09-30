from xhtml2pdf import pisa
import re
from datetime import datetime 
import sys


output_filename="./tmp/test.pdf"

def wrap_tag(tag: str, inner, css_class="") -> str:
    """Convert input to string and wrap in html tag, including classes."""
    return "<"+tag+" class=\""+css_class+"\">"+str(inner)+"</"+tag+">"

def human_date(to_convert):
    """Convert datetime to `Month day, year`"""
    try:
        return datetime.strftime(to_convert, "%b %d, %Y")
    except TypeError:
        return "&mdash;"

def build_printable_html(table):
    """Render HTML table as PDF"""
    base = table.query.all()
    headings = wrap_tag("thead",
            wrap_tag("th", "Intention", css_class="w-150")+\
            wrap_tag("th", "Requested By", css_class="w-125")+\
            wrap_tag("th", "Requested Date", css_class="w-100")+\
            wrap_tag("th", "#", css_class="w-025")+\
            wrap_tag("th", "Taken By", css_class="w-150")+\
            wrap_tag("th", "mm-dd-yyyy", css_class="w-100")
            )
    with open('./stipendium/stipend_utils/html/template.html', 'r') as f:
        content, combined, i = [], "", 1
        for entry in base:
            if i%2 == 0:
                gray_row = "grey center"
            else:
                gray_row = " center"
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
            if i%2 == 0:
                gray_row = "grey-row"
            else:
                gray_row = ""
            complete_content += wrap_tag("tr", combined, css_class=gray_row)
            combined = ""
            i+=1
        total = headings+wrap_tag("tbody", complete_content)
        with open('./stipendium/stipend_utils/html/css/main.css', 'r') as css:
            added_style = re.sub('<% STYLE %>', re.escape(css.read()), f.read())
        added_header = re.sub('<% HEADER %>', 'Brooksville', added_style)
        return re.sub('<% CONTENT %>', total, added_header)


def convert_html_to_pdf(source_html, output_filename):
    result_file = open(output_filename, 'w+b')
    pisa_status = pisa.CreatePDF(
            source_html,
            dest=result_file
            )
    result_file.close()
    return pisa_status.err

