"""Unit tests for cli_parser.py.

Tests cover build_parser(), resolve_defaults(), handle_args(), and main()
using pytest. Naming convention: test_<function_name>_<test_number>.

Run with:
    pytest test_cli_parser.py -v
    pytest test_cli_parser.py -v --cov=cli_parser --cov-report=term-missing
"""

import argparse
import sys
from unittest.mock import patch, call
from gct.lib.utils import SUCCESS

import pytest

from gct.lib import cli_parser
from gct.lib.cli_parser import (
    build_parser,
    resolve_defaults,
    handle_args,
    main,
    DEFAULT_COPY_DEST,
    DEFAULT_CREATE_DIR,
    DEFAULT_MERGE_DEST,
)


@pytest.fixture
def dir_path(tmp_path):
    src_path = tmp_path / "source"
    src_path.mkdir()
    return src_path


@pytest.fixture
def fake_path(tmp_path):
    fake_path = tmp_path / "not_created"
    return fake_path


@pytest.fixture
def txt_file_1(dir_path):
    f_path = dir_path / "test_1.txt"
    f_path.write_text(
        "This is a test text file.\n"
        "This is the second sentence.\n"
        "This is the third sencentce.\n"
    )
    return f_path


@pytest.fixture
def txt_file_2(dir_path):
    f_path = dir_path / "test_1.txt"
    f_path.write_text(
        "This is a test text file 2.\n"
        "Hello World.\n"
        "This should work or I will be sad\n"
    )
    return f_path


# ──────────────────────────────────────────────────────────────────────────────
# build_parser()
# ──────────────────────────────────────────────────────────────────────────────


