import typer
from gfr.commands import hello, create, init, addmicro

# Create the main Typer application
app = typer.Typer(
    name="ggg",
    help="Git Flow Assistant of Rahmasir (gfr) helps with git and GitHub workflows.",
    add_completion=False,
)

# Add subcommands from the commands module
app.add_typer(hello.app, name="hello")
app.add_typer(create.app, name="create")
app.add_typer(init.app, name="init")
app.add_typer(addmicro.app, name="addmicro")
app.add_typer(addmicro.app, name="am")

if __name__ == "__main__":
    app()
