def urljoin(*args):
    """
    Joins given arguments into an url. Trailing but not leading slashes are
    stripped for each argument.
    """

    return '/'.join(map(lambda x: str(x).rstrip('/'), args)) + '/'


def find_element_position(lst: list, element: str):
    try:
        return lst.index(element)
    except ValueError:
        return None
