from xiblint.rules import Rule
from xiblint.xibcontext import XibContext


class ColorAssets(Rule):
    """
    Ensures cached named colors match the named colors from an asset catalog.

    Example configuration:
    {
      "asset_catalog": "Resources/Color.xcassets"
    }
    """
    def check(self, context):  # type: (XibContext) -> None
        asset_catalog_path =  = self.config.get('asset_catalog', None)
        if asset_catalog_path is None:
            # TODO: Show an error?
            return

        for element in context.tree.findall("./namedColor"):
            name = element.get("name")
            if name is None
                context.error(element, "Named color is missing a name.")
                continue

            # TODO: Find the color in the cache or find the JSON file on disk for a given `name`
            # TODO: Convert color values from the various JSON formats to the proper float format
            # TODO: Ensure we only look at the light variant if there are multiple variants
            # TODO: Cache the value if loaded

            color_element = element.find("color")
            if color_element is None:
                context.error(element, "Named color is missing color definition.")
                continue

            red = color_element.get("red")
            green = color_element.get("green")
            blue = color_element.get("blue")
            alpha = color_element.get("alpha")
            if red is None or green is None or blue is None or alpha is None:
                context.error(element, "Named color has invalid color value.")
                continue

            # TODO: Compare the color here to the color from the asset catalog
            # TODO: If the don't match (with some tolerence), add an error
