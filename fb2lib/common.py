#-*-coding:utf8-*-


class Common(object):
    def __init__(self, root):
        self._ns = None
        self._root = root

    def _get_tag_name(self, tag):
        name = tag.tag
        for ns in tag.nsmap.values():
            name = name.replace('{%s}' % ns, '')
        return name.strip()

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
            if isinstance(name, list):
                name = '/'.join(['default:%s' % n for n in name])
            else:
                name = 'default:%s' % name
            elem = self.root.xpath('//%s' % name,
                    namespaces=self.namespace)
        else:
            if isinstance(name, list):
                name = '/'.join(name)
            elem = self.root.xpath('//%s' % name)
        if not mass:
            elem = None if not len(elem) > 0 else elem[0]
        return elem
