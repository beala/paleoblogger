def add_slash_if_missing(filename):
    """Add a slash to the end of a string if it doesn't already have one.
       Handy for URLs, directory paths, etc.
       /usr/sbin -> /usr/sbin/
       /usr/sbin/ -> /usr/sbin/
    """
    stripped = filename.strip()
    if len(stripped) > 0 and stripped[-1] != "/":
        stripped += "/"
    return stripped
