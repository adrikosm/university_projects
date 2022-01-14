import xml.sax


class GroupHandler(xml.sax.ContentHandler):

    def startElement(self, name, attrs):
        self.current = name
        global ite
        if self.current == 'movies':
            print("---MOVIE---")
            print(f"Element {ite} with info : {attrs['docid']}")
            ite += 1


def characters(self, content):
    if self.current == 'title':
        self.current = content
    elif self.current == 'year':
        self.current == content
    elif self.current == 'type':
        self.current == content
    elif self.current == 'colorinfos':
        self.current == content
    elif self.current == 'genres':
        self.current == content
    elif self.current == 'languages ':
        self.current == content
    elif self.current == 'countries':
        self.current == content
    elif self.current == 'releasedates':
        self.current == content
    elif self.current == 'directors':
        self.current == content
    elif self.current == 'composers':
        self.current == content
    elif self.current == 'cast':
        self.current == content
    elif self.current == 'plot':
        self.current == content
    elif self.current == 'url':
        self.current == content


def endElement(self, name):
    if self.current == 'title':
        print(f"Name : {self.name}")
    elif self.current == 'year':
        print(f"Year : {self.year}")
    elif self.current == 'type':
        print(f"type : {self.type}")
    elif self.current == 'colorinfos':
        print(f"colorinfos : {self.colorinfos}")
    elif self.current == 'genres':
        print(f"genres : {self.genres}")
    elif self.current == 'languages ':
        print(f"languages : {self.languages}")
    elif self.current == 'countries':
        print(f"countries : {self.countries}")
    elif self.current == 'releasedates':
        print(f"releasedates : {self.releasedates}")
    elif self.current == 'directors':
        print(f"directors : {self.directors}")
    elif self.current == 'composers':
        print(f"composers : {self.composers}")
    elif self.current == 'cast':
        print(f"cast : {self.cast}")
    elif self.current == 'plot':
        print(f"plot : {self.plot}")
    elif self.current == 'url':
        print(f"url : {self.url}")
    self.current = ""


ite = 0

handler = GroupHandler()
parser = xml.sax.make_parser()
parser.setContentHandler(handler)
parser.parse('all.xml')
