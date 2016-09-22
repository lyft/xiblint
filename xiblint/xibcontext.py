from __future__ import unicode_literals
from xiblint.xmlutils import parse_xml, element_and_parents


class XibContext(object):
    def __init__(self, path):
        self.path = path
        self.success = True
        self.tree = parse_xml(path)
        self.rule_name = None

    @staticmethod
    def _get_object_id(element):
        for element in element_and_parents(element):
            object_id = element.get('id')
            if object_id is not None:
                return object_id

    @staticmethod
    def _get_moniker(view):
        """
        Tries to determine a human-readable string for a view.
        """
        label = view.get('userLabel')
        if label:
            return label
        if view.tag == 'button':
            state_normal = view.find("./state[@key='normal']")
            if state_normal is not None:
                return state_normal.get('title') or state_normal.get('image')

    def error(self, element, message, *args):
        self.success = False
        object_id = self._get_object_id(element)
        moniker = self._get_moniker(element)
        print("{}:{}: error: {}{}{} [rule: {}]".format(
            self.path,
            element.line,
            "{}: ".format(object_id) if object_id else '',
            "'{}': ".format(moniker) if moniker else '',
            message.format(*args),
            self.rule_name,
        ))
