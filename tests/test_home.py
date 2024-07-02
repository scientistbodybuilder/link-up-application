import unittest
from unittest.mock import patch, Mock
from flask import session
from website.views import home_page, CardButton
from website.auth import User
from website import create_app
app = create_app()


class HomeTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] =  True
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('orderOrg')
    @patch('render_template')
    def test_order_by_card(self, mock_orderOrg, mock_render_template):
        mock_render_template.return_value = "rendered_template"

        mock_render_template.assert_called_once_with('home.html')
        
    @patch('orderOrg')
    @patch('render_template')
    def test_order_by_date(self, mock_orderOrg, mock_render_template):
        mock_render_template.return_value = "rendered_template"

        mock_render_template.assert_called_once_with('home.html')
