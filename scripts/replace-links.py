import os
import csv

from lxml import etree


def replace_links(filename, urls):
    ''' Replace bit.ly links in given file with the real urls. Added embed code
    if it is Youtube
    '''
    with open(filename, 'r') as f_in:
        contents = f_in.readlines()

    if 'tableofcontents' in filename:
        return
    if 'inhouds' in filename:
        return

    try:
        html = etree.HTML(''.join(contents[4:]))
    except etree.XMLSyntaxError:
        # jekyll file
        import ipdb; ipdb.set_trace()
        html = etree.HTML(''.join(contents[4:]))

    # replace links
    for (url, curious, bitly) in urls:
        for anchor in html.findall('.//a'):
            if 'href' not in anchor.attrib:
                continue
            if 'youtube' in url:
                if bitly in anchor.attrib['href']:
                    newlink = etree.fromstring(url)
                    newlink.text = ''
                    anchor.addnext(newlink)
                    anchor.getparent().remove(anchor)

            else:
                if bitly in anchor.attrib['href']:
                    newlink = url
                    anchor.text = ' ' + url
                    anchor.attrib['href'] = url


    newcontents = ''.join(contents[0:4])
    for child in html.find('.//body'):
        newcontents += etree.tostring(child) + '\n'

    with open(filename, 'w') as f_out:
        f_out.write(newcontents)


def get_youtube_code(url, bitly):
    ''' Return just the youtube code'''
    code = None

    if 'youtube' in url:
        if 'v=' in url:
            code = url[url.find('v=')+2:]
            if r'&' in code:
                code = code[0:code.find(r'&')]

    elif 'youtu.be' in url:
        code = url.split('/')[-1]

    if '#' in code:
        code = code[0:code.find('#')]

    if not code:
        import ipdb; ipdb.set_trace()

    return code


if __name__ == "__main__":
    natsci = ['natural-sciences', 'natuurwetenskappe']

    urls = [line for line in csv.reader(open('consolidated.csv'))]

    # replace youtube links with embed codes
    for i, (url, curious, bitly) in enumerate(urls):
        if 'youtu' in url:
            code = get_youtube_code(url, bitly)
            code = r'''<iframe width="420" height="315" src="http://www.youtube.com/embed/{}"></iframe>'''.format(code)
            urls[i] = (code, curious, bitly)

    for dirpath, dirnames, files in os.walk(os.curdir):
        if dirpath in ['.', '..']:
            continue
        # only want those two folders
        dp = dirpath.split('/')[1]
        if dp not in natsci:
            continue

        htmlfiles = [f for f in files if '.html' in f]

        for htmlfile in htmlfiles:
            replace_links(os.path.join(dirpath, htmlfile), urls)
