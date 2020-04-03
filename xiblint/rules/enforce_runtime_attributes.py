from xiblint.rules import Rule
from xiblint.xibcontext import XibContext


class EnforceRuntimeAttributes(Rule):
    """
    Ensures a runtime attribute is set to one of the allowed values.

    You must specify a module as part of the class name if it is a custom type.

    Example configuration:
    {
      "runtime_attributes": {
        "SomeModule.LegacyButton": {
          "sizeName": ["small", "large"]
        },
        "button": {
          "layer.cornerRadius": [null]
        }
      }
    }
    """
    def check(self, context):  # type: (XibContext) -> None
        runtime_attributes = self.config.get('runtime_attributes', {})

        for full_class_name in runtime_attributes.keys():
            enforced_attributes = runtime_attributes.get(full_class_name)

            # Get system or custom class elements
            full_class_name_split = full_class_name.split(".")
            if len(full_class_name_split) == 1:
                elements = context.tree.findall(".//{}".format(full_class_name))
            elif len(full_class_name_split) == 2:
                elements = context.tree.findall(".//*[@customClass='{}'][@customModule='{}']"
                                                .format(full_class_name_split[1], full_class_name_split[0]))

            for element in elements:
                for attribute_keyPath in enforced_attributes.keys():
                    attribute_allowed_values = enforced_attributes.get(attribute_keyPath)
                    attribute_value = None

                    attribute_list = element.find("./userDefinedRuntimeAttributes")
                    if attribute_list is not None:
                        attribute_element = attribute_list.find("./userDefinedRuntimeAttribute/[@keyPath='{}']"
                                                                .format(attribute_keyPath))
                        if attribute_element is not None:
                            attribute_value = attribute_element.get("value")

                    if attribute_value in attribute_allowed_values:
                        continue

                    options_string = '`, `'.join(map(str, attribute_allowed_values))
                    context.error(element, '`<{}>` runtime attribute `{}` must use `{}` instead of `{}`.'
                                  .format(full_class_name, attribute_keyPath, options_string, attribute_value))
