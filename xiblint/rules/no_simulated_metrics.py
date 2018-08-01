from xiblint.rules import Rule


class NoSimulatedMetrics(Rule):
    """
    Ensures there are no `simulatedMetricsContainer`s, which were removed with Xcode 9
    """
    def check(self, context):  # type: (Rule, xiblint.xibcontext.XibContext) -> None
        root = context.tree.getroot()
        for container in root.findall('.//simulatedMetricsContainer'):
            context.error(container, 'SimulatedMetricsContainers should be removed (resave with Xcode 9+)')
