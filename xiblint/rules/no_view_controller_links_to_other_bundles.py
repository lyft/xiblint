from xiblint.rules import Rule
from xiblint.xibcontext import XibContext


class NoViewControllerLinksToOtherBundles(Rule):
    """
    Ensures there are no links to storyboards in different bundles
    """
    def check(self, context):  # type: (XibContext) -> None
        for element in context.tree.findall(".//viewControllerPlaceholder"):
            if element.get("bundleIdentifier"):
                context.error(element, "Linking to a view controller in another bundle")
