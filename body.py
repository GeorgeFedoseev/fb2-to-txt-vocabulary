#-*-coding:utf8-*-
from common import Common

import logging


LOG = logging.getLogger('body')


class MainTag(Common):
    def __init__(self, tag):
        self._tag = tag
        self._tags = []
        self._parse()

    @property
    def root(self):
        return self._tag

    def add_tag(self, tag):
        self._tags.append(tag)

    def _parse(self):
        for child in self.root.getchildren():
            name = self._get_tag_name(child)
            try:
                t = TAGS[name](child)
            except KeyError:
                LOG.error("I'm not know tag %s in line %s" %
                    (name, child.sourceline))
                continue
            self.add_tag(t)

    def _to_text(self, text):
        return text

    def to_text(self):
        text = ''
        for tag in self._tags:
            text += tag.to_text()
        if self.root.text:
            return self._to_text(self.root.text.strip() + text)
        else:
            return self._to_text(text)

    def _to_html(self, text):
        return text

    def to_html(self):
        text = ''
        for tag in self._tags:
            text += tag.to_html()
        if self.root.text:
            return self._to_html(self.root.text.strip() + text)
        else:
            return self._to_html(text)


class TagBody(MainTag):
    pass


class TagSection(MainTag):
    pass


class TagAnnotation(MainTag):
    pass


class TagPoem(MainTag):
    pass


class TagCite(MainTag):
    pass


class TagEpigraph(MainTag):
    pass


class TagP(MainTag):
    def _to_html(self, text):
        return '<p>' + text + '</p>'

    def _to_text(self, text):
        return '\n\t' + text


class TagEmptyLine(MainTag):
    def _to_html(self, text):
        return text + '<br/>'

    def _to_text(self, text):
        return text + '\n'


class TagTextAuthor(MainTag):
    pass


class TagA(MainTag):
    pass


class TagImage(MainTag):
    pass


class TagTitle(MainTag):
    def _to_html(self, text):
        return '<H1>' + text + '</H1>'

    def _to_text(self, text):
        return '\n' + text + '\n'


TAGS = {'body': TagBody,
        'section': TagSection,
        'annotation': TagAnnotation,
        'poem': TagPoem,
        'cite': TagCite,
        'epigraph': TagEpigraph,
        'p': TagP,
        'empty-line': TagEmptyLine,
        'image': TagImage,
        'title': TagTitle,
        'a': TagA,
        'text-author': TagTextAuthor}
