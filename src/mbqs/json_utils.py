"""
Utility functions for JSON encoding and decoding.
"""


def json_encode_keys(data):
    """
    Recursively encode keys of a dictionary to strings (JSON-compatible).

    Args:
        data: Dictionary to encode.

    Returns:
        Dictionary with encoded keys.

    """
    conv = {}

    if not isinstance(data, dict):
        return data

    for k, v in data.items():
        if isinstance(k, tuple):
            k = str(k)

        conv[k] = json_encode_keys(v)

    return conv


def json_decode_keys(data):
    """
    Recursively decode keys from JSON data to a dictionary from strings.

    Args:
        data: Dictionary to decode.

    Returns:
        Dictionary with decoded keys.

    """

    def check_bitstring(k):
        return k.isdecimal() and all(c in "01" for c in k)

    def convert_key(k):
        if k.isdecimal():
            k = int(k)
        elif k.replace(".", "", 1).isdecimal():
            # if key is made of numbers and at mot one period, then it's a float
            # the period can be at the start or end of string and still be a valid float
            k = float(k)
        elif k[0] == "(" and k[-1] == ")" and "," in k:
            # if key starts and ends with parenthesis and contains comma, assume that it's a tuple
            # we convert the elements of the tuple using the same function
            k = tuple(map(convert_key, k[1:-1].split(", ")))
        elif k[0] == "'" and k[-1] == "'":
            # key is a string with redundant quotes, which must be removed
            # this happens for elements of a tuple
            k = k[1:-1]

        return k

    if not isinstance(data, dict):
        return data

    if all(len(k) >= 2 and check_bitstring(k) for k in data.keys()):
        # check if all keys are bitstrings; in that case, we keep them as strings
        # we assume that length is at least 2 to avoid problems with 0 and 1
        return {k: json_decode_keys(v) for k, v in data.items()}
    else:
        return {convert_key(k): json_decode_keys(v) for k, v in data.items()}
