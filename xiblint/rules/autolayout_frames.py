from xiblint.rules import Rule
from xiblint.xibcontext import XibContext


class AutolayoutFrames(Rule):
    """
    Checks for ambiguous and misplaced views.
    """
    def check(self, context):  # type: (XibContext) -> None
        for element in context.tree.iter():
            if element.get('ambiguous') == 'YES':
                context.error(element, "View with ambiguous constraints")
            elif element.get('misplaced') == 'YES':
                context.error(element, "Misplaced view")
