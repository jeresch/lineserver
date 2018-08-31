import unittest
import threading
import time
import urllib.request
from lineserver.server import Server


class SystemTestCase(unittest.TestCase):
    def setUp(self):
        self.port = 8000
        self.server = Server(self.port, '../frankenstein.txt')
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.start()

    def tearDown(self):
        time.sleep(0.5)
        self.server.shutdown()

    def test_first_line(self):
        request = urllib.request.Request('http://127.0.0.1:{}/lines/1'.format(self.port), method='GET')
        response = urllib.request.urlopen(request)
        self.assertEqual(int(response.status), 200)

    def test_normal_line(self):
        request = urllib.request.Request('http://127.0.0.1:{}/lines/1435'.format(self.port), method='GET')
        response = urllib.request.urlopen(request)
        self.assertEqual(int(response.status), 200)
        self.assertEqual(response.read(), "The astonishment which I had at first experienced on this discovery")

    def test_empty_line(self):
        request = urllib.request.Request('http://127.0.0.1:{}/lines/1'.format(self.port), method='GET')
        response = urllib.request.urlopen(request)
        self.assertEqual(response.read(), "")

    def test_past_the_end(self):
        request = urllib.request.Request('http://127.0.0.1:{}/lines/8000'.format(self.port), method='GET')
        response = urllib.request.urlopen(request)
        self.assertEqual(int(response.status), 413)
