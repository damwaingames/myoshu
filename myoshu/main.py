import random
import textwrap

from typing_extensions import Annotated

import typer

from rich import print

from .go import Game

app = typer.Typer()


@app.callback()
def callback() -> None:
    """
    Myoshu (妙手) a CLI for playing Go.
    """


@app.command()
def new(
    boardsize: Annotated[
        int, typer.Option(help="Size of board to create game on.")
    ] = 19,
    p1_name: Annotated[
        str, typer.Option(help="Name of black player.")
    ] = "Black player",
    p2_name: Annotated[
        str, typer.Option(help="Name of white player.")
    ] = "White player",
    handicap: Annotated[
        int, typer.Option(help="Number of handicap stones to be placed.")
    ] = 0,
) -> None:
    """
    Create a new game.
    """
    new_game = Game(boardsize, p1_name, p2_name, handicap)
    print(new_game.board._size)


@app.command()
def proverb() -> None:
    """
    Display a random Go proverb.
    """
    with open("resources/proverbs.txt", "r") as proverbs_file:
        proverbs = proverbs_file.readlines()
        rnd_proverb = proverbs[random.randrange(0, len(proverbs))].strip()
        proverb_length = len(rnd_proverb) if len(rnd_proverb) <= 70 else 70
        print(_full_border(proverb_length))
        print(_empty_row_border(proverb_length))
        print(_proverb_with_border(rnd_proverb))
        print(_empty_row_border(proverb_length))
        print(_full_border(proverb_length))


def _full_border(proverb_length: int) -> str:
    return "[bold red]#" * (proverb_length + 6) + "[/bold red]"


def _empty_row_border(proverb_length: int) -> str:
    return (
        "[bold red]#[/bold red]  " + " " * proverb_length + "  [bold red]#[/bold red]"
    )


def _proverb_with_border(proverb: str) -> str:
    lines = textwrap.wrap(proverb, width=70)
    if len(lines) <= 1:
        return f"[bold red]#[/bold red]  [bright_yellow]{lines[0]}[/bright_yellow]  [bold red]#[/bold red]"
    else:
        proverb = ""
        for line in lines:
            proverb += (
                "[bold red]#[/bold red]  [bright_yellow]"
                + line.ljust(70)
                + "[/bright_yellow]  [bold red]#[/bold red]\n"
            )
        return proverb.strip()
