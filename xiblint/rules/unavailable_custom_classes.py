from xml.etree.ElementTree import Element

from xiblint.rules import Rule
from xiblint.xibcontext import XibContext


class UnavailableCustomClasses(Rule):
    """
    Ensures a given custom class isn't used and provides a replacement suggestion.

    You must specify a module as part of the class name.

    Example configuration:
    {
      "custom_classes": {
          "SomeModule.LegacyButton": "SomeModule.NewButton"
      }
    }
    """
    def check(self, context):  # type: (XibContext) -> None
        unavailable_classes = self.config.get('custom_classes', {})

        for element in context.tree.findall('.//*[@customClass]'):
            full_name = self._full_class_name(element)
            replacement = unavailable_classes.get(full_name)

            if not replacement:
                continue

            context.error(element, '`{}` is prohibited. Use `{}` instead.'.format(full_name, replacement))

    def _full_class_name(self, element):  # type: (Rule, Element) -> str
        return "{}.{}".format(element.get('customModule'), element.get('customClass'))
