from __future__ import unicode_literals
from .xmlutils import parse_xml
from .xibutils import get_object_id


class XibContext(object):
    def __init__(self, path):
        self.path = path
        self.success = True
        self.tree = parse_xml(path)
        self.rule_name = None
        self.errors = []

    @staticmethod
    def _get_moniker(view):
        """
        Tries to determine a human-readable string for a view.
        """
        label = view.get('userLabel')
        if label:
            return label
        if view.tag == 'imageView':
            return view.get('image')
        if view.tag == 'button':
            state_normal = view.find("./state[@key='normal']")
            if state_normal is not None:
                return state_normal.get('title') or state_normal.get('image')

    def error(self, element, message, *args):
        self.success = False
        object_id = get_object_id(element)
        moniker = self._get_moniker(element)

        new_error = "{}{}{}".format(
            "{}: ".format(object_id) if object_id else '',
            "'{}': ".format(moniker) if moniker else '',
            message.format(*args)
        )
        new_error_dict = {"file": self.path, 
            "line": element.line, 
            "error": new_error, 
            "rule": self.rule_name}

        self.errors.append(new_error_dict)