class TestBuildParser:

    def test_build_parser_1_returns_argument_parser(self):
        """Return value is an ArgumentParser instance."""
        parser = build_parser()
        assert isinstance(parser, argparse.ArgumentParser)

    def test_build_parser_2_prog_name(self):
        """Parser prog is set to 'mytool'."""
        parser = build_parser()
        assert parser.prog == "mytool"

    def test_build_parser_3_interactive_flag_default_false(self):
        """--interactive defaults to False when not supplied."""
        parser = build_parser()
        args = parser.parse_args([])
        assert args.interactive is False

    def test_build_parser_4_interactive_short_flag(self):
        """-i sets interactive to True."""
        parser = build_parser()
        args = parser.parse_args(["-i"])
        assert args.interactive is True

    def test_build_parser_5_interactive_long_flag(self):
        """--interactive sets interactive to True."""
        parser = build_parser()
        args = parser.parse_args(["--interactive"])
        assert args.interactive is True

    def test_build_parser_6_no_subcommand_sets_command_none(self):
        """args.command is None when no subcommand is given."""
        parser = build_parser()
        args = parser.parse_args([])
        assert args.command is None

    # copy / cp ----------------------------------------------------------------

    def test_build_parser_7_copy_src_required(self):
        """copy exits with error when -s/--src is missing."""
        parser = build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["copy"])

    def test_build_parser_8_copy_src_parsed(self):
        """copy -s stores the source path correctly."""
        parser = build_parser()
        args = parser.parse_args(["copy", "-s", "/src/file.txt"])
        assert args.src == "/src/file.txt"

    def test_build_parser_9_copy_dest_defaults_to_none(self):
        """copy -d omitted leaves dest as None."""
        parser = build_parser()
        args = parser.parse_args(["copy", "-s", "/src/file.txt"])
        assert args.dest is None

    def test_build_parser_10_copy_dest_parsed(self):
        """copy -d stores the destination path correctly."""
        parser = build_parser()
        args = parser.parse_args(["copy", "-s", "/src/file.txt", "-d", "/dst/"])
        assert args.dest == "/dst/"

    def test_build_parser_11_copy_alias_cp(self):
        """'cp' alias parses identically to 'copy'."""
        parser = build_parser()
        args = parser.parse_args(["cp", "-s", "/src/file.txt"])
        assert args.src == "/src/file.txt"

    def test_build_parser_12_copy_command_name(self):
        """args.command is 'copy' when using the copy subcommand."""
        parser = build_parser()
        args = parser.parse_args(["copy", "-s", "/src/file.txt"])
        assert args.command == "copy"

    def test_build_parser_13_copy_long_flags(self):
        """copy --src and --dest long-form flags are parsed correctly."""
        parser = build_parser()
        args = parser.parse_args(["copy", "--src", "/src/file.txt", "--dest", "/dst/"])
        assert args.src == "/src/file.txt"
        assert args.dest == "/dst/"

    # mkfile / mkf -------------------------------------------------------------

    def test_build_parser_14_mkfile_name_required(self):
        """mkfile exits with error when -n/--name is missing."""
        parser = build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["mkfile"])

    def test_build_parser_15_mkfile_name_parsed(self):
        """mkfile -n stores the filename correctly."""
        parser = build_parser()
        args = parser.parse_args(["mkfile", "-n", "report.csv"])
        assert args.name == "report.csv"

    def test_build_parser_16_mkfile_dir_defaults_to_none(self):
        """mkfile -d omitted leaves dir as None."""

    def test_build_parser_17_mkfile_dir_parsed(self):
        """mkfile -d stores the directory correctly."""
        parser = build_parser()
        args = parser.parse_args(["mkfile", "-n", "report.csv", "-d", "/output/"])
        assert args.dir == "/output/"

    def test_build_parser_18_mkfile_alias_mkf(self):
        """'mkf' alias parses identically to 'mkfile'."""
        parser = build_parser()
        args = parser.parse_args(["mkf", "-n", "config.json"])
        assert args.name == "config.json"

    def test_build_parser_19_mkfile_command_name(self):
        """args.command is 'mkfile' when using the mkfile subcommand."""
        parser = build_parser()
        args = parser.parse_args(["mkfile", "-n", "report.csv"])
        assert args.command == "mkfile"

    # merge / combine ----------------------------------------------------------

    def test_build_parser_20_merge_file_a_required(self):
        """merge exits with error when -a/--file-a is missing."""
        parser = build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["merge", "-f2", "b.txt"])

    def test_build_parser_21_merge_file_b_required(self):
        """merge exits with error when -b/--file-b is missing."""
        parser = build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["merge", "-f1", "a.txt"])

    def test_build_parser_23_merge_all_required_flags_parsed(self):
        """merge stores file_a, file_b, and name correctly."""
        parser = build_parser()
        args = parser.parse_args(["merge", "-f1", "a.txt", "-f2", "b.txt"])
        assert args.file_1 == "a.txt"
        assert args.file_2 == "b.txt"

    def test_build_parser_24_merge_dest_dir_defaults_to_none(self):
        """merge -d omitted leaves dest_dir as None."""
        parser = build_parser()
        args = parser.parse_args(["merge", "-f1", "a.txt", "-f2", "b.txt"])
        assert args.dest_dir is None

    def test_build_parser_25_merge_dest_dir_parsed(self):
        """merge -d stores the destination directory correctly."""
        parser = build_parser()
        args = parser.parse_args(
            ["merge", "-f1", "a.txt", "-f2", "b.txt", "-d", "/out/"]
        )
        assert args.dest_dir == "/out/"

    def test_build_parser_26_merge_alias_combine(self):
        """'combine' alias parses identically to 'merge'."""
        parser = build_parser()
        args = parser.parse_args(["combine", "-f1", "a.txt", "-f2", "b.txt"])
        assert args.file_1 == "a.txt"

    def test_build_parser_27_merge_command_name(self):
        """args.command is 'merge' when using the merge subcommand."""
        parser = build_parser()
        args = parser.parse_args(["merge", "-f1", "a.txt", "-f2", "b.txt"])
        assert args.command == "merge"


# ──────────────────────────────────────────────────────────────────────────────
# resolve_defaults()
# ──────────────────────────────────────────────────────────────────────────────


