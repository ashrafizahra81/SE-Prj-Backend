from abc import ABC, abstractmethod

class UniqueCodeService(ABC):
    @abstractmethod
    def getUniqueCode(self):
        pass