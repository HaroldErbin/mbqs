"""
CLI action to describe the parameters of the MBQS protocol.
"""

import json
import os
from pathlib import Path
from typing import Any, cast

from mbqs import MBQSProtocol, RydbergMapping
from mbqs.cli.arguments import ARGS_DEFAULT

header = "# MBQS protocol\n"

protocol_text = [
    "J = {J:.4g} rad / µs",
    "State = {state}",
]

size_text = [
    "L = {L}",
    "Time = {time:.4g} µs",
    "Correlation indices: {corr_idx}",
]

rydberg_text = [
    "Level = {level}",
    "a = {a:.4g} µm",
]

pulses_text = [
    "Ω = {Omega:.4g} rad / µs",
    "δ = {delta:.4g} rad / µs",
]


def join_with_prefix(text_list: list[str], prefix: str) -> str:
    """
    Join a list of strings with a prefix for each item.
    """

    return "\n".join([prefix + text for text in text_list])


def combine_text(protocol_data: dict) -> str:
    """
    Combine the texts for one or several protocols.
    """

    text = header + "\n"
    text += "\n".join(protocol_text).format(**protocol_data)

    if "rydberg" in protocol_data:
        text += "\n\nRydberg data\n"
        text += join_with_prefix(rydberg_text, "- ").format(**protocol_data["rydberg"])

    if "sizes" in protocol_data:
        for size_data in protocol_data["sizes"]:
            text += "\n\n## "
            text += join_with_prefix(size_text, "- ")[2:].format(**size_data)
            if "pulses" in size_data:
                text += "\n- Pulses:\n"
                text += join_with_prefix(pulses_text, "  - ").format(
                    **size_data["pulses"]
                )

    return text


def combine_text_single(protocol_data: dict) -> str:
    """
    Combine the texts for one or several protocols.
    """

    text = header + "\n"
    text += join_with_prefix(protocol_text, "- ").format(**protocol_data)
    text += "\n"
    text += join_with_prefix(size_text, "- ").format(**protocol_data)

    if "rydberg" in protocol_data:
        text += "\n- Rydberg data:\n"
        text += join_with_prefix(rydberg_text, "  - ").format(
            **protocol_data["rydberg"]
        )
        text += "\n"
        text += join_with_prefix(pulses_text, "  - ").format(**protocol_data["pulses"])

    return text


def protocol_action(args):
    """
    Execute the protocol action.
    """

    if args.L[0] == 1:
        raise ValueError("System size must be >= 2.")

    if args.output is not None and args.verbose is False:
        display_on_cli = False
    else:
        display_on_cli = True

    include_rydberg = (
        args.include_rydberg or args.a is not None or args.level is not None
    )

    level = args.level if args.level is not None else ARGS_DEFAULT["level"]
    level = cast(int, level)

    if args.J is None and args.a is None:
        args.J = cast(float, ARGS_DEFAULT["J"])

    if args.a is not None:
        J = RydbergMapping.compute_J(args.a, level)
    else:
        J = args.J

    protocol_data: dict[str, Any] = {"J": J, "state": args.state, "sizes": []}

    if include_rydberg is True:
        if args.a is None:
            a = RydbergMapping.compute_a(J, level)
        else:
            a = args.a

        protocol_data["rydberg"] = {"level": level, "a": a}

    for L in args.L:
        definition_data = MBQSProtocol(state=args.state, L=L, J=J).summary
        size_data = {
            "L": L,
            "time": definition_data["time"],
            "corr_idx": definition_data["corr_idx"],
        }

        if args.a is not None:
            rydberg_data = RydbergMapping(L=L, a=args.a, level=level).summary
        else:
            rydberg_data = RydbergMapping(L=L, J=J, level=level).summary

        if include_rydberg:
            size_data["pulses"] = {
                "Omega": rydberg_data["Omega"],
                "delta": rydberg_data["delta"],
            }

        protocol_data["sizes"].append(size_data)

    if len(args.L) == 1:
        size_data = protocol_data.pop("sizes")[0]
        protocol_data.update(size_data)

    if display_on_cli is True:
        if len(args.L) == 1:
            text = combine_text_single(protocol_data)
        else:
            text = combine_text(protocol_data)
        print(text)

    if args.output is not None:
        json_path = Path(args.output)

        with open(json_path, "w") as f:
            json.dump(protocol_data, f, indent=4)

    return os.EX_OK
