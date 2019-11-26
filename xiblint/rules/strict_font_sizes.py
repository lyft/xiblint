from xiblint.rules import Rule
from xiblint.xibcontext import XibContext


class StrictFontSizes(Rule):
    """
    Ensures fonts are in the allowed set.

    Example configuration:
    {
      "minimum_size": 13,
      "maximum_size": 30
    }
    """
    def check(self, context):  # type: (XibContext) -> None
        minimum_size = self.config.get('minimum_size', 0)
        maximum_size = self.config.get('maximum_size', 1000)

        for element in context.tree.findall('.//font') + context.tree.findall('.//fontDescription'):
            attribute_name = None

            if element.tag == 'font':
                # Skip <font> tags nested in a localization comment
                container = element.parent.parent.parent
                if container.tag == 'attributedString' and container.get('key') == 'userComments':
                    continue

                attribute_name = 'size'
            else:
                attribute_name = 'pointSize'

            size = element.get(attribute_name)
            if size is None:
                context.error(element, 'Invalid <{}> found. Must have a {}.'.format(element.tag, attribute_name))
                continue

            point_size = int(size)

            if point_size < minimum_size:
                context.error(element, '"{}" is smaller than the allowed minimum size ({})'.format(size, minimum_size))
            elif point_size > maximum_size:
                context.error(element, '"{}" is larger than the allowed maximum size ({})'.format(size, maximum_size))
