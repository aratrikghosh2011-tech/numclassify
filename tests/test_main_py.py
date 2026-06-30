"""Test __main__.py entry point."""


def test_main_runs_no_args(monkeypatch):
    """Call main() with no args should print footer and exit 0."""
    import sys
    from numclassify.cli import main
    monkeypatch.setattr(sys, 'argv', ['numclassify'])
    try:
        main()
    except SystemExit as e:
        assert e.code == 0 or e.code is None


def test_main_runs_check(monkeypatch, capsys):
    """Call main() with check 7."""
    import sys
    from numclassify.cli import main
    monkeypatch.setattr(sys, 'argv', ['numclassify', 'check', '7'])
    try:
        main()
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert '7' in captured.out
