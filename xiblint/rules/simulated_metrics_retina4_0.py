"""
Ensures simulated metrics are for the iPhone SE, which is currently the smallest display profile.
"""


def check(context):  # type: (xiblint.xibcontext.XibContext) -> None
    root = context.tree.getroot()
    for simulated_screen_metrics in root.findall(".//simulatedScreenMetrics[@key='destination']"):
        if simulated_screen_metrics.get('type') != 'retina4_0.fullscreen':
            context.error(simulated_screen_metrics, 'Simulated metrics ("View As:") must be set to iPhone SE.')
