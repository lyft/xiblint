from xiblint.rules import Rule
from xiblint.xibcontext import XibContext


class StrictColorNames(Rule):
    """
    Ensures colors are in an allowed set.

    Example configuration:
    {
        "allowed_colors": ["CustomRed", "CustomGreen"],
        "allow_system_colors": true,
    }
    """
    def check(self, context):  # type: (XibContext) -> None
        allowed_colors = self.config.get('allowed_colors', [])
        allow_system_colors = self.config.get('allow_system_colors', False)

        for element in context.tree.findall(".//color"):
            # Skip <color> tags nested in a localization comment
            container = element.parent.parent.parent
            if container.tag == 'attributedString' and container.get('key') == 'userComments':
                continue

            # Skip <color> tags part of a color definition
            if element.parent.tag == 'namedColor':
                continue

            # Skip <color> tags part of a system color definition
            if element.parent.tag == 'systemColor':
                continue

            # If `systemColor` or `catalog` is present, it's a named system color
            if element.get('systemColor') is not None or element.get('catalog') is not None:
                if not allow_system_colors:
                    context.error(element, "Use of named system colors is not allowed. Use a named color instead.")
                continue

            # Require a name
            color_name = element.get('name')
            if color_name is None:
                context.error(element, "Use of custom colors is not allowed. Use a named color instead.")
                continue

            if color_name not in allowed_colors:
                context.error(element, '"{}" is not one of the allowed colors.'.format(color_name))
