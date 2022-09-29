from xhtml2pdf import pisa
from datetime import datetime 


output_filename="./tmp/test.pdf"

def wrap_tag(inner: str, tag: str, class="": str) -> str:
    """Convert input to string and wrap in html tag, including classes."""
    return "<"+tag+" class=\""+class+"\">"+str(inner)+"</"+tag+">"

def build_printable_html(table):
    """Render HTML table as PDF"""
    base = table.query.all()
    style = '<link href="https://cdn.jsdelivr.net\
            /npm/bootstrap@5.0.2/dist/css/bootstr\
            ap.min.css" rel="stylesheet" integrit\
            y="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9\
            Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC\
            " crossorigin="anonymous">'
    content = []
    for entry in base:
        try:
            requested_date = datetime.strftime(entry.req_date, "%b %d, %Y")
        except TypeError:
            requested_date = "&mdash;"
        intention = wrap_tag(entry.intention, "td")
        requester = wrap_tag(entry.requester, "td")
        req_date  = wrap_tag(requested_date, "td")
        number    = wrap_tag(entry.masses, "td")
        content.append([
            intention, requester, req_date, number
            ])
        headings = (
                "Intention",
                "Requested By",
                "Requested Date",
                "Number",
                "Taken By",
                "Date Taken",
                )
        headers = ""
    for header in headings:
        headers += wrap_tag(header, "th")
    start = '''
        <table class="table table-striped">
        <thead class="thead-dark">
        '''
    middle = '''
        </thead>
        <tbody>
        '''
    end = '''
        </tbody>
        </table>
        '''
    complete_content = ""
    for row in content:
        combined = ""
        for item in row:
            combined += item
        complete_content += wrap_tag(combined, "tr")
    complete = start+wrap_tag(headers, "tr")+middle+complete_content+end
    return complete


def convert_html_to_pdf(source_html, output_filename):
    result_file = open(output_filename, 'w+b')
    pisa_status = pisa.CreatePDF(
            source_html,
            dest=result_file
            )
    result_file.close()
    return pisa_status.err

