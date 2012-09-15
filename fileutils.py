def add_slash_if_missing(filename):
    stripped = filename.strip()
    if len(stripped) > 0 and stripped[-1] != "/":
        stripped += "/"
    return stripped
