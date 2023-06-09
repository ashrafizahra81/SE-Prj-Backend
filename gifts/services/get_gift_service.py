from accounts.models import User
from ..models import Gift
from .get_gift_Interface import GetGiftService
import logging


logger = logging.getLogger("django")


class ConcreteGetGiftService(GetGiftService):

    def get_gifts(self, user, score):
        
        gift = Gift.objects.get(score = score)
        data = {}
        user.gift = gift
        user.score = user.score - gift.score
        user.save()
        data['discount_code'] = gift.discount_code
        data['new_score'] = user.score
        logger.info('The gifts with id '+str(gift.id) +' assigned to the user with id '+str(user.id))
        
        return data