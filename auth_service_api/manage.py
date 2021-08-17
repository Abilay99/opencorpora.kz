import click
from flask.cli import with_appcontext


@click.group()
def cli():
    """Main entry point"""


@cli.command("init")
@with_appcontext
def init():
    """Create a new admin user"""
    from auth_service_api.extensions import db
    from auth_service_api.models import Users

    click.echo("create user")
    user = Users(
        full_name="Abylay Satybaldiev",
        mobile="7777777777",
        bin="990721000154",
        email="nba_abilay.99@mail.ru",
        password="admin123"
    )
    db.session.add(user)
    db.session.commit()
    click.echo("created user admin")


if __name__ == "__main__":
    cli()
