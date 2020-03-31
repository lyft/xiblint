from xml.etree.ElementTree import Element

from xiblint.rules import Rule
from xiblint.xibcontext import XibContext


class EnforceSystemProperties(Rule):
    """
    Ensures unavailable system properties are not used.

    Example configuration:
    {
      "system_properties": {
        "label": {
          "adjustsFontForContentSizeCategory": [null, "NO"]
        },
        "button": {
          "reversesTitleShadowWhenHighlighted": ["YES"]
        }
      }
    }
    """
    def check(self, context):  # type: (XibContext) -> None
        system_properties = self.config.get('system_properties', {})

        for tag_name in system_properties.keys():
            for element in context.tree.findall('.//{}'.format(tag_name)):
                tag_name = element.tag
                enforced_properties = system_properties.get(tag_name)
                for property_name in enforced_properties.keys():
                    property_allowed_values = enforced_properties.get(property_name)
                    property_value = element.get(property_name)

                    if property_value in property_allowed_values:
                        continue

                    options_string = '`, `'.join(map(str, property_allowed_values))
                    context.error(element, '`<{}>` property `{}` must use `{}` instead of `{}`.'
                                  .format(tag_name, property_name, options_string, property_value))
