"""
Main entry point for the MBQS CLI.
"""

from .cli.arguments import arg_parser


def main() -> None:
    """Entry point for the MBQS command line interface."""
    parser = arg_parser()
    args = parser.parse_args()

    if args.action is None:
        parser.print_help()
        return

    if args.action == "protocol":
        print("Protocol action")
    elif args.action == "scorer":
        print("Scorer action")


if __name__ == "__main__":
    main()
