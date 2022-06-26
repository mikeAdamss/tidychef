"""
Creates a ConfigParser object from the provided configuration

Allows remote configurations.
"""

from __future__ import annotations

import configparser
from dataclasses import dataclass
from pathlib import Path

this_dir = Path(__file__).parent
default_config_path = Path(this_dir / "default_config.ini")


@dataclass
class ConfigController:
    configparser: configparser.ConfigParser

    def validate(config: configparser.ConfigParser):
        """
        Validate the configuration
        """

        # TODO
        ...

    @staticmethod
    def from_ini(ini_path: Path = default_config_path) -> ConfigController:

        cfg = configparser.ConfigParser()
        cfg.read(ini_path)

        cc = ConfigController(cfg)
        cc.validate()
        return cc
