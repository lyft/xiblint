from xiblint.rules import Rule
from xiblint.xibcontext import XibContext

ALLOWED_DEVICES = [
    'retina4_0',
    'watch38',
]


class SimulatedMetricsRetina40(Rule):
    """
    Ensures simulated metrics are for the iPhone SE or a 38mm watch
    which are currently the smallest display profiles.
    """
    def check(self, context):  # type: (XibContext) -> None
        root = context.tree.getroot()

        # In Xcode 9 this metadata is in a new place
        device = root.find('device')
        if device is not None and device.get('id') not in ALLOWED_DEVICES:
            context.error(
                device,
                'Simulated metrics ("View As:") must be one of: {}'
                .format(', '.join(ALLOWED_DEVICES)))
