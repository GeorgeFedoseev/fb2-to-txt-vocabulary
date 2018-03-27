#-*-coding:utf8-*-


class Info(object):
    def __init__(self, root):
        self._root = root
        self._ns = None

    def _get_tag_name(self, tag):
        name = tag.tag
        for ns in tag.nsmap.values():
            name = name.replace('{%s}' % ns, '')
        return name.strip()

    def get_element(self, name, mass=False):
        if 'default' in self.namespace:
            elem = self.root.xpath('//default:%s' % name,
                    namespaces=self.namespace)
        else:
            elem = self.root.xpath('//%s' % name)
        if not mass:
            elem = None if not len(elem) > 0 else elem[0]
        return elem

    @property
    def namespace(self):
        if self._ns is None:
            nsmap = self.root.nsmap
            if None in nsmap:
                default = nsmap[None]
                del(nsmap[None])
                nsmap['default'] = default
            self._ns = nsmap
        return self._ns

    @property
    def root(self):
        return self._root


class TitleInfo(Info):
    def __init__(self, root):
        super(TitleInfo, self).__init__(root)
        self._author = None
        self._genres = None
        self._title = None
        self._lang = None

    @property
    def author(self):
        if self._author is None:
            author = self.get_element('author')
            if author is None:
                self._author = ''
                return self._author
            name = {'first-name': '', 'middle-name': '', 'last-name': ''}
            for child in author.getchildren():
                name.update({self._get_tag_name(child):
                    '%s ' % child.text.strip()})
            self._author = "%(first-name)s%(middle-name)s%(last-name)s" % name
        return self._author

    @property
    def genres(self):
        if self._genres is None:
            genres = self.get_element('genre', mass=True)
            self._genres = []
            for genre in genres:
                self._genres.append(genre.text)
        return self._genres

    @property
    def title(self):
        if self._title is None:
            title = self.get_element('book-title')
            if title is not None:
                title = title.text
            self._title = title
        return self._title

    @property
    def lang(self):
        if self._lang is None:
            lang = self.get_element('lang')
            if lang is not None:
                lang = lang.text
            self._lang = lang
        return self._lang


class DocumentInfo(Info):
    def __init__(self, root):
        super(DocumentInfo, self).__init__(root)
        self._author = None
        self._date = None
        self._source = None
        self._id = None

    @property
    def author(self):
        if self._author is None:
            author = self.get_element('author')
            if author is None:
                self._author = ''
                return self._author
            else:
                author = author[0]
            name = {'first-name': '', 'middle-name': '', 'last-name': ''}
            for child in author.getchildren():
                name.update({self._get_tag_name(child):
                    '%s ' % child.text.strip()})
            self._author = "%(first-name)s%(middle-name)s%(last-name)s" % name
        return self._author

    @property
    def date(self):
        if self._date is None:
            date = self.get_element('date')
            if date is not None:
                date = date.text
            self._date = date
        return self._date

    @property
    def source(self):
        if self._source is None:
            source = self.get_element('src-url')
            if source is not None:
                source = source.text
            self._source = source
        return self._source

    @property
    def id(self):
        if self._id is None:
            id = self.get_element('id')
            if id is not None:
                id = id.text
            self._id = id
        return self._id


class PublishInfo(Info):
    def __init__(self, root):
        super(PublishInfo, self).__init__(root)
        self._name = None
        self._publisher = None
        self._city = None
        self._year = None
        self._isdn = None

    @property
    def name(self):
        if self._name is None:
            name = self.get_element('book-name')
            if name:
                name = name.text
            self._name = name
        return self._name

    @property
    def publisher(self):
        if self._publisher is None:
            publisher = self.get_element('publisher')
            if publisher is not None:
                publisher = publisher.text
            self._publisher = publisher
        return self._publisher

    @property
    def city(self):
        if self._city is None:
            city = self.get_element('city')
            if city is not None:
                city = city.text
            self._city = city
        return self._city

    @property
    def year(self):
        if self._year is None:
            year = self.get_element('year')
            if year is not None:
                year = year.text
            self._year = year
        return self._year

    @property
    def isdn(self):
        if self._isdn is None:
            isdn = self.get_element('isdn')
            if isdn is not None:
                isdn = isdn.text
            self._isdn = isdn
        return self._isdn
