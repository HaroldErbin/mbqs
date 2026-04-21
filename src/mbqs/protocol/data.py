"""
Data tools for the MBQS protocol.
"""


def find_data_type(data):
    """
    Find type of protocol data.

    Args:
        data: Data to analyze.

    Returns:
        str: Type of data.

    """

    if not isinstance(data, dict):
        raise TypeError("Data must be a dictionary.")

    if (
        all(isinstance(k, str) for k in data.keys())
        and len(set(len(k) for k in data.keys())) == 1
        and all(isinstance(v, int) for v in data.values())
    ):
        # keys are bitstrings of identical length, values are counts
        return "samples"
    elif all(isinstance(k, tuple) for k in data.keys()) and all(
        isinstance(v, float) for v in data.values()
    ):
        # keys are pairs of indices, values are correlation functions
        return "correlations"
    elif all(isinstance(k, int) for k in data.keys()):
        # keys are system sizes
        # values must be dictionnary of the same type (samples or correlations)
        s = set(find_data_type(v) for v in data.values())

        if len(s) == 1:
            return s.pop() + "_sequence"
        else:
            raise ValueError(f"Cannot work with mixed types: found {s}")

    raise ValueError("Invalid data type")
