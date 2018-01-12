from lxml import etree

def true_false(value):
    return 'true' if value else 'false'

def attach_element(elm, name, value, fmt=None, attrs={}):
    subElm = etree.SubElement(elm, name, **attrs)
    if callable(fmt):
        subElm.text = fmt(value)
    elif fmt:
        subElm.text = fmt.format(value)
    else:
        subElm.text = value

def attach_optional_element(elm, name, value, fmt=None):
    if value is None:
        return
    attach_element(elm, name, value, fmt=None)


