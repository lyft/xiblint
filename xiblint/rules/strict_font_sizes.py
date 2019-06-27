from xiblint.rules import Rule
from xiblint.xibcontext import XibContext


class StrictFontSizes(Rule):
    """
    Ensures fonts are in the allowed set.

    Example configuration:
    {
      "minimum_size": 13
    }
    """
    def check(self, context):  # type: (XibContext) -> None
        minimum_size = self.config.get('minimum_size', 10)

        for element in context.tree.findall(".//font"):
            # Skip <font> tags nested in a localization comment
            container = element.parent.parent.parent
            if container.tag == 'attributedString' and container.get('key') == 'userComments':
                continue

            size = element.get('size')
            if size is None:
                context.error(element, "Invalid <font> found. Must have a size.")
                continue

            if int(size) < minimum_size:
                context.error(element, '"{}" is smaller than the allowed minimum size ({})'.format(size, minimum_size))

        for element in context.tree.findall(".//fontDescription"):
            size = element.get('pointSize')
            if size is None:
                context.error(element, "Invalid <fontDescription> found. Must have a pointSize.")
                continue

            if int(size) < minimum_size:
                context.error(element, '"{}" is smaller than the allowed minimum size ({})'.format(size, minimum_size))

