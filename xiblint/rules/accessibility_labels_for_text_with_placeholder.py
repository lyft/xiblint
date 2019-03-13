from xiblint.rules import Rule
from xiblint.xibcontext import XibContext
from xiblint.xibutils import (
    get_view_user_defined_attr,
    view_is_accessibility_element,
)


class AccessibilityLabelsForTextWithPlaceholder(Rule):
    """
    Checks for text fields and text views with a placeholder and no accessibility label.
    A placeholder is not a substitute for an accessibility label, since it's no longer announced
    after the text is edited.
    """
    def check(self, context):  # type: (XibContext) -> None
        for element in context.tree.findall(".//textField") + context.tree.findall(".//textView"):
            placeholder = (element.get('placeholder') if element.tag == 'textField'
                           else get_view_user_defined_attr(element, 'placeholder'))
            if (
                    placeholder is not None and
                    element.find('./accessibility[@label]') is None and
                    view_is_accessibility_element(element) is not False
            ):
                context.error(
                    element,
                    "{} with placeholder text '{}' but no accessibility label",
                    element.tag, element.get('placeholder'))
