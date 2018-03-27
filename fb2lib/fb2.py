#-*-coding:utf8-*-
from lxml import etree
from info import TitleInfo, PublishInfo, DocumentInfo


class PyFb2(object):
    def __init__(self, fpath):
        self.file = fpath
        self._tree = None
        self._ns = None
        self._root = None

    def _get_tag_name(self, tag):
        name = tag.tag
        for ns in tag.nsmap.values():
            name = name.replace('{%s}' % ns, '')
        return name.strip()

    def _get_tree(self):
        if not self._tree:
            parser = etree.XMLParser(ns_clean=True, recover=True)
            self._tree = etree.parse(self.file, parser)
        return self._tree

    @property
    def root(self):
        if self._root is None:
            self._root = self._get_tree().getroot()
        return self._root

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

    def get_element(self, name, mass=False):
        if 'default' in self.namespace:
            elem = self.root.xpath('//default:%s' % name,
                    namespaces=self.namespace)
        else:
            elem = self.root.xpath('//%s' % name)
        if not mass:
            elem = None if not len(elem) > 0 else elem[0]
        return elem

    def get_title_info(self):
        title = self.get_element('title-info')
        if title is not None:
            return TitleInfo(title)
        return None

    def get_document_info(self):
        document = self.get_element('document-info')
        if document is not None:
            return DocumentInfo(document)
        return None

    def get_publish_info(self):
        publish = self.get_element('publish-info')
        if publish is not None:
            return PublishInfo(publish)
        return None
