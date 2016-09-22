"""
Makes sure that interactive views have accessibility identifiers, to support testing through UI Automation.
"""


def check(context):  # type: (xiblint.xibcontext.XibContext) -> None
    for tag in ['button', 'textField', 'textView']:
        for view in context.tree.findall(".//{}".format(tag)):
            if view.find('./accessibility[@identifier]') is None:
                context.error(view, "{} requires an accessibility identifier for UI Automation", tag)
