"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Northern Lights Forecast."""


if __name__ == "__main__":
    main(prog_name="northern-lights-forecast")  # pragma: no cover
