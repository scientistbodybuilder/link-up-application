import unittest
from unittest.mock import patch, Mock
from flask import session
from website.auth import login_page, User
from website import create_app
app = create_app()

class LoginTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] =  True
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('app.userExist')
    @patch('app.flash')
    @patch('app.render_template')
    def test_login_success(self,mock_flash, mock_userExist, mock_render_template):
        mock_userExist.return_value = 1
        mock_render_template.return_value = "rendered_template"

        mock_flash.assert_called_with("Authetication Succesful", category='success')
        mock_render_template.assert_called_once_with('login.html', title="LOGIN", prompt="Create an account")

    @patch('app.userExist')
    @patch('app.flash')
    @patch('app.render_template')
    def test_login_incorrect_password(self, mock_flash, mock_render_template, mock_userExist):
        mock_userExist.return_value = 2
        mock_render_template.return_value = "rendered_template"

        mock_flash.assert_called_with("Incorrect password", category='error')
        mock_render_template.assert_called_once_with('login.html', title="LOGIN", prompt="Create an account")

    @patch('app.userExist')
    @patch('app.flash')
    @patch('app.render_template')
    def test_login_invalid_credential(self, mock_flash, mock_render_template, mock_userExist):
        mock_userExist.return_value = 0
        mock_render_template.return_value = "rendered_template"

        mock_flash.assert_called_with("Invalid Credentials", category='error')
        mock_render_template.assert_called_once_with('login.html', title="LOGIN", prompt="Create an account")

    if __name__ == '__main__':
        unittest.main()