from xiblint.rules import Rule
from xiblint.xibcontext import XibContext


class NamedColors(Rule):
    """
    Ensures colors are using named colors from an asset catalog.

    Example configuration:
    {
      "ignore_alpha": true
    }
    """
    def check(self, context):  # type: (XibContext) -> None
        ignore_alpha = self.config.get('ignore_alpha', False)

        for element in context.tree.findall(".//color"):
            # Skip <color> tags nested in a localization comment
            container = element.parent.parent.parent
            if container.tag == 'attributedString' and container.get('key') == 'userComments':
                continue

            # Skip <color> tags part of a color definition
            if element.parent.tag == 'namedColor':
                continue

            # Skip colors with alpha
            if ignore_alpha and element.get('alpha') is not None:
                continue

            if element.get('name') is None:
                context.error(element, "Use of custom colors is not allowed. Use a named color instead.")
                continue
