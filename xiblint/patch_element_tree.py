def patch_element_tree():
    # HACK to ensure cElementTree is not loaded -- we need the pure Python implementation
    import sys
    assert 'xml.etree.ElementTree' not in sys.modules
    sys.modules['_elementtree'] = None  # type: ignore
