from xiblint.rules import Rule
from xiblint.xibcontext import XibContext


class AutomationIdentifiers(Rule):
    """
    Makes sure that interactive views have accessibility identifiers, to support testing through UI Automation.
    """
    def check(self, context):  # type: (XibContext) -> None
        for tag in ['button', 'textField', 'textView']:
            for view in context.tree.findall(".//{}".format(tag)):
                if view.find('./accessibility[@identifier]') is None:
                    context.error(view, "{} requires an accessibility identifier for UI Automation", tag)
