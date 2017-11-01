"""
Ensures simulated metrics are for the iPhone SE, which is currently the smallest display profile.
"""


def check(context):  # type: (xiblint.xibcontext.XibContext) -> None
    root = context.tree.getroot()

    # In Xcode 9 this metadata is in a new place
    device = root.find('device')
    if device is not None and device.get('id') != 'retina4_0':
        context.error(device, 'Simulated metrics ("View As:") must be set to iPhone SE.')
        return

    for simulated_screen_metrics in root.findall(".//simulatedScreenMetrics[@key='destination']"):
        if simulated_screen_metrics.get('type') != 'retina4_0.fullscreen':
            context.error(simulated_screen_metrics, 'Simulated metrics ("View As:") must be set to iPhone SE.')
