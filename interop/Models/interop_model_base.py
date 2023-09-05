from abc import ABC, abstractmethod

class Interop_Model_Base(ABC):
    @abstractmethod
    def load_from_json(self):
        pass
