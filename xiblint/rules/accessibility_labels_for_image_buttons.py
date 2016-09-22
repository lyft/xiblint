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
            state_normal is not None and
            'image' in state_normal.attrib and
            'title' not in state_normal.attrib and
            view_is_accessibility_element(button) is not False and
            not view_accessibility_label(button) and
            not get_view_user_defined_attr(button, 'accessibilityFormat')
        ):
            context.error(button,
                          "Button with image '{}' and no title "
                          "should either have an accessibility label or 'Is Accessibility Element' unchecked",
                          state_normal.get('image'))

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
