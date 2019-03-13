from xiblint.rules import Rule
from xiblint.xibcontext import XibContext


class NoSimulatedMetrics(Rule):
    """
    Ensures there are no `simulatedMetricsContainer`s, which were removed with Xcode 9
    """
    def check(self, context):  # type: (XibContext) -> None
        root = context.tree.getroot()
        for container in root.findall('.//simulatedMetricsContainer'):
            context.error(container, 'SimulatedMetricsContainers should be removed (resave with Xcode 9+)')
