# -*- coding: utf-8 -*-
"""
This module contains the generalised abstraction for INI files.
"""
from typing import List, Any
import configparser
from pathlib import Path


class IniFile:
    """
    Generalised wrapper around OS-independent INI files
    """

    def __init__(self, name: Path) -> None:
        self._inifilepath = name
        self._ini = configparser.ConfigParser()
        self._ini.read(self._inifilepath)

    @property
    def sections(self) -> List[str]:
        """
        Get accessor for derived classes to avoid direct use of the private implementation.

        Returns:
            List[str]: list of section names.
        """
        return self._ini.sections()

    def add_section(self, name: str) -> None:
        """
        Set accessor for derived classes to avoid direct use of the private implementation.

        Args:
            name (str): section name to be added.
        """
        self._ini.add_section(name)

    def get_section(self, name: str) -> Any:
        """
        Accessor for retrieving a a named section.

        Args:
            name (str): section to be retrieved.

        Returns:
            Any: implementation-dependent data structure.
        """
        return self._ini[name]

    def has_section(self, sname: str) -> bool:
        """
        Test for the existence of a named section.

        Args:
            sname (str): section to be tested.

        Returns:
            bool: True if the named section exists in the INI data.
        """
        return self._ini.has_section(section=sname)

    def has_option(self, sname: str, soption: str) -> bool:
        """
        Test for the existence of a named option within a named section.

        Args:
            sname (str): section name
            soption (str): option name

        Returns:
            bool: True if the option exists in the section.
        """
        return self._ini.has_option(section=sname, option=soption)

    def delete_option(self, sname: str, soption: str) -> bool:
        """
        Method to delete an option from a named section.

        Args:
            sname (str): section name
            soption (str): option name

        Returns:
            bool: True if the option is successfully deleted from the section.
        """
        return self._ini.remove_option(section=sname, option=soption)

    def close(self, discard=False) -> None:
        """
        Automatically saves the configuration back to the original file unless
        flagged to discard any changes.
        """
        if discard is False:
            with open(self._inifilepath, "w", encoding="utf8") as inifile:
                self._ini.write(inifile)
                print(f"Updated: {self._inifilepath}")


class Profiles(IniFile):
    """
    Lightweight wrapper for OS-independent profile configuration information.
    """

    def __init__(self) -> None:
        self._config = Path(Path.home(), ".diz", "profiles")
        super().__init__(name=self._config)

    def add_profile(self, name: str) -> None:
        """Adds a named profile to the sections of the configuration."""
        self.add_section(name)

    def has_profile(self, name: str) -> bool:
        """Checks for the existence of a named profile in the underlying list of sections."""
        return self.has_section(name)

    def content(self, name: str = "default") -> tuple[int, int]:
        """
        Returns the sample rate and bit depth of the named profile
        """
        if self.has_profile(name):
            section = self.get_section(name)
            srate: int = int(section["sample_rate"])
            bdepth: int = int(section["bit_depth"])
            return (srate, bdepth)
        raise ValueError(f"No profile: {name}")
