from xiblint.rules import Rule
from xiblint.xibcontext import XibContext


class StrictFontNames(Rule):
    """
    Ensures fonts are in the allowed set.

    Example configuration:
    {
      "allowed_fonts": ["ComicSans-Regular", "ComicSans-Bold"],
      "allow_system_fonts": true
    }
    """
    def check(self, context):  # type: (XibContext) -> None
        allowed_fonts = self.config.get('allowed_fonts', [])
        allow_system_fonts = self.config.get('allow_system_fonts', False)

        for element in context.tree.findall(".//fontDescription") + context.tree.findall(".//font"):
            # Skip <font> tags nested in a localization comment
            if element.tag == 'font':
                container = element.parent.parent.parent
                if container.tag == 'attributedString' and container.get('key') == 'userComments':
                    continue

            font_name = element.get('name')
            if font_name is None:
                if not allow_system_fonts:
                    context.error(element, "Use of system fonts is not allowed.")
                continue

            if font_name not in allowed_fonts:
                context.error(element, '"{}" is not one of the allowed fonts.'.format(font_name))
