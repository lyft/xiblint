from xiblint.rules import Rule
from xiblint.xibcontext import XibContext


class NoTraitVariations(Rule):
    """
    Checks for Trait Variations being enabled.
    """
    def check(self, context):  # type: (XibContext) -> None
        root = context.tree.getroot()
        if root.get('useTraitCollections') == 'YES' and root.get('targetRuntime') != 'watchKit':
            context.error(root, "Document has 'Use Trait Variations' enabled")
