from .editProfile_interface import EditProfileService
from rest_framework.response import Response
from rest_framework import status

import logging

logger = logging.getLogger("django")

class ConcreteEditProfileService(EditProfileService):

    def edit_profile(slf, serialized_data):
        
        if(not(serialized_data.data['user_postal_code'].isdigit())):
            logger.warn('The user postal code entered is invalid')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if(not(serialized_data.data['user_phone_number'].isdigit())):
            logger.warn('The user phone number entered is invalid')
            return Response(status=status.HTTP_400_BAD_REQUEST)
        logger.info('Data entered is valid')
        edited_user = serialized_data.save()

        return Response(serialized_data.data, status=status.HTTP_200_OK)