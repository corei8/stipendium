from xhtml2pdf import pisa
from datetime import datetime 


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
    css = """
    @page {
            size: letter;
            margin: 1in;
            }
    """
    head = wrap_tag("head", wrap_tag("style", css))
    content = []
    for entry in base:
        intention = wrap_tag("td", entry.intention)
        requester = wrap_tag("td", entry.requester)
        req_date  = wrap_tag("td", human_date(entry.req_date))
        number    = wrap_tag("td", entry.masses)
        content.append([
            intention, requester, req_date, number
            ])
        headings = (
                "Intention", "Requested By",
                "Requested Date", "Number",
                "Taken By", "Date Taken",
                )
        headers = ""
    for header in headings:
        headers += wrap_tag("th", header)
    complete_content = ""
    for row in content:
        combined = ""
        for item in row:
            combined += item
        complete_content += wrap_tag("tr", combined)
    wrapped_headers = wrap_tag("thead",headers, css_class="")
    return wrap_tag(
            "html",
            head+wrap_tag(
                "table", 
                wrapped_headers+complete_content, 
                css_class="table table-striped"
                )
            )


def convert_html_to_pdf(source_html, output_filename):
    result_file = open(output_filename, 'w+b')
    pisa_status = pisa.CreatePDF(
            source_html,
            dest=result_file
            )
    result_file.close()
    return pisa_status.err

