"""
Main entry point for the MBQS CLI.
"""

import json
import os
from pathlib import Path
from typing import cast

from mbqs import MBQSProtocol, RydbergMapping
from mbqs.cli.arguments import ARGS_DEFAULT, arg_parser
from mbqs.cli.display import combine_text, combine_text_single


def main() -> int:
    """Entry point for the MBQS command line interface."""
    parser = arg_parser()
    args = parser.parse_args()

    code = os.EX_OK

    match args.action:
        case "protocol":
            code = protocol_action(args)
        case "scorer":
            code = scorer_action(args)
        case _:
            parser.print_help()

    return code


def protocol_action(args):
    """
    Execute the protocol action.
    """

    if args.json is not None and args.verbose is False:
        display_on_cli = False
    else:
        display_on_cli = True

    include_rydberg = (
        args.include_rydberg or args.a is not None or args.level is not None
    )

    level = args.level if args.level is not None else ARGS_DEFAULT["level"]
    level = cast(int, level)

    if args.a is not None:
        J = RydbergMapping.compute_J(args.a, level)
    else:
        J = args.J

    protocol_data = {"J": J, "state": args.state, "sizes": []}

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

    if args.json is not None:
        json_path = Path(args.json)

        with open(json_path, "w") as f:
            json.dump(protocol_data, f, indent=4)

    return os.EX_OK


def scorer_action(args):
    """
    Execute the scorer action.
    """

    raise NotImplementedError


if __name__ == "__main__":
    main()
