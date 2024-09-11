#!/usr/bin/env python
from pathlib import Path

from app_cli import Cli, Command, echo
from tomlkit import dumps as toml_dump
from tomlkit import load as toml_load
from yaml import safe_load as yaml_loads


def create_cli() -> Cli:
    cli = Cli(__file__)
    cli.add_command("get-version", get_version())
    cli.add_command("update-poetry", update_poetry())

    return cli


def get_version() -> Command:
    def _version() -> None:
        with Path(".config/meta.yml").open(encoding="utf-8") as meta:
            project = yaml_loads(meta)
            echo(project["version"])

    return Command(
        name="get-version",
        callback=_version,
        help="Print current version of application",
    )


def update_poetry() -> Command:
    def _update() -> None:
        with Path("pyproject.toml").open(encoding="utf-8") as pyproject:
            project: dict = toml_load(pyproject)

        poetry = project["tool"]["poetry"]

        with Path(".config/meta.yml").open(encoding="utf-8") as f_meta:
            meta = yaml_loads(f_meta)
            poetry["name"] = meta["name"]
            poetry["description"] = meta["description"]
            poetry["repository"] = meta["link"]
            poetry["authors"] = meta["authors"]
            poetry["dependencies"] = meta.get("deps", {})
            poetry["dev-dependencies"] = meta.get("dev", {})

            if poetry.get("group") is None:
                poetry["group"] = {
                    "linter": {"dependencies": {}},
                    "tests": {"dependencies": {}},
                }

            if meta.get("linters", {}).get("types", {}):
                poetry["group"]["linter"]["dependencies"].update(meta["linters"]["types"])
            if meta.get("linters", {}).get("deps", {}):
                poetry["group"]["linter"]["dependencies"].update(meta["linters"]["deps"])

            if meta.get("tests", {}).get("deps", {}):
                poetry["group"]["tests"]["dependencies"].update(meta["tests"]["deps"])

        with Path("pyproject.toml").open("w", encoding="utf-8") as pyproject:
            pyproject.write(toml_dump(project))

    return Command(name="update-poetry", callback=_update, help="Update poetry in pyproject.toml")


if __name__ == "__main__":
    create_cli().start()
