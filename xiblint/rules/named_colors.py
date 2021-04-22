from xiblint.rules import Rule
from xiblint.xibcontext import XibContext


class NamedColors(Rule):
    """
    Ensures colors are using named colors from an asset catalog.

    Example configuration:
    {
      "allowed_colors": ["CustomRed", "CustomGreen"],
      "allow_system_colors": true,
      "ignore_alpha": true,
      "allow_clear_color": true
    }
    """
    def check(self, context):  # type: (XibContext) -> None
        allowed_colors = self.config.get('allowed_colors', [])
        allow_system_colors = self.config.get('allow_system_colors', False)
        ignore_alpha = self.config.get('ignore_alpha', False)
        allow_clear_color = self.config.get('allow_clear_color', False)

        for element in context.tree.findall(".//color"):
            # Skip <color> tags nested in a localization comment
            container = element.parent.parent.parent
            if container.tag == 'attributedString' and container.get('key') == 'userComments':
                continue

            # Skip <color> tags part of a color or system color definition
            if element.parent.tag == 'namedColor' or element.parent.tag == 'systemColor':
                continue

            # Skip colors with alpha (if configured)
            if ignore_alpha and element.get('alpha') is not None and element.get('alpha') != '1':
                continue

            # Skip clear color (if configured)
            if (
                    allow_clear_color and
                    element.get('alpha') is not None and element.get('white') is not None and
                    element.get('alpha') == '0.0' and element.get('white') == '0.0'
            ):
                continue

            color = element.get('key') if element.get('key') else 'color'

            # If `systemColor` or `catalog` is present, it's a named system color
            if (
                    element.get('systemColor') is not None or
                    element.get('cocoaTouchSystemColor') is not None or
                    element.get('catalog') is not None
            ):
                if not allow_system_colors:
                    context.error(element,
                                  "Use of named system {}s is not allowed. Use a named color instead."
                                  .format(color))
                continue

            # Require a name
            color_name = element.get('name')
            if color_name is None:
                context.error(element,
                              "Use of custom {}s is not allowed. Use a named color instead."
                              .format(color))
                continue

            # If allowed_colors is set, verify that color_name is included
            options_string = '`, `'.join(map(str, allowed_colors))
            if allowed_colors and color_name not in allowed_colors:
                context.error(element, '"{}" is not one of the allowed {}s: `{}`.'
                              .format(color_name, color, options_string))