class TestResolveDefaults:

    def test_resolve_defaults_1_copy_dest_none_becomes_default(self):
        """copy with dest=None is replaced by DEFAULT_COPY_DEST."""
        args = argparse.Namespace(command="copy", src="/src/file.txt", dest=None)
        result = resolve_defaults(args)
        assert result.dest == DEFAULT_COPY_DEST

    def test_resolve_defaults_2_copy_dest_explicit_unchanged(self):
        """copy with an explicit dest is not overwritten."""
        args = argparse.Namespace(
            command="copy", src="/src/file.txt", dest="/custom/dest"
        )
        result = resolve_defaults(args)
        assert result.dest == "/custom/dest"

    def test_resolve_defaults_3_copy_alias_cp_dest_none_becomes_default(self):
        """cp alias with dest=None is also replaced by DEFAULT_COPY_DEST."""
        args = argparse.Namespace(command="cp", src="/src/file.txt", dest=None)
        result = resolve_defaults(args)
        assert result.dest == DEFAULT_COPY_DEST

    def test_resolve_defaults_4_mkfile_dir_none_becomes_default(self):
        """mkfile with dir=None is replaced by DEFAULT_CREATE_DIR."""
        args = argparse.Namespace(command="mkfile", name="report.csv", dir=None)
        result = resolve_defaults(args)
        assert result.dir == DEFAULT_CREATE_DIR

    def test_resolve_defaults_5_mkfile_dir_explicit_unchanged(self):
        """mkfile with an explicit dir is not overwritten."""
        args = argparse.Namespace(
            command="mkfile", name="report.csv", dir="/custom/dir"
        )
        result = resolve_defaults(args)
        assert result.dir == "/custom/dir"

    def test_resolve_defaults_6_mkfile_alias_mkf_dir_none_becomes_default(self):
        """mkf alias with dir=None is also replaced by DEFAULT_CREATE_DIR."""
        args = argparse.Namespace(command="mkf", name="report.csv", dir=None)
        result = resolve_defaults(args)
        assert result.dir == DEFAULT_CREATE_DIR

    def test_resolve_defaults_7_merge_dest_dir_none_becomes_default(self):
        """merge with dest_dir=None is replaced by DEFAULT_MERGE_DEST."""
        args = argparse.Namespace(
            command="merge",
            file_a="a.txt",
            file_b="b.txt",
            name="out.txt",
            dest_dir=None,
        )
        result = resolve_defaults(args)
        assert result.dest_dir == DEFAULT_MERGE_DEST

    def test_resolve_defaults_8_merge_dest_dir_explicit_unchanged(self):
        """merge with an explicit dest_dir is not overwritten."""
        args = argparse.Namespace(
            command="merge",
            file_a="a.txt",
            file_b="b.txt",
            name="out.txt",
            dest_dir="/out/",
        )
        result = resolve_defaults(args)
        assert result.dest_dir == "/out/"

    def test_resolve_defaults_9_merge_alias_combine_dest_dir_none_becomes_default(self):
        """combine alias with dest_dir=None is also replaced by DEFAULT_MERGE_DEST."""
        args = argparse.Namespace(
            command="combine",
            file_a="a.txt",
            file_b="b.txt",
            name="out.txt",
            dest_dir=None,
        )
        result = resolve_defaults(args)
        assert result.dest_dir == DEFAULT_MERGE_DEST

    def test_resolve_defaults_10_unknown_command_namespace_unchanged(self):
        """An unrecognised command leaves the namespace untouched."""
        args = argparse.Namespace(command="unknown")
        result = resolve_defaults(args)
        assert result.command == "unknown"

    def test_resolve_defaults_11_returns_same_namespace_object(self):
        """resolve_defaults returns the same Namespace object (mutates in place)."""
        args = argparse.Namespace(command="copy", src="/src/file.txt", dest=None)
        result = resolve_defaults(args)
        assert result is args


# ──────────────────────────────────────────────────────────────────────────────
# handle_args()
# ──────────────────────────────────────────────────────────────────────────────


