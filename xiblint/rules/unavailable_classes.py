from xiblint.rules import Rule


class UnavailableClasses(Rule):
    """
    Ensures a given custom class isn't used system types are subclassed by a set of classes.

    You must specify a module as part of the class name.

    Example configuration:
    {
      "classes": {
          "SomeModule.LegacyButton": "SomeModule.NewButton"
      }
    }
    """
    def check(self, context):  # type: (Rule, xiblint.xibcontext.XibContext) -> None
        unavailable_classes = self.config.get('classes', {})
        if not unavailable_classes:
            return

        for element in context.tree.findall('.//*[@customClass]'):
            full_name = self._full_class_name(element)
            replacement = unavailable_classes.get(full_name)

            if not replacement:
                continue

            context.error(element, '`{}` is prohibited. Use `{}` instead.'.format(full_name, replacement))

    def _full_class_name(self, element):  # type: (Rule, Element) -> str
        return "{}.{}".format(element.get('customModule'), element.get('customClass'))
