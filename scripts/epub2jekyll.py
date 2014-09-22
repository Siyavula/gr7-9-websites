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
    for a in element.findall('.//{%s}a'%ID.nsmap[None]):
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




if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: %s template" % sys.argv[0])
        sys.exit(1)

    xhtmlfiles = [f for f in os.listdir(os.curdir) if f.endswith('.xhtml')]

    for xhtml in xhtmlfiles:
        template = open(sys.argv[1], 'r').read()
        strands = {'eb':'earthandbeyond', 'ec':'energyandchange',
                   'll':'lifeandliving', 'mm':'matterandmaterials'}

        strand = None
        for key in strands.keys():
            if key in xhtml:
                strand = strands[key]

        if not strand:
            strand = ''

        template += '<div class="container %s">' % strand
        template += '<div id="contents" class="col-md-12 main-content">'
        html = etree.XML(open(xhtml, 'r').read())
        # html = addBootstrapClasses(html)

        body = html.find('.//{http://www.w3.org/1999/xhtml}body')

        for bodychild in body:
            template += etree.tostring(bodychild, method='xml')
        template = template.replace('xmlns="http://www.w3.org/1999/xhtml"', '')
        template += "</div></div>"
        with open(xhtml.replace('.xhtml', '-test.html') , 'w') as output:
            output.write(template)

    writeTOC()
