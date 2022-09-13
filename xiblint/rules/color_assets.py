from xiblint.rules import Rule
from xiblint.xibcontext import XibContext
import glob
import json


class ColorAssets(Rule):
    def __init__(self, config):
        asset_catalog_path = config.get("asset_catalog", None)
        if asset_catalog_path is None:
            raise SystemExit(
                "error: Asset catalog not found. Please configure 'asset_catalog'.",
            )

        self.assets = glob.glob("{}/**/*.colorset".format(asset_catalog_path))

        if not self.assets:
            raise SystemExit(
                "error: Failed to load asset catalog at: '{}'".format(
                    asset_catalog_path,
                ),
            )

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
            if not name:
                context.error(element, "Named color is missing a name.")
                continue

            expected_color = self._load_color(name)
            if not expected_color:
                context.error(
                    element,
                    "Named color '{}' is missing from asset catalog.".format(name),
                )
                continue

            color_element = element.find("color")
            if color_element is None:
                context.error(
                    element,
                    "Named color '{}' is missing color definition.".format(name),
                )
                continue

            red = color_element.get("red")
            green = color_element.get("green")
            blue = color_element.get("blue")
            alpha = color_element.get("alpha")
            if not all([red, green, blue, alpha]):
                context.error(
                    element, "Named color '{}' has invalid color value.".format(name),
                )
                continue

            color = (float(red), float(green), float(blue), float(alpha))

            if not self._compare_colors(color, expected_color):
                print(color, expected_color)
                context.error(
                    element,
                    "Color value for '{}' does not match asset catalog.".format(name),
                )

    def _load_color(self, name):
        if name in self.colors:
            return self.colors[name]

        for path in self.assets:
            if not path.endswith("{}.colorset".format(name)):
                continue

            with open("{}/Contents.json".format(path)) as json_file:
                data = json.load(json_file)
                color = self._load_components(data["colors"][0]["color"]["components"])
                self.colors[name] = color
                return color

    def _load_components(self, components):
        return (
            self._load_component(components, "red"),
            self._load_component(components, "green"),
            self._load_component(components, "blue"),
            self._load_component(components, "alpha"),
        )

    def _load_component(self, components, key):
        string = components[key]

        if "." in string:
            return float(string)

        return float(string) / 255.0

    def _compare_colors(self, lhs, rhs):
        # Compare with only 4 decimal places
        return all(format(left, ".4f") == format(right, ".4f") for left, right in zip(lhs, rhs))
