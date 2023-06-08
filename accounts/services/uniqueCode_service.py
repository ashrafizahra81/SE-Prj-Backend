import random
from .uniqueCode_interface import UniqueCodeService
from Backend import dependencies




class ConcreteUniqueCodeService(UniqueCodeService):

    def getUniqueCode(self):
        codeForUsers_service_instance = dependencies.codeForUsers_service_instance
        while(True):
            token = random.randint(100000,999999)
            if(not(codeForUsers_service_instance.checkIfTheCodeExists(token))):
                return token
    
