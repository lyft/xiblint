"""
Checks for incorrect use of Lyft extensions `accessibilityFormat` and `accessibilitySources`.
"""
import re

from xiblint.xibutils import get_view_user_defined_attr


def check(context):  # type: (xiblint.xibcontext.XibContext) -> None
    views_with_accessibility_format = {
        element.parent.parent
        for element in context.tree.findall(
            ".//userDefinedRuntimeAttributes/userDefinedRuntimeAttribute[@keyPath='accessibilityFormat']")
    }
    views_with_accessibility_sources = {
        element.parent.parent
        for element in context.tree.findall(".//connections/outletCollection[@property='accessibilitySources']")
    }

    for view in views_with_accessibility_format.union(views_with_accessibility_sources):
        accessibility_sources_count = len([
            element for element in view.findall("./connections/outletCollection[@property='accessibilitySources']")
        ])

        accessibility_format = get_view_user_defined_attr(view, 'accessibilityFormat')
        if accessibility_format is None and accessibility_sources_count != 0:
            context.error(view, "View has {} accessibility source(s) but accessibilityFormat is unset.",
                          accessibility_sources_count)
            continue

        #
        # Check for strange format types (e.g. %d)
        #
        for m in re.finditer(r'%(.)', accessibility_format):
            format_type = m.group(1)
            if format_type not in ['@', '%']:
                context.error(view, "Unexpected format type %{} in accessibility format {}", format_type,
                              accessibility_format)

        #
        # Check for accessibilityFormat that could've been a accessibilityLabel
        #
        expected_accessibility_sources_count = len(re.findall(r'%@', accessibility_format))
        if expected_accessibility_sources_count == 0 and '[self' not in accessibility_format:
            context.error(view, "No format specifiers in '{}'; use `accessibilityLabel` instead",
                          accessibility_format)

        #
        # Check for mismatching format vs. sources
        #
        if accessibility_sources_count != expected_accessibility_sources_count:
            context.error(view, "Format string '{}' has {} `%@`-specifiers but view has {} accessibility source(s)",
                          accessibility_format, expected_accessibility_sources_count, accessibility_sources_count)
