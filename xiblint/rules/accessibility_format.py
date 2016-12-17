"""
Checks for incorrect use of Lyft extensions `accessibilityFormat` and `accessibilitySources`.
"""
import re

from xiblint.xibutils import get_view_user_defined_attr, view_accessibility_identifier


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
    accessibility_sources_by_id = get_accessibility_sources_by_id(context, view, accessibility_sources)
    accessibility_sources_count = len(accessibility_sources)

    #
    # Ensure accessibilityFormat iff accessibilitySources
    #
    accessibility_format = get_view_user_defined_attr(view, 'accessibilityFormat')
    if accessibility_format is None and accessibility_sources_count != 0:
        context.error(view, "View has {} accessibility source(s) but accessibilityFormat is unset.",
                      accessibility_sources_count)
        return

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
    if expected_accessibility_sources_count == 0 and not re.match(r'.*\[.+?\].*', accessibility_format):
        context.error(view, "No format specifiers in '{}'; use `accessibilityLabel` instead",
                      accessibility_format)
        return

    #
    # Check new format (with [identifier]s)
    #
    unused_sources = set(accessibility_sources)
    for m in re.finditer(r'\[(.+?)\]', accessibility_format):
        identifier = m.group(1)
        if identifier == 'self':
            continue
        source = accessibility_sources_by_id.get(identifier)
        if source is None:
            context.error(view, "Missing accessibility source for identifier {} in {}",
                          identifier,
                          accessibility_format)
        unused_sources -= {source}

    #
    # Check old format (with %@)s
    #
    if len(unused_sources) != expected_accessibility_sources_count:
        context.error(view, "Format string '{}' has {} unused accessibility source(s)",
                      accessibility_format,
                      len(unused_sources))


def get_accessibility_sources_by_id(context, view, accessibility_sources):
    """
    Gets a dictionary of accessibility sources keyed by their 'accessibilityFormatIdentifier'.
    """
    accessibility_sources_by_id = {}
    for source in accessibility_sources:
        accessibility_identifier = view_accessibility_identifier(source)
        accessibility_format_identifier = get_view_user_defined_attr(source, 'accessibilityFormatIdentifier')
        if not accessibility_format_identifier:
            continue
        accessibility_sources_by_id[accessibility_format_identifier] = source
        if accessibility_identifier != accessibility_format_identifier:
            context.error(
                view,
                "View accessibility format identifier '{}' doesn't match accessibility identifier '{}'",
                accessibility_format_identifier,
                accessibility_identifier,
            )
    return accessibility_sources_by_id
