import typer


app = typer.Typer()


@app.callback()
def callback() -> None:
    """
    Myoshu (妙手) a CLI for playing Go.
    """
