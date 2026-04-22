"""
Data tools for the MBQS protocol.
"""

from collections.abc import Mapping
from typing import Any, cast


def find_data_type(data: Mapping[str, Any] | Mapping[int, Any]) -> str:
    """
    Find type of protocol data.

    The data can be:
    - samples: dictionary of bitstrings and counts
    - correlations: dictionary of pairs of indices and correlation functions
    - samples_sequence: dictionary of system sizes and samples
    - correlations_sequence: dictionary of system sizes and correlations
    - protocol_samples[_sequence]: dictionary of quench parameters and
      samples[_sequence]
    - protocol_correlations[_sequence]: dictionary of quench parameters and
      correlations[_sequence]

    If the data is of the protocol_* type, returns also the parameters in a separate
    dict.

    Args:
        data: Data to analyze.

    Returns:
        str: Type of data.

    """

    if not isinstance(data, dict):
        raise TypeError("Data must be a dictionary.")

    if (
        all(isinstance(k, str) for k in data.keys())
        and len(set(len(cast(str, k)) for k in data.keys())) == 1
        and all(isinstance(v, int) for v in data.values())
    ):
        # keys are bitstrings of identical length, values are counts
        return "samples"
    elif all(isinstance(k, tuple) for k in data.keys()) and all(
        isinstance(v, float) for v in data.values()
    ):
        # keys are pairs of indices, values are correlation functions
        return "correlations"
    elif "sz" in data.keys() or "szsz" in data.keys() or "szsz_c" in data.keys():
        # keys are named of correlation functions
        return "correlations_dict"
    elif all(isinstance(k, int) for k in data.keys()):
        # keys are system sizes
        # values must be dictionnary of the same type (samples or correlations)
        s = set(find_data_type(v) for v in data.values())

        if len(s) == 1:
            return str(s.pop()) + "_sequence"
        else:
            raise ValueError(f"Cannot work with mixed types: found {s}")
    else:
        if not all(isinstance(k, str) for k in data.keys()):
            raise ValueError("Keys must be strings for protocol data.")

        data_type = "protocol"
        data = cast(dict[str, Any], data)
        if "correlations" in data.keys():
            data_type += "_" + str(find_data_type(data["correlations"]))
        elif "samples" in data.keys():
            data_type += "_" + str(find_data_type(data["samples"]))

        return str(data_type)


def find_protocol_parameters(
    data: Mapping[str, Any] | Mapping[int, Any],
) -> dict[str, Any]:
    """
    Find protocol parameters from a data dict.
    """

    if not isinstance(data, dict):
        raise TypeError("Data must be a dictionary.")

    data = cast(dict[str, Any], data)

    data_type = find_data_type(data)
    if not data_type.startswith("protocol"):
        return {}

    params = dict(data)
    if "correlations" in params:
        del params["correlations"]
    elif "samples" in params:
        del params["samples"]

    return params
