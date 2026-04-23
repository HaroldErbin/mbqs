"""
Arguments for the MBQS CLI interface.
"""

import argparse

ARGS_DEFAULT = {
    "verbose": False,
    "J": 1.0,
    "state": "down",
    "include_rydberg": False,
    "level": 60,
    "a": None,
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
    correlations_arg_parser(subparsers, parents=[global_parser])

    return parser


def physical_arguments(parser, required=True, single_L=False):
    """
    Add physical arguments to the parser.
    """

    parser.add_argument(
        "--state",
        "-s",
        type=str,
        choices=["down", "plus"],
        default=ARGS_DEFAULT["state"],
        help=f"""
        Initial state for the protocol.
        Default: {ARGS_DEFAULT["state"]}
        """,
    )

    group = parser.add_mutually_exclusive_group()

    group.add_argument(
        "-J",
        type=float,
        default=None,
        help=f"""
        Ising coupling.
        Default: {ARGS_DEFAULT["J"]}.
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

    if single_L:
        parser.add_argument(
            "-L",
            type=int,
            required=required,
            help="""
            System size: number of qubits.
            Default: None.
            """,
        )
    else:
        parser.add_argument(
            "-L",
            type=int,
            nargs="+",
            required=required,
            help="""
            System size(s): number(s) of qubits.
            Can be a single number or a list.
            """,
        )

    return parser


def input_output_arguments(
    parser, input_required=False, output_required=False, remove_input=False
):
    """
    Add input and output arguments to the parser.
    """

    if remove_input is False:
        parser.add_argument(
            "--input",
            "-i",
            type=str,
            default=None,
            required=input_required,
            help="""
            Path to input JSON file.
            Default: None.
            """,
        )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=None,
        required=output_required,
        help="""
        Path to output JSON file.
        Default: None.
        """,
    )


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
        The protocol can be saved as a JSON file with `-o`. In this case, the protocol
        is not printed to the console except if verbose is true.
        """,
        parents=parents + [arg_parser],
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

    physical_arguments(parser)
    input_output_arguments(parser, remove_input=True)

    return parser


def correlations_arg_parser(subparsers, parents):
    """
    Set up the argument parser for the correlations action.
    """

    arg_parser = argparse.ArgumentParser(add_help=False)

    parser = subparsers.add_parser(
        "correlations",
        description="""
        Compute correlation functions. If physical parameters are provided, it computes
        the correlations at the surge time by performing the quench in the Ising
        Hamiltonian. If a JSON file of samples is provided, it computes the correlations
        from the bitstring counts.
        """,
        parents=parents + [arg_parser],
    )

    physical_arguments(parser, required=False, single_L=True)
    input_output_arguments(parser)

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

    parser.add_argument(
        "--threshold",
        type=float,
        default=None,
        help="""
        Threshold for the MBQS score.
        Default: None.
        """,
    )

    physical_arguments(parser, required=False, single_L=True)
    input_output_arguments(parser, input_required=True)

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
