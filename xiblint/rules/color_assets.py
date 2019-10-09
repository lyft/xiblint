from xiblint.rules import Rule
from xiblint.xibcontext import XibContext
import glob
import json

class ColorAssets(Rule):
    """
    Ensures cached named colors match the named colors from an asset catalog.

    Example configuration:
    {
      "asset_catalog": "Resources/Color.xcassets"
    }
    """
    def check(self, context):  # type: (XibContext) -> None
        asset_catalog_path = self.config.get('asset_catalog', None)
        if asset_catalog_path is None:
            # TODO: Show an error?
            return

        self.assets = glob.glob("{}/**/*.colorset".format(asset_catalog_path))
        self.cache = {}

        # TODO: Show an error if there aren't any color assets in this asset catalog

        for element in context.tree.findall("./namedColor"):
            name = element.get("name")
            if name is None:
                context.error(element, "Named color is missing a name.")
                continue

            color = self.colors[name]
            if color is None:
                context.error(element, "Named color is missing from asset catalog.")
                continue

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

            if float(red) is not color.red:
                context.error(element, "Color value does not match asset catalog.")

    def load_color(name):
        color = self.colors[name]
        if color is not None:
            return color

        for path in self.assets:
            if path.endswith("{}.colorset".format(name)):
                print("{}/Contents.json".format(path))
                with open("{}/Contents.json".format(path)) as json_file:
                    data = json.load(json_file)
                    components = data["colors"][0]["color"]["components"]
                    color = (load_component(components, "red"), load_component(components, "green"), load_component(components, "blue"), load_component(components, "alpha"))
                    self.colors[name] = color

    def load_component(components, key):
        string = components[key]

        if "." in string:
            return float(string)

        return float(string) / 255.0
