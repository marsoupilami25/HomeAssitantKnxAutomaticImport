from ClassFromTypedDict import ClassFromTypedDict
from xknxproject.models import CommunicationObject

from KNXProjectManagement.KNXFlags import KNXFlags


class KNXComObject(ClassFromTypedDict):
    _class_ref = CommunicationObject
    _exception = { 'module_def': 'module' }

    name: str
    flags: KNXFlags

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