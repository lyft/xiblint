"""
Checks for labels with outlets into a view controller that have no accessibility identifiers.
Labels with outlets might get dynamic text, and therefore should be accessible to UI testing.
"""


def check(_, context):  # type: (Dict[str, Any], xiblint.xibcontext.XibContext) -> None
    for outlet in context.tree.findall(".//viewController/connections/outlet"):
        destination = outlet.get('destination')
        label = context.tree.find(".//label[@id='{}']".format(destination))
        if label is None:
            continue
        if label.find('./accessibility[@identifier]') is not None:
            continue
        context.error(label,
                      "Label with text '{}' has an outlet into the view controller "
                      "so it requires an accessibility identifier",
                      label.get('text'),
                      label.tag)
