from xiblint.rules import Rule


class AutomationIdentifiers(Rule):
    """
    Makes sure that interactive views have accessibility identifiers, to support testing through UI Automation.
    """
    def check(self, context):  # type: (Rule, xiblint.xibcontext.XibContext) -> None
        for tag in ['button', 'textField', 'textView']:
            for view in context.tree.findall(".//{}".format(tag)):
                if view.find('./accessibility[@identifier]') is None:
                    context.error(view, "{} requires an accessibility identifier for UI Automation", tag)
