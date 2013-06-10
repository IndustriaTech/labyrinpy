import logging
import requests

logger = logging.getLogger(__name__)

API_URL = 'http://gw.labyrintti.com:28080/sendsms'
API_SSL_URL = 'https://gw.labyrintti.com:28080/sendsms'


class LabyrinpyRequest(object):
    kwargs = {}

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
        request = getattr(requests, method.lower(), 'post')
        payload = {
            'user': self.user,
            'password': self.password,
            'dests': ','.join(recipients),
            message_type: content,
        }
        payload.update(self.kwargs)
        return request(self.api_url, params=payload)
