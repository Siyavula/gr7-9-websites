import copy

import docopt
from lxml import etree

#
# For every xhtml file in the current folder, transform it into the jekyll
# format # i.e. everything in <body> must go into a jekyll template, that is in
# the current folder


def split_chapters(body):
    '''body: etree element containing <body> tag

    returns list containing chapter content
    '''
    chapters = []

    # strip comments
    for el in body.iter():
        if not isinstance(el.tag, basestring):
            el.getparent().remove(el)

    # there are some divs in body. Replace them with their children
    for child in body:
        if 'h1' not in child.tag:
            for subchild in child:
                child.addprevious(subchild)
            try:
                assert(child.tail is None)
            except AssertionError:
                assert(child.tail.strip() == '')
            assert(len(child) == 0)
            body.remove(child)

    # clean up the title text a bit
    for heading in ['h1', 'h2', 'h3']:
        for h1 in body.findall('.//{{http://www.w3.org/1999/xhtml}}{}'.format(heading)):
            title_text = ' '.join([t.strip() for t in h1.itertext()]).strip()
            title_text = ' '.join([t.strip() for t in title_text.split()]).strip()

            # strip numbers out of titles
            print
            print(title_text)
            words = title_text.split()
            if any([char.isdigit() for char in words[0]]):
                words = words[1:]

            cleaned = [word.strip() for word in words]


            title_text = ' '.join(cleaned).lower()
            title_text = title_text[0].upper() + title_text[1:]
            print(title_text)

            for child in h1:
                h1.remove(child)
            h1.text = title_text

    try:
        assert(body[0].tag.endswith('h1'))
    except AssertionError as aerr:
        print("First tag in body is not h1")
        print(aerr)
        import ipdb
        ipdb.set_trace()

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

    # check that we're not missing any h1 that is nested somehow
    assert(len(chapters) == etree.tostring(body).count('<h1'))

    return chapters


class TOCBuilder(object):
    ''' Class for TOC'''

    def __init__(self):
        self.entries = []
        self.previous_element = None

    def as_etree_element(self):
        ''' Returns Toc as etree element'''
        ol = etree.Element('ol')

        for entry in self.entries:
            ol.append(entry.as_etree_element())

        return ol

    def add_entry(self, tocelement):
        ''' Add a new tocelement'''

        # if there are no entries
        if (not self.entries):
            self.entries.append(tocelement)
            self.previous_element = tocelement

            return

        if tocelement.level == 1:
            self.entries.append(tocelement)
            self.previous_element = tocelement

            return

        # if we add a lower level to a higher level
        if tocelement.level > self.previous_element.level:
            assert(tocelement.level - self.previous_element.level == 1)
            self.previous_element.children.append(tocelement)
            tocelement.parent = self.previous_element
            self.previous_element = tocelement

            return

        # we add a level the same as the previous one
        if tocelement.level == self.previous_element.level:
            self.previous_element.parent.children.append(tocelement)
            tocelement.parent = self.previous_element.parent
            self.previous_element = tocelement

            return

        # we add a higher than the previous one, could go from h3 to h1 or h3
        # to h2 etc.
        else:
            leveldiff = tocelement.level - self.previous_element.level
            parent = self.previous_element.parent
            for i in range(leveldiff+1):
                parent = parent.parent

            parent.children.append(tocelement)
            tocelement.parent = parent
            self.previous_element = tocelement

            return


class TocElement(object):
    '''Class to represent an element in the TOC'''
    def __init__(self, filename, h_element):
        self.filename = filename
        self.element = h_element
        self.children = []
        self.parent = None
        self.level = int(self.element.tag[1])

    def as_etree_element(self):
        ''' Return object as etree element'''
        li = etree.Element('li')
        a = etree.Element('a')
        a.attrib['href'] = '{}#{}'.format(self.filename, self.element.attrib['id'])
        a.text = self.element.text
        li.append(a)
        ol = etree.Element('ol')
        for child in self.children:
            ol.append(child.as_etree_element())
        if len(ol) > 0:
            li.append(ol)

        return li


def create_toc(file_list):
    '''Take file list and turn it into a TOC'''

    toc = []

    for htmlfile in file_list:
        with open(htmlfile) as hf:
            html = hf.readlines()
            html = html[4:]
            html = '\n'.join([h for h in html])
            html = etree.HTML(html)

        for element in html.iter():
            if element.tag in ['h1', 'h2']:
                toc.append((htmlfile, copy.deepcopy(element)))

    tocelements = [TocElement(t[0], t[1]) for t in toc]

    assert(len(toc) == len(set(toc)))

    tocbuilder = TOCBuilder()
    for tocelement in tocelements:
        tocbuilder.add_entry(tocelement)


    toccontent = '<div class="container"><div id="contents" class="col-md-12 main-content">\n'
    toccontent += etree.tostring(tocbuilder.as_etree_element(), pretty_print=True)
    toccontent += '\n</div></div>'

    return toccontent


if __name__ == "__main__":

    usage = "Usage: prog <template-name> <title> <files>..."
    arguments = docopt.docopt(usage)

    xhtmlfiles = arguments['<files>']
    template_name = arguments['<template-name>']
    title = arguments['<title>']

    CHAPTER = 1

    file_list = []

    for xhtml in xhtmlfiles:
        html = etree.XML(open(xhtml, 'r').read())

        body = html.find('.//{http://www.w3.org/1999/xhtml}body')
        chapters = split_chapters(body)

        for number, chapter in enumerate(chapters):
            template = '''---\nlayout: {}\ntitle: {}\n---\n'''.format(template_name, title)
            template += '<div class="container">\n'
            template += '  <div id="contents" class="col-md-12 main-content">'
            outputfilename = '{}-{:02d}.html'.format('-'.join(title.lower().split()),
                                                     CHAPTER)
            file_list.append(outputfilename)
            CHAPTER += 1
            with open(outputfilename, 'w') as outputfile:
                for content in chapter:
                    template += etree.tostring(content, encoding='utf-8')

                template += "\n  </div>\n</div>"
                outputfile.write(template)

    toccontent = create_toc(file_list)
    with open('tableofcontents.html', 'w') as tableofcontents:
        tableofcontents.write('---\nlayout: {}\ntitle: {}\n---\n'.format(template_name, title))
        tableofcontents.write(toccontent)
