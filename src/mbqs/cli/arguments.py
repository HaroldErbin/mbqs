"""
Arguments for the MBQS CLI interface.
"""

import argparse

ARGS_DEFAULT = {
    "verbose": False,
}


def arg_parser():
    """
    Set up the argument parser.
    """

    prog = "mbqs"
    description = "Many-body quantum score CLI."

    # parser for the global options
    # they can be used before or after the action
    global_parser = argparse.ArgumentParser(add_help=False)
    global_arguments(global_parser)

    # root parser of the program
    parser = argparse.ArgumentParser(
        prog=prog, description=description, parents=[global_parser]
    )

    # subparsers for each action
    subparsers = parser.add_subparsers(title="Actions", dest="action")

    protocol_arg_parser(subparsers, parents=[global_parser])
    scorer_arg_parser(subparsers, parents=[global_parser])

    return parser


def protocol_arg_parser(subparsers, parents):
    """
    Set up the argument parser for the protocol action.
    """

    arg_parser = argparse.ArgumentParser(add_help=False)

    parser = subparsers.add_parser(
        "protocol",
        description="""
        Describe the protocol parameters given a state and a system size or a list of
        system sizes.
        """,
        parents=parents + [arg_parser],
    )

    return parser


def scorer_arg_parser(subparsers, parents):
    """
    Set up the argument parser for the scorer action.
    """

    arg_parser = argparse.ArgumentParser(add_help=False)
    parser = subparsers.add_parser(
        "scorer",
        description="""
        Compute MBQS score.
        """,
        parents=parents + [arg_parser],
    )

    return parser


def global_arguments(parser):
    """
    Set up the global arguments.
    """

    control_group = parser.add_argument_group("Control")

    control_group.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=argparse.SUPPRESS,
        help=f"""
        Display more information in the console.
        Default: {ARGS_DEFAULT["verbose"]}
        """,
    )

    return parser
