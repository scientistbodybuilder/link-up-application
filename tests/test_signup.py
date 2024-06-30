import unittest
from unittest.mock import patch, Mock
from flask import session
from website.auth import signup_page, User
from website import create_app
app = create_app()

class SignupTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] =  True
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('app.flash')
    @patch('app.render_template')
    @patch('app.uniqueEmail')
    @patch('app.createUser')
    @patch('app.initializeCards')
    def test_signup_success(self, mock_flash, mock_render_template, mock_uniqueEmail, mock_createUser, mock_initializeCards):
        mock_createUser.return_value = True
        mock_uniqueEmail.return_value = True
        mock_initializeCards.return_value = True
        mock_render_template.return_value = "rendered_template"

        response = self.client.post('/signup', data = {
            'email': 'bob@example.com',
            'password': 'bob1234',
            'confirm password': 'bob1234'
        })

        mock_flash.assert_called_with("Account created!", category='success')
        mock_render_template.assert_called_once_with('signup.html', title="REGISTER", prompt="Log in to an existing account")

    @patch('app.flash')
    @patch('app.render_template')
    def test_signup_password_too_short(self, mock_flash, mock_render_template):
        mock_render_template.return_value = "rendered_template"

        mock_flash.assert_called_with("Password must be atleast 7 characters", category='error')
        mock_render_template.assert_called_once_with('signup.html', title="REGISTER", prompt="Log in to an existing account")

    @patch('app.flash')
    @patch('app.render_template')
    def test_signup_fail_to_confirm_passwords(self, mock_flash, mock_render_template):
        mock_render_template.return_value = "rendered_template"

        mock_flash.assert_called_with("Passwords do not match", category='error')
        mock_render_template.assert_called_once_with('signup.html', title="REGISTER", prompt="Log in to an existing account")

    @patch('app.flash')
    @patch('app.render_template')
    def test_signup_password_does_not_contain_number(self, mock_flash, mock_render_template):
        mock_render_template.return_value = "rendered_template"

        mock_flash.assert_called_with("Password must contain a number", category='error')
        mock_render_template.assert_called_once_with('signup.html', title="REGISTER", prompt="Log in to an existing account")

if __name__ == '__main__':
    unittest.main()