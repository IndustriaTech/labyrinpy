import logging
import requests

logger = logging.getLogger(__name__)

API_URL = 'http://gw.labyrintti.com:28080/sendsms'
API_SSL_URL = 'https://gw.labyrintti.com:28080/sendsms'


class LabyrinpyRequest(object):
    kwargs = {}
    headers = {}

    def __init__(self, user, password, **kwargs):
        self.user = user
        self.password = password
        self.api_url = API_SSL_URL if kwargs.pop('ssl', False) else API_URL
        for key, value in kwargs.items():
            if isinstance(value, bool):
                value = 'yes' if value else 'no'
            self.kwargs[key] = value

    def send(self, recipients, content='', message_type='text', method='POST'):
        if not isinstance(recipients, (tuple, list)):
            recipients = [recipients]

        request, headers = self._request_method(method, self.headers)
        payload = {
            'user': self.user,
            'password': self.password,
            'dests': ','.join(recipients),
            message_type: content,
        }
        payload.update(self.kwargs)
        return request(self.api_url, params=payload, headers=headers)

    def _request_method(self, method, headers):
        if method.lower() == 'post':
            headers = self.headers.copy()
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
        return getattr(requests, method.lower(), 'post'), headers

    def method_name(self):
        pass


class LabyrinpyResponse(object):

    def __init__(self, response):
        self.response = response
        self.messages = self._extract_messages()

    def _extract_messages(self):
        messages = [msg.split(' ', 4) for msg in
                    self.response.content.split('\n')]
        # messages.pop()

        for msg in messages[:-1]:
            if msg[1] == 'OK':
                msg[4] = msg[3] + ' ' + msg[4]
                msg[3] = msg[2]
                msg[2] = 0

        return [{'number': msg[0],
                 'status': msg[1],
                 'error_code': int(msg[2]),
                 'message_count': int(msg[3]),
                 'description': msg[4]} for msg in messages[:-1]]

    def is_send(self):
        return {msg_info['status'] for msg_info in self.messages} == {'OK'}

    def errors(self):
        return [message for message in
                self.messages if message['status'] == 'ERROR']
