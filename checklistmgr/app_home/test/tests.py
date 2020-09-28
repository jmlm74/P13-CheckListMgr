from django.test import TestCase
from django.urls import reverse, resolve
import inspect
import pytest

class TestUrls(TestCase):
    """
        Test urls for home_app
    """

    def test_index_is_ok(self):
        """
            test reverse and resolve for /
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('index')
        assert path == '/'
        assert resolve(path).view_name == 'index'

    def test_apphome_index_is_ok(self):
        """
            test reverse and resolve for app_home/index/
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_home:index')
        assert path == '/app_home/index/'
        assert resolve(path).view_name == 'app_home:index'

    def test_legal_ok(self):
        """
            test reverse and resolve for Legal
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_home:legal')
        assert path == '/app_home/legal/'
        assert resolve(path).view_name == 'app_home:legal'

    def test_contact_ok(self):
        """
            test reverse and resolve for contact
        """
        print(inspect.currentframe().f_code.co_name)
        path = reverse('app_home:contact')
        assert path == '/app_home/contact/'
        assert resolve(path).view_name == 'app_home:contact'
