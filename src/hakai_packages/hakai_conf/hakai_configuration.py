from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from hakai_packages.knx_project import KNXProjectManager

@dataclass(frozen=True)
class HAKAIConfiguration: # pylint: disable=too-many-instance-attributes

    project : "KNXProjectManager"
    hamode : bool | None
    overwrite : bool
    location_separator : str
    suppress_project_name : bool
    replace_spaces : str
    not_remove_location : bool
    not_remove_device : bool
    remove_keyword : bool
    name_pattern : str

    # singleton storage
    _instance = None

    def __new__(cls, *_args, **_kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls):
        """Get the singleton. Raise an error if not initialised."""
        if cls._instance is None:
            raise RuntimeError("The singleton HAKAIConfiguration is not yet initialized.")
        return cls._instance
