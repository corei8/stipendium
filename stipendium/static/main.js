function printTable() {
    var table = document.getElementById('book');
    var a = window.open('');
    a.document.write(table.outerHTML);
    a.print();
    a.close();
}
