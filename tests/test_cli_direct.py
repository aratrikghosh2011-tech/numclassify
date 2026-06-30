"""Direct unit tests for numclassify.cli functions (no subprocess)."""
import argparse
import json
from io import StringIO
import sys

import pytest

from numclassify.cli import (
    build_parser,
    _normalize,
    _resolve_type,
    _computed_extras,
    _c, _bold, _green, _red, _yellow, _cyan,
    _check_mark, _rule,
)


class TestHelpers:
    def test_normalize(self):
        assert _normalize("Twin Prime") == "twin_prime"
        assert _normalize("  Fibonacci  ") == "fibonacci"
        assert _normalize("look-and-say") == "look_and_say"

    def test_resolve_type_known(self):
        from numclassify._registry import REGISTRY
        key = _resolve_type("prime", REGISTRY)
        assert key == "prime"

    def test_resolve_type_unknown_dies(self):
        from numclassify._registry import REGISTRY
        with pytest.raises(SystemExit):
            _resolve_type("nonexistent_xyz", REGISTRY)

    def test_computed_extras(self):
        extras = _computed_extras(153)
        assert 'digit_sum' in extras
        assert 'digital_root' in extras
        assert 'num_divisors' in extras
        assert extras['digit_sum'] == 9
        assert extras['digital_root'] == 9

    def test_computed_extras_zero(self):
        extras = _computed_extras(0)
        assert isinstance(extras, dict)

    def test_computed_extras_negative(self):
        extras = _computed_extras(-10)
        assert isinstance(extras, dict)


class TestAnsiHelpers:
    def test_c_no_color(self):
        assert _c("hello", 1) == "hello"

    def test_bold_no_color(self):
        assert _bold("x") == "x"

    def test_green_no_color(self):
        assert _green("x") == "x"

    def test_red_no_color(self):
        assert _red("x") == "x"

    def test_yellow_no_color(self):
        assert _yellow("x") == "x"

    def test_cyan_no_color(self):
        assert _cyan("x") == "x"

    def test_check_mark_returns_yes(self):
        assert _check_mark() == "[YES]"

    def test_rule_default(self):
        r = _rule(5)
        assert r == "-----"


class TestBuildParser:
    def test_parser_has_commands(self):
        parser = build_parser()
        subactions = parser._subparsers._group_actions
        assert len(subactions) == 1
        choices = subactions[0].choices
        for cmd in ['check', 'info', 'why', 'find', 'list', 'compare', 'range', 'query']:
            assert cmd in choices, f"Missing command: {cmd}"

    def test_parser_check_defaults(self):
        parser = build_parser()
        args = parser.parse_args(['check', '42'])
        assert args.command == 'check'
        assert args.number == '42'
        assert args.json is False
        assert args.full is False

    def test_parser_check_json_flag(self):
        parser = build_parser()
        args = parser.parse_args(['check', '6', '--json'])
        assert args.json is True

    def test_parser_why_requires_n(self):
        parser = build_parser()
        args = parser.parse_args(['why', 'prime', '7'])
        assert args.command == 'why'
        assert args.type_name == 'prime'
        assert args.n == 7

    def test_parser_find_limit_default(self):
        parser = build_parser()
        args = parser.parse_args(['find', 'prime'])
        assert args.limit == 20

    def test_parser_find_limit_custom(self):
        parser = build_parser()
        args = parser.parse_args(['find', 'armstrong', '--limit', '5'])
        assert args.limit == 5

    def test_parser_query_has(self):
        parser = build_parser()
        args = parser.parse_args(['query', '1', '100', '--has', 'prime', 'fibonacci'])
        assert args.has == ['prime', 'fibonacci']


class TestCmdCheckDirect:
    def test_cmd_check_default(self, capsys):
        from numclassify.cli import cmd_check
        parser = build_parser()
        args = parser.parse_args(['check', '7'])
        cmd_check(args)
        captured = capsys.readouterr()
        assert '7' in captured.out

    def test_cmd_check_json(self, capsys):
        from numclassify.cli import cmd_check
        parser = build_parser()
        args = parser.parse_args(['check', '6', '--json'])
        cmd_check(args)
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data['number'] == 6
        assert 'true_properties' in data
        assert 'false_properties' in data

    def test_cmd_info_json(self, capsys):
        from numclassify.cli import cmd_info
        parser = build_parser()
        args = parser.parse_args(['info', 'prime', '--json'])
        cmd_info(args)
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data['name'] == 'Prime'
        assert 'description' in data

    def test_cmd_compare_json(self, capsys):
        from numclassify.cli import cmd_compare
        parser = build_parser()
        args = parser.parse_args(['compare', '6', '28', '--json'])
        cmd_compare(args)
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert 'shared' in data
        assert 'only_a' in data
        assert 'only_b' in data

    def test_cmd_query_json(self, capsys):
        from numclassify.cli import cmd_query
        parser = build_parser()
        args = parser.parse_args(['query', '1', '20', '--has', 'prime', '--json'])
        cmd_query(args)
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert isinstance(data, list)
        assert 2 in data

    def test_cmd_find_json(self, capsys):
        from numclassify.cli import cmd_find
        parser = build_parser()
        args = parser.parse_args(['find', 'prime', '--limit', '3', '--json'])
        cmd_find(args)
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert isinstance(data, list)
        assert len(data) <= 3

    def test_cmd_range_json(self, capsys):
        from numclassify.cli import cmd_range
        parser = build_parser()
        args = parser.parse_args(['range', '1', '10', '--json'])
        cmd_range(args)
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert isinstance(data, list)

    def test_cmd_range_with_filter(self, capsys):
        from numclassify.cli import cmd_range
        parser = build_parser()
        args = parser.parse_args(['range', '1', '20', '--filter', 'prime'])
        cmd_range(args)
        captured = capsys.readouterr()
        assert 'prime' in captured.out.lower() or '2' in captured.out


class TestCmdInfoDirect:
    def test_cmd_info_shows_examples(self, capsys):
        from numclassify.cli import cmd_info
        parser = build_parser()
        args = parser.parse_args(['info', 'prime'])
        cmd_info(args)
        captured = capsys.readouterr()
        assert 'Examples' in captured.out or '2' in captured.out
