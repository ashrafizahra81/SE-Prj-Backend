from django.test import SimpleTestCase
from django.urls import resolve , reverse
from ..views import *

class TestChargeWalletUrls(SimpleTestCase):

    def test_charge_wallet_url(self):

        #Arrange
        charge_wallet_urls = reverse('charge_wallet')

        #Assert
        self.assertEqual(resolve(charge_wallet_urls).func.view_class , ChargeWallet)