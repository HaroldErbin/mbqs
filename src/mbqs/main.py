"""
Main entry point for the MBQS CLI.
"""

import os

from mbqs.cli.arguments import arg_parser
from mbqs.cli.protocol import protocol_action


def main() -> int:
    """
    Entry point for the MBQS command line interface.
    """

    parser = arg_parser()
    args = parser.parse_args()

    code = os.EX_OK

    match args.action:
        case "protocol":
            code = protocol_action(args)
        case "scorer":
            # code = scorer_action(args)
            raise NotImplementedError
        case _:
            parser.print_help()

    return code


if __name__ == "__main__":
    main()
