from tarotteller import cli


def run_cli(args):
    return cli.main(args)


def test_cli_list_major(capsys):
    exit_code = run_cli(["list", "--arcana", "major", "--limit", "3"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Cards in deck" in captured.out
    assert "The Fool" in captured.out


def test_cli_info(capsys):
    exit_code = run_cli(["info", "The Magician"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "The Magician" in captured.out
    assert "Arcana : Major" in captured.out


def test_cli_draw_cards(capsys):
    exit_code = run_cli([
        "draw",
        "--cards",
        "2",
        "--seed",
        "5",
        "--no-reversed",
    ])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Card 1:" in captured.out
    assert "(upright)" in captured.out
