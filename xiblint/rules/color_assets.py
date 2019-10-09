from xiblint.rules import Rule
from xiblint.xibcontext import XibContext
import glob
import json

class ColorAssets(Rule):
    def __init__(self, config):
        asset_catalog_path = config.get('asset_catalog', None)
        if asset_catalog_path is None:
            # TODO: Proper error
            print("Asset catalog not found. Please configure 'asset_catalog'.")
            return

        self.assets = glob.glob("{}/**/*.colorset".format(asset_catalog_path))

        if not self.assets:
            # TODO: Proper error
            print("Failed to load asset catalog at: '{}'".format(asset_catalog_path))
            return

        self.colors = {}

    """
    Ensures cached named colors match the named colors from an asset catalog.

    Example configuration:
    {
      "asset_catalog": "Resources/Color.xcassets"
    }
    """
    def check(self, context):  # type: (XibContext) -> None
        for element in context.tree.findall(".//namedColor"):
            name = element.get("name")
            if name is None:
                context.error(element, "Named color is missing a name.")
                continue

            color = self.load_color(name)
            if color is None:
                context.error(element, "Named color '{}' is missing from asset catalog.".format(name))
                continue

            color_element = element.find("color")
            if color_element is None:
                context.error(element, "Named color '{}' is missing color definition.".format(name))
                continue

            red = color_element.get("red")
            green = color_element.get("green")
            blue = color_element.get("blue")
            alpha = color_element.get("alpha")
            if red is None or green is None or blue is None or alpha is None:
                context.error(element, "Named color '{}' has invalid color value.".format(name))
                continue

            if float(red) != color[0] or float(green) != color[1] or float(blue) != color[2] or float(alpha) != color[3]:
                context.error(element, "Color value for '{}' does not match asset catalog.".format(name))

    def load_color(self, name):
        if name in self.colors:
            return self.colors[name]

        for path in self.assets:
            if not path.endswith("{}.colorset".format(name)):
                continue

            with open("{}/Contents.json".format(path)) as json_file:
                data = json.load(json_file)
                components = data["colors"][0]["color"]["components"]
                color = (self.load_component(components, "red"), self.load_component(components, "green"), self.load_component(components, "blue"), self.load_component(components, "alpha"))
                self.colors[name] = color
                return color

    def load_component(self, components, key):
        string = components[key]

        if "." in string:
            return float(string)

        return float(string) / 255.0
