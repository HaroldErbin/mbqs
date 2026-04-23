#!/usr/bin/env python
# PYTHON_ARGCOMPLETE_OK

"""
Main entry point for the MBQS CLI.
"""

import os

import argcomplete

from mbqs.cli.arguments import arg_parser
from mbqs.cli.correlations import correlations_action
from mbqs.cli.protocol import protocol_action
from mbqs.cli.scorer import scorer_action


def main() -> int:
    """
    Entry point for the MBQS command line interface.
    """

    parser = arg_parser()
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    code = os.EX_OK

    match args.action:
        case "protocol":
            code = protocol_action(args)
        case "correlations":
            code = correlations_action(args)
        case "scorer":
            code = scorer_action(args)
        case _:
            parser.print_help()

    return code


if __name__ == "__main__":
    main()
