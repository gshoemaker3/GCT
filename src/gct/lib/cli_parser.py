"""CLI argument parsing for mytool.

This module defines and wires up all command-line arguments and subcommands
for mytool using Python's built-in argparse library.

Supported modes and commands:
    -i / --interactive: Launch the tool in interactive mode.
    copy (cp):          Copy a file from a source path to a destination path.
    mkfile (mkf):       Create a new file at an optional directory path.
    merge (combine):    Merge two source files into a single new output file.

Typical usage:
    python mytool.py --interactive
    python mytool.py copy -s /src/file.txt -d /dst/
    python mytool.py mkfile -n report.csv -d /output/
    python mytool.py merge -a file1.txt -b file2.txt -n merged.txt
"""

import argparse
import sys
import os
from pathlib import Path

from gct.lib import files, interactive

DEFAULT_COPY_DEST = Path(os.getcwd()) / "files"  # Replace with your actual default
DEFAULT_CREATE_DIR = Path(os.getcwd()) / "files"  # Replace with your actual default
DEFAULT_MERGE_DEST = Path(os.getcwd()) / "files"  # Replace with your actual default


def build_parser() -> argparse.ArgumentParser:
    """Build and return the top-level argument parser for mytool.

    Constructs the main ArgumentParser along with all subparsers for the
    supported subcommands: copy/cp, mkfile/mkf, and merge/combine. Also
    registers the top-level --interactive flag.

    Returns:
        argparse.ArgumentParser: The fully configured argument parser, ready
            to be used by calling .parse_args() on it.
    """
    parser = argparse.ArgumentParser(
        prog="mytool",
        description="A CLI tool with interactive mode, file copying, creation, and merging.",
    )

    # ── 1. Interactive mode flag ──────────────────────────────────────────────
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Launch the tool in interactive mode.",
    )

    subparsers = parser.add_subparsers(dest="command", metavar="COMMAND")

    # ── 2. copy / cp ──────────────────────────────────────────────────────────
    copy_parser = subparsers.add_parser(
        "copy",
        aliases=["cp"],
        help="Copy a file from a source path to a destination path.",
    )
    copy_parser.add_argument(
        "-s",
        "--src",
        required=True,
        metavar="SOURCE",
        help="Path of the file to copy.",
    )
    copy_parser.add_argument(
        "-d",
        "--dest",
        default=None,  # None signals 'use the tool default'
        metavar="DESTINATION",
        help=(
            "Destination path for the copied file. "
            f"Defaults to '{DEFAULT_COPY_DEST}' when omitted."
        ),
    )

    # ── 3. mkfile / mkf ───────────────────────────────────────────────────────
    mkfile_parser = subparsers.add_parser(
        "mkfile",
        aliases=["mkf"],
        help="Create a new file.",
    )
    mkfile_parser.add_argument(
        "-n",
        "--name",
        required=True,
        metavar="FILENAME",
        help="Name of the new file, including its extension (e.g. report.txt).",
    )
    mkfile_parser.add_argument(
        "-d",
        "--dir",
        default=None,
        metavar="DIRECTORY",
        help=(
            "Directory in which the file will be created. "
            f"Defaults to '{DEFAULT_CREATE_DIR}' when omitted."
        ),
    )

    # ── 4. merge / combine ────────────────────────────────────────────────────
    merge_parser = subparsers.add_parser(
        "merge",
        aliases=["combine"],
        help="Merge two files into a single new file.",
    )
    merge_parser.add_argument(
        "-f1",
        "--file-1",
        required=True,
        metavar="FILE_A",
        help="Path to the first source file.",
    )
    merge_parser.add_argument(
        "-f2",
        "--file-2",
        required=True,
        metavar="FILE_B",
        help="Path to the second source file.",
    )
    merge_parser.add_argument(
        "-n",
        "--name",
        # required=True,
        metavar="OUTPUT_NAME",
        help="Name of the merged output file, including its extension.",
    )
    merge_parser.add_argument(
        "-d",
        "--dest-dir",
        default=None,
        metavar="DEST_DIR",
        help=(
            "Directory where the merged file will be saved. "
            f"Defaults to '{DEFAULT_MERGE_DEST}' when omitted."
        ),
    )

    return parser


def resolve_defaults(args: argparse.Namespace) -> argparse.Namespace:
    """Fill in default paths for any optional arguments not supplied by the user.

    Inspects the parsed subcommand and replaces any None-valued path arguments
    with the appropriate tool-level default constant. This keeps default
    resolution separate from parser definitions for clarity.

    Args:
        args (argparse.Namespace): The namespace object returned by
            ArgumentParser.parse_args(), potentially containing None values
            for optional path arguments.

    Returns:
        argparse.Namespace: The same namespace object with all None path
            values replaced by their corresponding default constants.
    """
    if args.command in ("copy", "cp"):
        if args.dest is None:
            args.dest = DEFAULT_COPY_DEST

    elif args.command in ("mkfile", "mkf"):
        if args.dir is None:
            args.dir = DEFAULT_CREATE_DIR

    elif args.command in ("merge", "combine"):
        if args.dest_dir is None:
            args.dest_dir = DEFAULT_MERGE_DEST

    return args


def handle_args(args: argparse.Namespace) -> None:
    """Route parsed arguments to the appropriate command handler.

    Checks for interactive mode first, then dispatches to the correct
    subcommand branch based on args.command. If neither --interactive nor
    a subcommand is provided, the help text is printed and the program exits.
    resolve_defaults() is called before dispatch to ensure all path arguments
    have concrete values.

    Args:
        args (argparse.Namespace): The namespace object returned by
            ArgumentParser.parse_args(), fully populated with all flags
            and subcommand arguments.

    Returns:
        None
    """

    # Interactive mode can coexist with a subcommand, or stand alone.
    if args.interactive:
        print("[interactive mode]")
        interactive.run()
        return

    if args.command is None:
        # No subcommand and no --interactive: show help.
        build_parser().print_help()
        sys.exit(0)

    args = resolve_defaults(args)

    if args.command in ("copy", "cp"):
        print(f"[copy] {args.src!r}  →  {args.dest!r}")
        files.copy_file(args.interactive, args.src, args.dest)

    elif args.command in ("mkfile", "mkf"):
        files.create_file(args.interactive, args.name, args.dir)

    elif args.command in ("merge", "combine"):
        files.merge_files(args.interactive, args.file_1, args.file_2)


def main() -> None:
    """Entry point for the mytool CLI.

    Builds the argument parser, parses arguments from sys.argv, and delegates
    to handle_args() for routing and execution. Intended to be called directly
    when the module is run as a script or invoked via a console_scripts entry
    point.

    Returns:
        None
    """
    parser = build_parser()
    args = parser.parse_args()
    handle_args(args)


def run() -> None:
    main()
