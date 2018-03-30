import os
import pathlib
import json
import logging


class ConfigManager:
    """
    Class to a config file
    """

    def __init__(self, filename: str):
        self.logger = logging.getLogger(__name__)
        self._filename = filename
        self._dir = os.getenv("CONFIG_BASE", os.getcwd() + "/config")
        self._path = pathlib.Path(self.directory, self.filename)
        self._example_path = pathlib.Path(self.directory, "defaults", f"default.{self.filename}")
        self._config = None
        self.logger.debug(f"Created config manager for file {self.filename}")
        self.load()


    @property
    def filename(self):
        return self._filename

    @property
    def directory(self):
        return self._dir

    @property
    def path(self):
        return self._path

    @property
    def config(self):
        return self._config

    @staticmethod
    def build_from_example(example, live):
        """
        Adds any new items from the example config to the current config while retaining
        current updated values.
        """
        example = example.copy()
        for value in live:
            if isinstance(live[value], dict):
                if value not in example.keys():
                    example[value] = {}
                example[value] = ConfigManager.build_from_example(example[value], live[value])
            else:
                example[value] = live[value]
        return example

    def __getitem__(self, item):
        """
        Gets an item from the config
        """
        return self._config[item]

    def __setitem__(self, key, value):
        """
        Sets an item in the onfig
        """
        self._config[key] = value

    def load(self):
        """
        Loads the config file
        """
        self.logger.debug(f"Loading config file {self.filename}")
        self.check_exists()
        with open(self.path) as fp:
            live = json.load(fp)
        with open(self._example_path) as ef:
            example = json.load(ef)
        self._config = ConfigManager.build_from_example(example, live)
        self.save()

    def check_exists(self):
        """
        Checks if the config file exists and if not, creates it from the default config
        """
        if not os.path.exists(self.path):
            with open(self._example_path) as ef:
                example = json.load(ef)
            with open(self.path, "w") as fp:
                fp.write(json.dumps(example, indent=4, separators=(',', ':')))

    def save(self):
        """
        Saves the config
        """
        self.logger.debug(f"Saving config {self.filename} to file")
        with open(self.path, "w") as fp:
            fp.write(json.dumps(self._config, indent=4, separators=(',', ':')))
