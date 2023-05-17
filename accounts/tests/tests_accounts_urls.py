from django.test import SimpleTestCase
from django.urls import resolve , reverse
from ..views import *

class TestAccountsUrls(SimpleTestCase):

    def test_register_url(self):

        #Arrange
        register_url = reverse('accounts:register')

        #Assert
        self.assertEqual(resolve(register_url).func.view_class , UserRegister)
    
    def test_login_url(self):
    
        #Arrange
        login_url = reverse('accounts:token_obtain_pair')

        #Assert
        self.assertEqual(resolve(login_url).func.view_class , CustomTokenObtainPairView)
    
    def test_edit_profile_url(self):
    
        #Arrange
        edit_profile_url = reverse('accounts:edit-profile')

        #Assert
        self.assertEqual(resolve(edit_profile_url).func.view_class , UserEditProfile)

    def test_create_shop_url(self):
        
        #Arrange
        create_shop_url = reverse('accounts:create_shop')

        #Assert
        self.assertEqual(resolve(create_shop_url).func.view_class , ShopManagerRegister)

    def test_edit_shop_url(self):
        
        #Arrange
        edit_shop_url = reverse('accounts:edit_shop')

        #Assert
        self.assertEqual(resolve(edit_shop_url).func.view_class , EditShop)

    def test_show_user_info_url(self):
        
        #Arrange
        show_user_info_url = reverse('accounts:show_user_info')

        #Assert
        self.assertEqual(resolve(show_user_info_url).func.view_class , ShowUserInfo)

    def test_token_verify_url(self):
        
        #Arrange
        token_verify_url = reverse('accounts:token_verify')

        #Assert
        self.assertEqual(resolve(token_verify_url).func.view_class , TokenVerifyView)

    def test_show_score_url(self):
        
        #Arrange
        show_score_url = reverse('accounts:show_score')

        #Assert
        self.assertEqual(resolve(show_score_url).func.view_class , show_score)

    def test_reset_password_url(self):
        
        #Arrange
        reset_password_url = reverse('accounts:reset_password')

        #Assert
        self.assertEqual(resolve(reset_password_url).func , reset_password)

    def test_recover_password_url(self):
        
        #Arrange
        recover_password_url = reverse('accounts:recover_password', args=(1,))

        #Assert
        self.assertEqual(resolve(recover_password_url).func.view_class , RecoverPassword)

    def test_receive_password_url(self):
        
        #Arrange
        receive_password_url = reverse('accounts:receive_email')

        #Assert
        self.assertEqual(resolve(receive_password_url).func.view_class , ReceiveEmailForRecoverPassword)

    def test_verify_email_url(self):
        
        #Arrange
        verify_email_url = reverse('accounts:verify_email')

        #Assert
        self.assertEqual(resolve(verify_email_url).func.view_class , verfyUserToResgister)