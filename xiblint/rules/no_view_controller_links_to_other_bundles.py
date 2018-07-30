"""
Ensures there are no links to storyboards in different bundles
"""

from xiblint.rules import Rule


class NoViewControllerLinksToOtherBundles(Rule):
    def check(self, context):  # type: (Rule, xiblint.xibcontext.XibContext) -> None
        for element in context.tree.findall(".//viewControllerPlaceholder"):
            if element.get("bundleIdentifier"):
                context.error(element, "Linking to a view controller in another bundle")
