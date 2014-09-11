import sys
import os
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
            while title_text[0].isdigit():
                title_text = title_text[1:].strip()

            for child in h1:
                h1.remove(child)
                h1.text = title_text


    try:
        assert(body[0].tag.endswith('h1'))
    except AssertionError as aerr:
        print("First tag in body is not h1")
        print(aerr)
        import ipdb; ipdb.set_trace()

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

    for t in toc:
        print(t[1].attrib['id']); print(t[1].text.strip())


    assert(len(toc) == len(set(toc)))
    # TODO remember to add this:
    #
    # ---
    # layout: content-page
    # title: Natural Sciences Grade 7
    # ---


    return toc







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
            template = '''---\nlayout: {}\ntitle:{}\n---\n'''.format(template_name, title)
            template += '<div class="container">\n'
            template += '  <div id="contents" class="col-md-12 main-content">'
            outputfilename = '{:02d}-{}.html'.format(CHAPTER,
                                                     '-'.join(title.lower().split()))
            file_list.append(outputfilename)
            CHAPTER += 1
            with open(outputfilename, 'w') as outputfile:
                for content in chapter:
                    template += etree.tostring(content, encoding='utf-8')

                template += "\n  </div>\n</div>"
                outputfile.write(template)

    create_toc(file_list)
#       for bodychild in body:
#           template += etree.tostring(bodychild, method='xml')
#       template = template.replace('xmlns="http://www.w3.org/1999/xhtml"', '')
#       with open(xhtml.replace('.xhtml', '-test.html'), 'w') as output:
#           output.write(template.encode('utf-8'))

#   writeTOC()
