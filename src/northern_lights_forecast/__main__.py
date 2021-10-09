"""Command-line interface."""
import click

import northern_lights_forecast.northern_lights as nl


@click.command()
@click.version_option()
def main() -> None:
    """Northern Lights Forecast."""
    nl.main()


if __name__ == "__main__":
    main(prog_name="northern-lights-forecast")  # pragma: no cover
