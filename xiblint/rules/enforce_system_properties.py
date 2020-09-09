from xiblint.rules import Rule
from xiblint.xibcontext import XibContext


class EnforceSystemProperties(Rule):
    """
    Ensures a property in a system type is set to one of the allowed values.

    Example configuration:
    {
      "system_properties": {
        "label": {
          "adjustsFontForContentSizeCategory": ["YES"]
        },
        "button": {
          "reversesTitleShadowWhenHighlighted": [null, "NO"]
        },
        "stackView/color": {
          "key": [null]
        }
      }
    }
    """
    def check(self, context):  # type: (XibContext) -> None
        system_properties = self.config.get('system_properties', {})

        for tag_name in system_properties.keys():
            for element in context.tree.findall('.//{}'.format(tag_name)):
                enforced_properties = system_properties.get(tag_name)
                for property_name in enforced_properties.keys():
                    property_allowed_values = enforced_properties.get(property_name)
                    property_value = element.get(property_name)

                    if property_value in property_allowed_values:
                        continue

                    options_string = '`, `'.join(map(str, property_allowed_values))
                    context.error(element, '`<{}>` property `{}` must use `{}` instead of `{}`.'
                                  .format(tag_name, property_name, options_string, property_value))
