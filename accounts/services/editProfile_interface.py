from abc import ABC, abstractmethod


class EditProfileService(ABC):

    @abstractmethod
    def edit_profile(slf, serialized_data):
        pass

