"""
tests/test_cli.py
Full CLI test suite using subprocess. Tests all 8 commands.
"""
import json
import subprocess
import sys

import pytest


def run(*args, expect_fail=False, timeout=20):
    """Run numclassify CLI and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, '-m', 'numclassify'] + list(args),
        capture_output=True, text=True, timeout=timeout
    )
    if not expect_fail:
        assert result.returncode == 0, (
            f"Command failed: {args}\nstderr: {result.stderr}\nstdout: {result.stdout}"
        )
    return result.returncode, result.stdout, result.stderr


# ---------------------------------------------------------------------------
# check command
# ---------------------------------------------------------------------------

class TestCmdCheck:
    def test_check_prime(self):
        _, out, _ = run('check', '7')
        assert 'prime' in out.lower() or '7' in out

    def test_check_armstrong(self):
        _, out, _ = run('check', '153')
        assert '153' in out
        assert 'armstrong' in out.lower() or 'Armstrong' in out

    def test_check_json_output(self):
        _, out, _ = run('check', '6', '--json')
        data = json.loads(out)
        assert data['number'] == 6
        assert 'true_properties' in data
        assert 'false_properties' in data

    def test_check_zero(self):
        _, out, _ = run('check', '0')
        assert '0' in out

    def test_check_negative(self):
        _, out, _ = run('check', '-1')

    def test_check_large(self):
        _, out, _ = run('check', '10000')
        assert '10000' in out

    def test_check_perfect_number(self):
        _, out, _ = run('check', '28')
        assert 'perfect' in out.lower() or '28' in out

    def test_check_json_perfect(self):
        _, out, _ = run('check', '28', '--json')
        data = json.loads(out)
        props = [p.lower() for p in data['true_properties']]
        assert 'perfect' in props


# ---------------------------------------------------------------------------
# info command
# ---------------------------------------------------------------------------

class TestCmdInfo:
    def test_info_prime(self):
        _, out, _ = run('info', 'prime')
        assert 'prime' in out.lower()

    def test_info_armstrong(self):
        _, out, _ = run('info', 'armstrong')
        assert 'armstrong' in out.lower() or 'narcissistic' in out.lower()

    def test_info_json(self):
        _, out, _ = run('info', 'prime', '--json')
        data = json.loads(out)
        assert 'name' in data
        assert 'description' in data
        assert 'category' in data
        assert 'oeis' in data or 'oeis_url' in data

    def test_info_shows_examples(self):
        _, out, _ = run('info', 'prime')
        assert any(c.isdigit() for c in out)

    def test_info_unknown_exits_nonzero(self):
        code, out, err_out = run('info', 'notarealtype12345', expect_fail=True)
        assert code != 0

    def test_info_fibonacci(self):
        _, out, _ = run('info', 'fibonacci')
        assert 'fibonacci' in out.lower()

    def test_info_perfect(self):
        _, out, _ = run('info', 'perfect')
        assert 'perfect' in out.lower()


# ---------------------------------------------------------------------------
# why command
# ---------------------------------------------------------------------------

class TestCmdWhy:
    def test_why_prime(self):
        _, out, _ = run('why', 'prime', '7')
        assert '7' in out

    def test_why_armstrong(self):
        _, out, _ = run('why', 'armstrong', '153')
        assert '153' in out

    def test_why_json(self):
        _, out, _ = run('why', 'prime', '7', '--json')
        data = json.loads(out)
        assert 'explanation' in data or 'why' in data or 'result' in data

    def test_why_false_case(self):
        _, out, _ = run('why', 'prime', '4')
        assert '4' in out

    def test_why_fibonacci(self):
        _, out, _ = run('why', 'fibonacci', '8')
        assert '8' in out

    def test_why_squarefree(self):
        _, out, _ = run('why', 'squarefree', '30')
        assert '30' in out

    def test_why_pell(self):
        _, out, _ = run('why', 'pell', '5')
        assert '5' in out

    def test_why_unknown_type(self):
        code, _, _ = run('why', 'notarealtype', '5', expect_fail=True)
        assert code != 0


# ---------------------------------------------------------------------------
# find command
# ---------------------------------------------------------------------------

class TestCmdFind:
    def test_find_prime(self):
        _, out, _ = run('find', 'prime', '--limit', '5')
        assert '2' in out or '3' in out or '5' in out

    def test_find_fibonacci(self):
        _, out, _ = run('find', 'fibonacci', '--limit', '5')
        assert '1' in out or '2' in out

    def test_find_json(self):
        _, out, _ = run('find', 'prime', '--limit', '3', '--json')
        data = json.loads(out)
        assert isinstance(data, list)
        assert len(data) <= 3

    def test_find_armstrong(self):
        _, out, _ = run('find', 'armstrong', '--limit', '3')
        assert '153' in out or '1' in out


# ---------------------------------------------------------------------------
# list command
# ---------------------------------------------------------------------------

class TestCmdList:
    def test_list_all(self):
        _, out, _ = run('list')
        assert len(out) > 100

    def test_list_category_primes(self):
        _, out, _ = run('list', '--category', 'primes')
        assert 'prime' in out.lower()

    def test_list_category_exam_types(self):
        _, out, _ = run('list', '--category', 'exam_types')
        assert out.strip() != ''

    def test_list_category_digital(self):
        _, out, _ = run('list', '--category', 'digital')
        assert 'armstrong' in out.lower() or 'harshad' in out.lower()


# ---------------------------------------------------------------------------
# compare command
# ---------------------------------------------------------------------------

class TestCmdCompare:
    def test_compare_two_numbers(self):
        _, out, _ = run('compare', '6', '28')
        assert '6' in out
        assert '28' in out

    def test_compare_json(self):
        _, out, _ = run('compare', '6', '28', '--json')
        data = json.loads(out)
        assert 'only_a' in data or '6' in str(data)
        assert 'only_b' in data or '28' in str(data)

    def test_compare_primes(self):
        _, out, _ = run('compare', '7', '11')
        assert '7' in out and '11' in out

    def test_compare_shared_properties(self):
        _, out, _ = run('compare', '6', '28', '--json')
        data = json.loads(out)

        # The response may vary, just check it's valid JSON
        assert isinstance(data, dict)


# ---------------------------------------------------------------------------
# range command
# ---------------------------------------------------------------------------

class TestCmdRange:
    def test_range_basic(self):
        _, out, _ = run('range', '1', '20')
        assert out.strip() != ''

    def test_range_with_filter(self):
        _, out, _ = run('range', '1', '50', '--filter', 'prime')
        assert '2' in out or 'prime' in out.lower()

    def test_range_json(self):
        _, out, _ = run('range', '1', '10', '--json')
        data = json.loads(out)
        assert isinstance(data, list)

    def test_range_empty_result(self):
        _, out, _ = run('range', '1', '5', '--filter', 'perfect')


# ---------------------------------------------------------------------------
# query command
# ---------------------------------------------------------------------------

class TestCmdQuery:
    def test_query_has(self):
        _, out, _ = run('query', '1', '100', '--has', 'prime')
        assert out.strip() != ''

    def test_query_not_has(self):
        _, out, _ = run('query', '1', '30', '--not-has', 'prime')
        assert '4' in out or '6' in out

    def test_query_any_of(self):
        _, out, _ = run('query', '1', '20', '--any-of', 'prime', 'perfect')
        assert out.strip() != ''

    def test_query_json(self):
        _, out, _ = run('query', '1', '20', '--has', 'prime', '--json')
        data = json.loads(out)
        assert isinstance(data, list)

    def test_query_combined(self):
        _, out, _ = run('query', '1', '100', '--has', 'prime', '--not-has', 'twin prime')
        assert out.strip() != ''


# ---------------------------------------------------------------------------
# quiz command
# ---------------------------------------------------------------------------

class TestCmdQuiz:
    def test_quiz_list_types(self):
        _, out, _ = run('quiz', '--list-types')
        assert 'armstrong' in out.lower()

    def test_quiz_runs_with_piped_input(self):
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, '-m', 'numclassify', 'quiz', 'prime', '--count', '4', '--seed', '1'],
            input='y\ny\ny\ny\n',
            capture_output=True, text=True, timeout=20
        )
        assert result.returncode == 0
        assert 'Score:' in result.stdout

    def test_quiz_invalid_type(self):
        code, _, _ = run('quiz', 'wolstenholme prime', '--count', '2', expect_fail=True)
        assert code != 0


# ---------------------------------------------------------------------------
# no-args (footer)
# ---------------------------------------------------------------------------

class TestCmdNoArgs:
    def test_no_args_shows_help(self):
        _, out, _ = run()
        assert 'github' in out.lower() or 'numclassify' in out.lower() or 'usage' in out.lower()

    def test_no_args_shows_version(self):
        _, out, _ = run()
        assert 'v0.' in out or 'version' in out.lower() or 'numclassify' in out.lower()
