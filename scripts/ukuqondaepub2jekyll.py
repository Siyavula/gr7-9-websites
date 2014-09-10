import sys
import os

from lxml import etree

#
# For every xhtml file in the current folder, transform it into the jekyll
# format # i.e. everything in <body> must go into a jekyll template, that is in
# the current folder


def addBootstrapClasses(html):
    ''' Add the necessary bootstrap elements to the given etree tree'''

    # add bootstrap class to note divs
    for note in html.findall('.//{http://www.w3.org/1999/xhtml}div[@class="note"]'):
        if note.attrib['data-type'] in ['newwords', 'takenote', 'visit', 'didyouknow']:
            note.attrib['class'] += ' col-md-6'
        else:
            note.attrib['class'] += ' col-md-10'

    return html


def writeTOC():
    ''' create the toc from the epub version'''

    tocfile = [f for f in os.listdir(os.curdir) if '.nav' in f and '.xhtml' in f][0]

    # find the TOC, it has id="toc"
    ID = None
    for element in etree.XML(open(tocfile, 'r').read()).iter():
        if 'id' in element.attrib:
            if element.attrib['id'] == 'toc':
                ID = element[0]
                break
    # replace xhtml links with html
    print ID.nsmap
    for a in element.findall('.//{%s}a' % ID.nsmap[None]):
        a.attrib['href'] = a.attrib['href'].replace('xhtml', 'html')

    # remove the first li since it contains the frontmatter entry
    ID.remove(ID[0])
    template = open(sys.argv[1], 'r').read()
    template += '<div class="container">'
    template += '<div id="contents" class="col-md-12 main-content">'
    template += etree.tostring(ID, pretty_print=True)
    template = template.replace('xmlns="http://www.w3.org/1999/xhtml"', '')
    template += "</div></div>"

    with open('tableofcontents.html', 'w') as f:
        f.write(template)


def split_chapters(body):
    '''body: etree element containing <body> tag

    returns list containing chapter content
    '''
    chapters = []


    # clean up the title text a bit
    for heading in ['h1', 'h2', 'h3']:
        for h1 in body.findall('.//{http://www.w3.org/1999/xhtml}{}'.format(heading)):
            title_text = ' '.join([t.strip() for t in h1.itertext()]).strip()
            title_text = ' '.join([t.strip() for t in title_text.split()])
            while title_text[0].isdigit():
                title_text = title_text[1:].strip()

            for child in h1:
                h1.remove(child)
                h1.text = title_text

    # split into chapters
    for h1 in body.findall('.//{http://www.w3.org/1999/xhtml}h1'):
        thischapter = []
        thischapter.append(h1)

        # go through the siblings until another h1 is found
        for h1sibling in h1.itersiblings():
            if h1sibling.tag == '{http://www.w3.org/1999/xhtml}h1':
                break
            thischapter.append(h1sibling)
        chapters.append(thischapter)

    return chapters


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: %s template-name title" % sys.argv[0])
        sys.exit(1)

    xhtmlfiles = [f for f in os.listdir(os.curdir) if f.endswith('.xhtml')]

    for xhtml in xhtmlfiles:
        prog, template_name, title = sys.argv
        template = '''---\nlayout: {}\ntitle:{}\n---\n'''.format(template_name, title)
        template += '<div class="container">\n'
        template += '  <div id="contents" class="col-md-12 main-content">'
        html = etree.XML(open(xhtml, 'r').read())

        body = html.find('.//{http://www.w3.org/1999/xhtml}body')
        chapters = split_chapters(body)

        for number, chapter in enumerate(chapters):
            with open('{:02d}-{}.html'.format(number+1, '-'.join(title.lower().split())), 'w') as outputfile:
                for content in chapter:
                    outputfile.write(etree.tostring(content, encoding='utf-8'))


#       for bodychild in body:
#           template += etree.tostring(bodychild, method='xml')
#       template = template.replace('xmlns="http://www.w3.org/1999/xhtml"', '')
        template += "\n  </div>\n</div>"
        print(template)
#       with open(xhtml.replace('.xhtml', '-test.html'), 'w') as output:
#           output.write(template.encode('utf-8'))

#   writeTOC()
