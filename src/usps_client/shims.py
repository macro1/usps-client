try:
    from lxml import etree
except ImportError:
    try:
        import xml.etree.cElementTree as etree  # type: ignore
    except ImportError:
        import xml.etree.ElementTree as etree  # type: ignore
