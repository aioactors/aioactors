#!/usr/bin/env python
from tomlkit import dumps as toml_dump, load as toml_load
from yaml import safe_load as yaml_loads

from app_cli import Cli, Command, echo


def create_cli() -> Cli:

    cli = Cli(__file__)
    cli.add_command('get-version', get_version())
    cli.add_command('update-poetry', update_poetry())

    return cli


def get_version() -> Command:

    def _version():
        with open(".config/meta.yml", encoding="utf-8") as meta:
            project = yaml_loads(meta)
            echo(project['version'])

    return Command(
        name='get-version',
        callback=_version,
        help="Print current version of application"
    )


def update_poetry() -> Command:

    def _update():
        with open("pyproject.toml") as pyproject:
            project: dict = toml_load(pyproject)

        poetry = project['tool']['poetry']

        with open(".config/meta.yml", encoding="utf-8") as f_meta:
            meta = yaml_loads(f_meta)
            poetry['name'] = meta['name']
            poetry['description'] = meta['description']
            poetry['repository'] = meta['link']
            poetry['authors'] = meta['authors']
            poetry['dependencies'] = meta.get('deps', {})
            poetry['dev-dependencies'] = meta.get('dev', {})

            if poetry.get('group') is None:
                poetry['group'] = {
                    'linter': {
                        'dependencies': {}
                    }
                }
            poetry['group']['linter']['dependencies'] = meta.get('linters', {}).get('types', {})

        with open("pyproject.toml", "w") as pyproject:
            pyproject.write(toml_dump(project))

    return Command(
        name='update-poetry',
        callback=_update,
        help="Update poetry in pyproject.toml"
    )


if __name__ == '__main__':
    create_cli().start()
