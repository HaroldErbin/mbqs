"""
Arguments for the MBQS CLI interface.
"""

import argparse

ARGS_DEFAULT = {
    "verbose": False,
    "state": "down",
    "include_rydberg": False,
    "level": 60,
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

    parser.add_argument(
        "--state",
        type=str,
        choices=["down", "plus"],
        default=ARGS_DEFAULT["state"],
        help=f"""
        Initial state for the protocol.
        Default: {ARGS_DEFAULT["state"]}
        """,
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "-J",
        type=float,
        default=None,
        help="""
        Ising coupling.
        Default: None.
        """,
    )

    group.add_argument(
        "-a",
        metavar="a",
        type=float,
        default=None,
        help="""
        Interatomic distance.
        Default: None.
        """,
    )

    parser.add_argument(
        "--level",
        type=int,
        default=None,
        help=f"""
        Rydberg level.
        Default: {ARGS_DEFAULT["level"]}
        """,
    )

    parser.add_argument(
        "--include-rydberg",
        action="store_true",
        default=ARGS_DEFAULT["include_rydberg"],
        help=f"""
        Include Rydberg parameters in the output.
        Default: {ARGS_DEFAULT["include_rydberg"]}
        """,
    )

    parser.add_argument(
        "-L",
        type=int,
        nargs="+",
        required=True,
        help="""
        System size(s): number(s) of qubits.
        Can be a single number or a list.
        """,
    )

    parser.add_argument(
        "--json",
        type=str,
        default=None,
        help="""
        Output the protocol as a JSON file. In this case, the protocol is not printed
        to the console except if verbose is true.
        """,
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
        default=ARGS_DEFAULT["verbose"],
        help=f"""
        Display more information in the console.
        Default: {ARGS_DEFAULT["verbose"]}
        """,
    )

    return parser
