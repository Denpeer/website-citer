import sys
import bibtexparser
import lxml.html
from datetime import date
from urllib.parse import urlparse
from urllib.request import urlopen #used to handle https with lxml

def generate_entry(url):
    print(url)
    parsed_html = lxml.html.parse(urlopen(url))
    parsed_uri = urlparse(url)

    author = parsed_uri.netloc
    title = parsed_html.find(".//title").text
    entry = {
        'author': author,
        'title': title[:-2], #title contains newline
        'url': url,
        'note': 'retrieved at ' + date.today().__str__(),
        'ENTRYTYPE': 'MISC',
        'ID': 'webpage:' + author
    }
    return entry

arglen = len(sys.argv)
if (arglen != 2) and (arglen != 3):
    print('Usage: onlineToBib.py <url>\n'
          'OR\n'
          'Usage: onlineToBib.py <inputfile> <outputfile>')
    sys.exit(1)

if (arglen == 2):
    db = bibtexparser.bibdatabase.BibDatabase()
    db.entries = [generate_entry(sys.argv[1])]
    writer = bibtexparser.bwriter.BibTexWriter()
    writer.contents = ['comments', 'entries']
    writer.indent = '  '
    writer.order_entries_by = ('ENTRYTYPE', 'author', 'year')
    print(writer.write(db))
    sys.exit(0)

db = bibtexparser.bibdatabase.BibDatabase()

with open('urls.txt', 'r') as url_file:
    for url in url_file: #file must contain only urls seperated by newlines
        db.entries.append(generate_entry(url[:-1]))


with open('out.bib','w') as bibtex_output_file:
    bibtexparser.dump(db,bibtex_output_file)