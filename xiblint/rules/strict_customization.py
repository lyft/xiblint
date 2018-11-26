from xiblint.rules import Rule


class StrictCustomization(Rule):
    """
    Ensures given system types are subclassed by a set of classes.

    You must specify a module as part of the class name.

    Example configuration:
    {
      "custom_classes": {
          "navigationController": ["ModuleName.CustomNavigationController"],
          "button": ["ModuleName.CoolButton", "ModuleName.CoolerButton"]
      }
    }
    """
    def check(self, context):  # type: (Rule, xiblint.xibcontext.XibContext) -> None
        custom_classes = self.config.get('custom_classes', {})
        for tag_name in custom_classes.keys():
            for element in context.tree.findall('.//' + tag_name):
                custom_class = element.get('customClass')
                options = custom_classes.get(tag_name)

                if custom_class:
                    if self.is_valid(element, options):
                        continue

                    context.error(element, '`<' + tag_name + '>` must use `' + '`, `'.join(options) + '` instead of `'
                                  + element.get('customModule') + '.' + element.get('customClass') + '`.')
                    return

                context.error(element, '`<' + tag_name + '>` without a custom class is prohibited. Use `' + '`, `'
                              .join(options) + '` instead.')

    def is_valid(self, element, custom_classes):  # type: (Rule, Element, [str]) -> Bool
        full_name = element.get('customModule') + '.' + element.get('customClass')
        return full_name in custom_classes
