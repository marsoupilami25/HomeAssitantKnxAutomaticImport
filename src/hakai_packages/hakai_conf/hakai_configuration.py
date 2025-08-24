from dataclasses import dataclass

from hakai_packages.knx_project import KNXProjectManager

@dataclass(frozen=True)
class HAKAIConfiguration:

    project : KNXProjectManager
    hamode : bool | None
    overwrite : bool
    location_separator : str
    suppress_project_name : bool

    # singleton storage
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls):
        """Get the singleton. Raise an error if not initialised."""
        if cls._instance is None:
            raise RuntimeError("The singleton HAKAIConfiguration is not yet initialized.")
        return cls._instance