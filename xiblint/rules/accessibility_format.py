import re

from xiblint.rules import Rule
from xiblint.xibcontext import XibContext
from xiblint.xibutils import (
    get_object_id,
    get_view_user_defined_attr,
    view_accessibility_identifier,
)


class AccessibilityFormat(Rule):
    """
    Checks for incorrect use of Lyft extensions `accessibilityFormat` and `accessibilitySources`.
    """
    def check(self, context):  # type: (XibContext) -> None
        views_with_accessibility_format = {
            element.parent.parent
            for element in context.tree.findall(
                ".//userDefinedRuntimeAttributes/userDefinedRuntimeAttribute[@keyPath='accessibilityFormat']")
        }
        views_with_accessibility_sources = {
            element.parent.parent
            for element in context.tree.findall(".//connections/outletCollection[@property='accessibilitySources']")
        }

        for view in views_with_accessibility_format | views_with_accessibility_sources:
            check_view(context, view)


def check_view(context, view):
    accessibility_source_destination_ids = [
        outlet_connection.get('destination') for outlet_connection
        in view.findall("./connections/outletCollection[@property='accessibilitySources']")
    ]

    accessibility_sources = [
        context.tree.find(".//*[@id='{}']".format(destination_id))
        for destination_id in accessibility_source_destination_ids
    ]
    accessibility_sources_count = len(accessibility_sources)

    #
    # Ensure accessibilityFormat iff accessibilitySources
    #
    accessibility_format = get_view_user_defined_attr(view, 'accessibilityFormat')
    if accessibility_format is None and accessibility_sources_count != 0:
        context.error(view, "View has {} accessibility source(s) but accessibilityFormat is unset.",
                      accessibility_sources_count)
        return

    used_identifiers = set(get_accessibility_identifiers(accessibility_format))
    if used_identifiers:
        check_new_format(context, view, accessibility_format, accessibility_sources, used_identifiers)
    else:
        check_old_format(context, view, accessibility_format, accessibility_sources)


def check_old_format(context, view, accessibility_format, accessibility_sources):
    #
    # Check for strange format types (e.g. %d)
    #
    for m in re.finditer(r'%(.)', accessibility_format):
        format_type = m.group(1)
        if format_type not in ['@', '%']:
            context.error(view, "Unexpected format type %{} in accessibility format '{}'", format_type,
                          accessibility_format)

    #
    # Check for accessibilityFormat that could've been a accessibilityLabel
    #
    expected_sources_count = len(re.findall(r'%@', accessibility_format))
    if expected_sources_count == 0 and '[self]' not in accessibility_format:
        context.error(view, "No format specifiers in '{}'; use `accessibilityLabel` instead", accessibility_format)

    #
    # Check old format (with %@-s).
    #
    if len(accessibility_sources) != expected_sources_count:
        context.error(view, "Format string '{}' has has {} format specifiers, but view has {} sources.",
                      accessibility_format, expected_sources_count, len(accessibility_sources))


def check_new_format(context, view, accessibility_format, accessibility_sources, used_identifiers):
    sources_by_id = get_accessibility_sources_by_id(accessibility_sources)
    source_identifiers = set(sources_by_id.keys())
    missing_identifiers = used_identifiers - source_identifiers
    extra_source_identifiers = source_identifiers - used_identifiers
    for identifier in missing_identifiers:
        context.error(view, "Missing accessibility source for identifier '{}' in accessibility format", identifier)
    for identifier in extra_source_identifiers:
        context.error(view, "Unused accessibility source with identifier '{}' in accessibility format", identifier)
    unidentified_sources = set(accessibility_sources) - set(sources_by_id.values())
    for source in unidentified_sources:
        context.error(view, "Accessibility source '{}' missing accessibility identifier", get_object_id(source))
    if '%@' in accessibility_format:
        context.error(view, "New-style accessibility format contains '%@'")


def get_accessibility_identifiers(accessibility_format):
    for m in re.finditer(r'\[(.+?)\]', accessibility_format):
        identifier = m.group(1)
        if identifier != 'self':
            yield identifier


def get_accessibility_sources_by_id(accessibility_sources):
    """
    Gets a dictionary of accessibility sources keyed by their 'accessibilityFormatIdentifier'.
    """
    accessibility_sources_by_id = {}
    for source in accessibility_sources:
        accessibility_identifier = view_accessibility_identifier(source)
        if accessibility_identifier:
            accessibility_sources_by_id[accessibility_identifier] = source
    return accessibility_sources_by_id
