import unittest

import mock
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


class FakeResponse(object):
    def __init__(self, some_str):
        self.content = some_str


class TestResponse(unittest.TestCase):
    def setUp(self):
        self.response_text = '35800001 OK 1 message accepted for sending\n' +\
                             '35800002 OK 2 messages accepted for sending\n' +\
                             '35800003 ERROR 2 1 message failed\n' +\
                             '35800004 ERROR 3 2 messages failed\n'
        self.fake_response = FakeResponse(self.response_text)
        self.response = request.LabyrinpyResponse(self.fake_response)

        self.response_OK = '35800001 OK 1 message accepted for sending\n' +\
                           '35800002 OK 2 messages accepted for sending\n'
        self.response_OK = FakeResponse(self.response_OK)
        self.response_OK = request.LabyrinpyResponse(self.response_OK)

    def test_extract_messages(self):
        should_be = [{'number': '35800001',
                      'status': 'OK',
                      'error_code': 0,
                      'message_count': 1,
                      'description': 'message accepted for sending'},
                     {'number': '35800002',
                      'status': 'OK',
                      'error_code': 0,
                      'message_count': 2,
                      'description': 'messages accepted for sending'},
                     {'number': '35800003',
                      'status': 'ERROR',
                      'error_code': 2,
                      'message_count': 1,
                      'description': 'message failed'},
                     {'number': '35800004',
                      'status': 'ERROR',
                      'error_code': 3,
                      'message_count': 2,
                      'description': 'messages failed'}
                     ]
        self.assertEqual(should_be, self.response._extract_messages())

    def test_is_sent_false(self):
        self.assertFalse(self.response.is_send())

    def test_is_sent_true(self):
        self.assertTrue(self.response_OK.is_send())

    def test_errors_feedback(self):
        should_be = [{'number': '35800003',
                      'status': 'ERROR',
                      'error_code': 2,
                      'message_count': 1,
                      'description': 'message failed'},
                     {'number': '35800004',
                      'status': 'ERROR',
                      'error_code': 3,
                      'message_count': 2,
                      'description': 'messages failed'}
                     ]
        self.assertEqual(should_be, self.response.errors())

    def test_errors_feedback_errors_none(self):
        should_be = []
        self.assertEqual(should_be, self.response_OK.errors())

if __name__ == '__main__':
    unittest.main()
