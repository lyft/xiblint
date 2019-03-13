from xml.etree.ElementTree import Element

from xiblint.rules import Rule
from xiblint.xibcontext import XibContext


class UnavailableSystemClasses(Rule):
    """
    Ensures given system types are subclassed by a set of classes.

    You must specify a module as part of the class name.

    Example configuration:
    {
      "system_classes": {
          "navigationController": ["ModuleName.CustomNavigationController"],
          "button": ["ModuleName.CoolButton", "ModuleName.CoolerButton"]
      }
    }
    """
    def check(self, context):  # type: (XibContext) -> None
        custom_classes = self.config.get('system_classes', {})

        for tag_name in custom_classes.keys():
            for element in context.tree.findall('.//{}'.format(tag_name)):
                tag_name = element.tag
                options = custom_classes.get(tag_name)
                custom_class = element.get('customClass')
                options_string = '`, `'.join(options)

                if not custom_class:
                    context.error(element, '`<{}>` without a custom class is prohibited. Use `{}` instead.'
                                  .format(tag_name, options_string))
                    continue

                full_class_name = self._full_class_name(element)
                if full_class_name in options:
                    continue

                context.error(element, '`<{}>` must use `{}` instead of `{}`.'
                              .format(tag_name, options_string, full_class_name))

    def _full_class_name(self, element):  # type: (Rule, Element) -> str
        return "{}.{}".format(element.get('customModule'), element.get('customClass'))
