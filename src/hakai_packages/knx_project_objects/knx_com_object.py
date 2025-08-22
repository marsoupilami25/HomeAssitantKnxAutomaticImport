from classfromtypeddict import ClassFromTypedDict
from xknxproject.models import CommunicationObject

from .knx_flags import KNXFlags
from hakai_packages.knx_utils import Quoted


class KNXComObject(ClassFromTypedDict):
    _class_ref = CommunicationObject
    _exception = { 'module_def': 'module' }

    # for information, instance attributes
    # warning: used ClassFromTypedDict below needs to be import
    #   otherwise the conversion does not work
    # name: str
    # flags: KNXFlags

    def __init__(self, data: dict):
        self.name : Quoted
        self.flags : KNXFlags | None = None #None only for init
        super().__init__(data)

    def is_readable(self):
        return self.flags.read

    def is_writable(self):
        return self.flags.write

    def is_communicating(self):
        return self.flags.communication

    def is_transmitting(self):
        return self.flags.transmit

    def is_updated(self):
        return self.flags.update

    def read_on_init(self):
        return self.flags.read_on_init
