from xiblint.rules import Rule
from xiblint.xibcontext import XibContext


class StrictFonts(Rule):
    """
    Ensures font name and size combinations are in the allowed set. This would generally be used instead
    of strict_font_names and strict_font_sizes.

    Example configuration:
    {
      "allowed_fonts": [
        {
          "name": "ComicSans-Regular",
          "size": 14
        },
        {
          "name": "ComicSans-Bold",
          "size": 14
        }
      ]
    }
    """
    def check(self, context):  # type: (XibContext) -> None
        allowed_fonts = [(d["name"], d["size"]) for d in self.config.get('allowed_fonts', [])]

        for element in context.tree.findall('.//font') + context.tree.findall('.//fontDescription'):
            size_attribute_name = None

            if element.tag == 'font':
                # Skip <font> tags nested in a localization comment
                container = element.parent.parent.parent
                if container.tag == 'attributedString' and container.get('key') == 'userComments':
                    continue

                size_attribute_name = 'size'
            else:
                size_attribute_name = 'pointSize'

            raw_size = element.get(size_attribute_name)
            if raw_size is None:
                context.error(element, 'Invalid <{}> found. Must have a {}.'.format(element.tag, size_attribute_name))
                continue

            size = int(raw_size)

            name = element.get('name')
            if name is None:
                context.error(element, 'Invalid <{}> found. Must have a name.'.format(element.tag))
                continue

            if (name, size) not in allowed_fonts:
                context.error(element, 'Invalid font found {} {}. Please use an allowed font.'.format(name, size))
