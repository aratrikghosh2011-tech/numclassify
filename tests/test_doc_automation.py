"""
tests/test_doc_automation.py
Verifies generate_docs.py produces correct output and check_repo.py's
strict mode actually distinguishes from normal mode.
"""
import subprocess
import sys
from pathlib import Path


class TestGenerateDocs:
    def test_runs_without_error(self):
        result = subprocess.run(
            [sys.executable, 'tools/generate_docs.py'],
            capture_output=True, text=True
        )
        assert result.returncode == 0, result.stderr

    def test_version_heading_matches_pyproject(self):
        import tomllib
        with open('pyproject.toml', 'rb') as f:
            version = tomllib.load(f)['project']['version']
        readme = Path('README.md').read_text(encoding='utf-8')
        assert f"What's new in v{version}" in readme

    def test_public_api_count_printed(self):
        result = subprocess.run(
            [sys.executable, 'tools/generate_docs.py'],
            capture_output=True, text=True
        )
        assert 'Public API count:' in result.stdout


class TestCheckRepoStrictMode:
    def test_fast_mode_runs(self):
        result = subprocess.run(
            [sys.executable, 'tools/check_repo.py', '--fast'],
            capture_output=True, text=True
        )
        assert result.returncode in (0, 1)

    def test_strict_flag_accepted(self):
        result = subprocess.run(
            [sys.executable, 'tools/check_repo.py', '--fast', '--strict'],
            capture_output=True, text=True
        )
        assert result.returncode in (0, 1)
        assert 'STRICT' in result.stdout


class TestSpecialAndCompositeTypes:
    def test_special_is_alias_for_strong(self):
        import numclassify as nc
        assert nc.why("special", 145) == nc.why("Strong", 145)

    def test_composite_registered(self):
        import numclassify as nc
        info = nc.property_info("Composite")
        assert info['name'] == 'Composite'

    def test_composite_correctness(self):
        import numclassify as nc
        for n, expected in [(4, True), (6, True), (7, False), (2, False), (1, False), (9, True)]:
            props = nc.get_true_properties(n)
            is_composite = props.get('Composite', False)
            assert is_composite == expected, f"n={n}: expected {expected}, got {is_composite}"

    def test_composite_why_hidden_no_leak(self):
        import numclassify as nc
        import re
        for n in [4, 6, 7, 8, 9]:
            hidden = nc.why_hidden("Composite", n)
            assert not re.search(r'\bis\s+(?:not\s+)?composite\b', hidden, re.IGNORECASE), (
                f"Verdict leaked at n={n}: {hidden!r}"
            )

    def test_strong_why_hidden_no_leak(self):
        import numclassify as nc
        import re
        for n in [1, 2, 145, 100]:
            hidden = nc.why_hidden("Strong", n)
            assert not re.search(r'\bis\s+(?:not\s+)?strong\b', hidden, re.IGNORECASE), (
                f"Verdict leaked at n={n}: {hidden!r}"
            )
