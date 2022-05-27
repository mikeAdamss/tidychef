"""
Creates a ConfigParser object from the provided configuration

Allows remote configurations.
"""

from __future__ import annotations

from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ConfigController:
    configparser: ConfigParser

    def validate(config: ConfigParser):
        """
        Validate the configuration
        """
        ...

    @staticmethod
    def from_ini(ini_path: Path) -> ConfigController:
        config_parsed = ConfigParser(ini_path)
        ConfigController(config_parsed)
        ConfigController.validate()
        return ConfigController
