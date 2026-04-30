import pytest

from calculator.cli import main


def test_cli_prints_result(capsys):
    rc = main(["2 + 3 * 4"])
    out = capsys.readouterr()
    assert rc == 0
    assert out.out.strip() == "14"
    assert out.err == ""


def test_cli_joins_multiple_args(capsys):
    rc = main(["2", "+", "3"])
    out = capsys.readouterr()
    assert rc == 0
    assert out.out.strip() == "5"


def test_cli_reports_calculator_error(capsys):
    rc = main(["1 / 0"])
    out = capsys.readouterr()
    assert rc == 2
    assert out.out == ""
    assert "division by zero" in out.err


def test_cli_no_args_exits_nonzero(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main([])
    assert exc_info.value.code != 0
