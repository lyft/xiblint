"""
Checks for image buttons with no accessibility label.
In this case, VoiceOver will announce the image asset's name, which might be unwanted.
"""
from xiblint.xibutils import (
    view_is_accessibility_element,
    view_accessibility_label,
    get_view_user_defined_attr,
)


def check(context):  # type: (xiblint.xibcontext.XibContext) -> None
    for button in context.tree.findall(".//button"):
        state_normal = button.find("./state[@key='normal']")
        if (
            state_normal is None or
            'title' in state_normal.attrib or
            view_is_accessibility_element(button) is False or
            view_accessibility_label(button) or
            get_view_user_defined_attr(button, 'accessibilityFormat')
        ):
            continue

        if 'image' in state_normal.attrib:
            context.error(button,
                          "Button with image '{}' and no title; "
                          "should either have an accessibility label or 'Accessibility Enabled' unchecked",
                          state_normal.attrib['image'])

        if 'backgroundImage' in state_normal.attrib:
            context.error(button,
                          "Button with background image '{}' and no title "
                          "should either have an accessibility label or 'Accessibility Enabled' unchecked",
                          state_normal.attrib['backgroundImage'])

    # For barButtonItem, we expect use of a LyftUI extension
    for bar_button_item in context.tree.findall(".//barButtonItem"):
        if (
            'image' in bar_button_item.attrib and
            'title' not in bar_button_item.attrib and
            get_view_user_defined_attr(bar_button_item, 'voiceoverLabel') is None
        ):
            context.error(bar_button_item,
                          "Bar button item with image {} and no title "
                          "should have a user-defined `voiceoverLabel` attribute", bar_button_item.get('image'))
