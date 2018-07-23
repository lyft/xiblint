"""
Checks for Trait Variations being enabled.
"""


def check(_, context):  # type: (Dict[str, Any], xiblint.xibcontext.XibContext) -> None
    root = context.tree.getroot()
    if root.get('useTraitCollections') == 'YES' and root.get('targetRuntime') != 'watchKit':
        context.error(root, "Document has 'Use Trait Variations' enabled")