class TestHandleArgs:

    def test_handle_args_3_no_command_no_interactive_calls_sys_exit(self):
        """No subcommand and no --interactive triggers sys.exit(0)."""
        args = argparse.Namespace(interactive=False, command=None)
        with pytest.raises(SystemExit) as exc_info:
            handle_args(args)
            assert exc_info.value.code == 0

    def test_handle_args_4_no_command_no_interactive_prints_help(self, capsys):
        """No subcommand and no --interactive prints help text to stdout."""
        args = argparse.Namespace(interactive=False, command=None)
        with pytest.raises(SystemExit):
            handle_args(args)
            captured = capsys.readouterr()
            assert "usage" in captured.out.lower()

    # def test_handle_args_5_copy_prints_correct_output(self, capsys):
    #     """copy command prints src and resolved dest."""
    #     args = argparse.Namespace(
    #     interactive=False, command="copy", src="/src/file.txt", dest="/dst/"
    #     )
    #     handle_args(args)
    #     captured = capsys.readouterr()
    #     assert "/src/file.txt" in captured.out
    #     assert "/dst/" in captured.out

    # def test_handle_args_6_copy_dest_none_resolved_to_default(self, capsys):
    #     """copy with dest=None resolves to DEFAULT_COPY_DEST before printing."""
    #     args = argparse.Namespace(
    #     interactive=False, command="copy", src="/src/file.txt", dest=None
    #     )
    #     handle_args(args)
    #     captured = capsys.readouterr()
    #     assert str(DEFAULT_COPY_DEST) in captured.out

    # def test_handle_args_7_copy_alias_cp_prints_correct_output(self, capsys):
    #     """cp alias routes to the copy handler."""
    #     args = argparse.Namespace(
    #     interactive=False, command="cp", src="/src/file.txt", dest="/dst/"
    #     )
    #     handle_args(args)
    #     captured = capsys.readouterr()
    #     assert "[copy]" in captured.out

    def test_handle_args_8_mkfile_prints_correct_output(self, capsys, monkeypatch):
        """mkfile command prints filename and resolved directory."""
        args = argparse.Namespace(
            interactive=False, command="mkfile", name="report.csv", dir="output/"
        )
        monkeypatch.setattr("builtins.input", lambda _: "yes")
        handle_args(args)
        captured = capsys.readouterr()
        exp_out = f"{SUCCESS}: file: report.csv was created at: output."
        assert exp_out == captured.out.strip()

    def test_handle_args_9_mkfile_dir_none_resolved_to_default(
        self, capsys, monkeypatch
    ):
        """mkfile with dir=None resolves to DEFAULT_CREATE_DIR before printing."""
        args = argparse.Namespace(
            interactive=False, command="mkfile", name="report.csv", dir=None
        )
        monkeypatch.setattr("builtins.input", lambda _: "yes")
        handle_args(args)
        captured = capsys.readouterr()
        assert str(DEFAULT_CREATE_DIR) in captured.out

    def test_handle_args_10_mkfile_alias_mkf_prints_correct_output(
        self, capsys, monkeypatch
    ):
        """mkf alias routes to the mkfile handler."""
        args = argparse.Namespace(
            interactive=False, command="mkf", name="config.json", dir="output/"
        )
        monkeypatch.setattr("builtins.input", lambda _: "yes")
        handle_args(args)
        captured = capsys.readouterr()
        exp_out = f"{SUCCESS}: file: config.json was created at: output."
        assert exp_out in captured.out.strip()

    def test_handle_args_12_merge_dest_dir_none_resolved_to_default(
        self, capsys, txt_file_1, txt_file_2
    ):
        """merge with dest_dir=None resolves to DEFAULT_MERGE_DEST before printing."""
        args = argparse.Namespace(
            interactive=False,
            command="merge",
            file_1=txt_file_1,
            file_2=txt_file_2,
            dest_dir=None,
        )
        handle_args(args)
        captured = capsys.readouterr()
        assert str(DEFAULT_MERGE_DEST) in captured.out

    def test_handle_args_13_merge_alias_combine_prints_correct_output(
        self, capsys, txt_file_1, txt_file_2
    ):
        """combine alias routes to the merge handler."""
        args = argparse.Namespace(
            interactive=False,
            command="combine",
            file_1=txt_file_1,
            file_2=txt_file_2,
            dest_dir="/out/",
        )
        handle_args(args)
        captured = capsys.readouterr()
        exp_out = f"{SUCCESS}: The files were merged. The merged file is located here:"
        assert exp_out in captured.out.strip()


# ──────────────────────────────────────────────────────────────────────────────
# main()
# ──────────────────────────────────────────────────────────────────────────────


class TestMain:

    def test_main_1_calls_handle_args(self):
        """main() calls handle_args() exactly once."""
        with patch.object(sys, "argv", ["mytool", "-i"]):
            with patch("gct.lib.cli_parser.handle_args") as mock_handle:
                main()
                mock_handle.assert_called_once()

    def test_main_2_passes_parsed_namespace_to_handle_args(self):
        """main() passes an argparse.Namespace to handle_args()."""
        with patch.object(sys, "argv", ["mytool", "-i"]):
            with patch("gct.lib.cli_parser.handle_args") as mock_handle:
                main()
                passed_arg = mock_handle.call_args[0][0]
                assert isinstance(passed_arg, argparse.Namespace)

    def test_main_3_interactive_flag_propagates(self):
        """main() with -i passes interactive=True to handle_args()."""
        with patch.object(sys, "argv", ["mytool", "-i"]):
            with patch("gct.lib.cli_parser.handle_args") as mock_handle:
                main()
                passed_arg = mock_handle.call_args[0][0]
                assert passed_arg.interactive is True

    def test_main_4_copy_subcommand_propagates(self):
        """main() with copy subcommand passes command='copy' to handle_args()."""
        with patch.object(sys, "argv", ["mytool", "copy", "-s", "/src/file.txt"]):
            with patch("gct.lib.cli_parser.handle_args") as mock_handle:
                main()
                passed_arg = mock_handle.call_args[0][0]
                assert passed_arg.command == "copy"
                assert passed_arg.src == "/src/file.txt"
