"""
Checks for ambiguous and misplaced views.
"""


def check(_, context):  # type: (Dict[str, Any], xiblint.xibcontext.XibContext) -> None
    for element in context.tree.iter():
        if element.get('ambiguous') == 'YES':
            context.error(element, "View with ambiguous constraints")
        elif element.get('misplaced') == 'YES':
            context.error(element, "Misplaced view")
