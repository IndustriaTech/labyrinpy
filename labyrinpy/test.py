import unittest
from unittest import mock

import request


class TestRequests(unittest.TestCase):
    def setUp(self):
        self.request = request.LabyrinpyRequest(
            user='tester',
            password='the_best_kept_secret_ever')
        self.expected_params = {
            'password': 'the_best_kept_secret_ever',
            'user': 'tester',
            'text': "I'm in space",
        }
        self.expected_headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

    @mock.patch('request.requests')
    def test_basic_request(self, mock_requests):
        self.request.send(['+359555000'], content="I'm in space")
        self.expected_params['dests'] = '+359555000'
        mock_requests.post.assert_called_with(self.request.api_url,
                                              params=self.expected_params,
                                              headers=self.expected_headers)

    @mock.patch('request.requests')
    def test_multiple_recipients(self, mock_requests):
        self.request.send(['+359555000', '+358555001'], content="I'm in space")
        self.expected_params['dests'] = '+359555000,+358555001'
        mock_requests.post.assert_called_with(self.request.api_url,
                                              params=self.expected_params,
                                              headers=self.expected_headers)

    @mock.patch('request.requests')
    def test_one_recipient_as_string(self, mock_requests):
        self.request.send('+359555000', content="I'm in space")
        self.expected_params['dests'] = '+359555000'
        mock_requests.post.assert_called_with(self.request.api_url,
                                              params=self.expected_params,
                                              headers=self.expected_headers)

    @mock.patch('request.requests')
    def test_one_recipient_as_list(self, mock_requests):
        self.request.send(['+359555000'], content="I'm in space")
        self.expected_params['dests'] = '+359555000'
        mock_requests.post.assert_called_with(self.request.api_url,
                                              params=self.expected_params,
                                              headers=self.expected_headers)

    @mock.patch('request.requests')
    def test_with_enabled_unicode(self, mock_requests):
        unicode_request = request.LabyrinpyRequest(
            user='tester',
            password='the_best_kept_secret_ever',
            unicode=True)
        unicode_request.send(['+359555000'], content="I'm in space")
        self.expected_params['dests'] = '+359555000'
        self.expected_params['unicode'] = 'yes'
        mock_requests.post.assert_called_with(unicode_request.api_url,
                                              params=self.expected_params,
                                              headers=self.expected_headers)

if __name__ == '__main__':
    unittest.main()
