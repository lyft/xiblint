import sys

# HACK to ensure cElementTree is not loaded -- we need the Pythonic implementation
assert 'xml.etree.ElementTree' not in sys.modules
sys.modules['_elementtree'] = {}
from xml.etree import ElementTree  # noqa


class _TreeBuilder(ElementTree.TreeBuilder):
    """
    Adds a line and column number to every element.
    """
    parser = None

    def start(self, tag, attrs):
        elem = super(_TreeBuilder, self).start(tag, attrs)
        elem.line = self.parser.parser.CurrentLineNumber
        elem.column = self.parser.parser.CurrentLineNumber
        return elem


def parse_xml(file_path):
    builder = _TreeBuilder()
    parser = ElementTree.XMLParser(target=builder)
    builder.parser = parser
    tree = ElementTree.parse(file_path, parser=parser)

    # ElementTree does not implement parent attributes: add parent property to every element
    parent_map = {child: parent
                  for parent in tree.getiterator()
                  for child in parent}
    for p in tree.getiterator():
        p.parent = parent_map.get(p)

    return tree


def element_and_parents(p):
    """
    Helper to iterate over the XML element and its parents up to root.
    """
    while p is not None:
        yield p
        p = p.parent
