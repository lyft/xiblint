from xiblint.rules import Rule


class StrictFontNames(Rule):
    """
    Ensures fonts are in the allowed set.

    Example configuration:
    {
      "allowed_fonts": ["ComicSans-Regular", "ComicSans-Bold"],
      "allow_system_fonts": true
    }
    """
    def check(self, context):  # type: (Rule, xiblint.xibcontext.XibContext) -> None
        allowed_fonts = self.config.get('allowed_fonts', [])
        allow_system_fonts = self.config.get('allow_system_fonts', False)

        for element in context.tree.findall(".//fontDescription") + context.tree.findall(".//font"):
            font_name = element.get("name")
            if font_name is None:
                if not allow_system_fonts:
                    context.error(element, "Use of system fonts is not allowed.")
                continue

            if font_name not in allowed_fonts:
                context.error(element, f'"{font_name}" is not one of the allowed fonts.')
