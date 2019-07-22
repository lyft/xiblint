from xiblint.rules import Rule
from xiblint.xibcontext import XibContext


class NoAttributedStringColors(Rule):
    """
    Ensures attributed strings don't specify colors.
    """
    def check(self, context):  # type: (XibContext) -> None
        for element in context.tree.findall(".//color"):
            # Skip <color> tags nested in a localization comment
            container = element.parent.parent.parent
            if container.tag == 'attributedString' and container.get('key') == 'userComments':
                continue

            # Skip <color> tags part of a color definition
            if element.parent.tag == 'namedColor':
                continue

            # Require a name
            if element.get('key') == "NSColor":
                context.error(element, "Colors in attributed strings are not allowed. Configure in code instead.")
                continue
