labyrinpy
===============

Implementation of [Labyrintti SMS Gateway](http://www.labyrintti.bg/en/sms-gateway.php) API for Python


Installation
---------------

    pip install git+git://github.com/MagicSolutions/labyrinpy.git


HowTo
---------------

Request (sending sms or giving orders to the SMS Gateway):

One must supply the gateway with at least three things:
    1) User
    2) Password
    3) Receiver

The User and Password must be given at initialization of the LabyrinpyRequest object (login with user/password).

    sender = LabyrinpyRequest(username, password)

After that, in order to send sms, you have method called 'send'. Send receive as arguments the following things: list of recipients, content and message type (by default it is text - may be binary or wap-url)

    sender.send([phone_num1, phone_num2, ...], 'sms_message_content', 'message_type')


Response (feedback from the SMS Gateway):

As you send your request to the Gateway it returns you information if your messages have been transmitted through it or not. In order to gain further info if everything has been fine you can catch that response and observe it

    give_me_info = LabyrinpyResponse(response_from_SMS_GATEWAY)

Then you can use some methods such as:

    give_me_info.is_send()  #Returns True if all messages have been sent successfully

and

    give_me_info.errors()  #Returns the status of the errors if there are such


License
---------------

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
