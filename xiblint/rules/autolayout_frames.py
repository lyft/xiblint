"""
Checks for ambiguous and misplaced views.
"""

from xiblint.rules import Rule


class AutolayoutFrames(Rule):
    def check(self, context):  # type: (Rule, xiblint.xibcontext.XibContext) -> None
        for element in context.tree.iter():
            if element.get('ambiguous') == 'YES':
                context.error(element, "View with ambiguous constraints")
            elif element.get('misplaced') == 'YES':
                context.error(element, "Misplaced view")
