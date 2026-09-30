from http.server import ThreadingHTTPServer
import json
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from portfolio.server import Handler


class ServerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def call(self, path, body=None, headers=None):
        req = Request(self.base + path, data=None if body is None else json.dumps(body).encode(), headers=headers or {"Content-Type": "application/json"})
        try:
            with urlopen(req, timeout=5) as response:
                return response.status, response.headers, response.read()
        except HTTPError as exc:
            return exc.code, exc.headers, exc.read()

    def test_health_and_documents(self):
        status, _, body = self.call("/api/health")
        self.assertEqual(status, 200)
        self.assertEqual(json.loads(body)["documents"], 12)
        self.assertEqual(len(json.loads(self.call("/api/documents")[2])), 12)

    def test_answer_endpoint(self):
        status, _, body = self.call("/api/ask", {"question": "VPN einrichten"})
        self.assertEqual(status, 200)
        self.assertFalse(json.loads(body)["abstained"])

    def test_bad_input_and_model_flag(self):
        for body in ({"question": ""}, [], {"question": "VPN", "use_model": "false"}):
            with self.subTest(body=body):
                self.assertEqual(self.call("/api/ask", body)[0], 400)

    def test_cross_origin_request_rejected(self):
        self.assertEqual(self.call("/api/ask", {"question": "VPN"}, {"Content-Type": "application/json", "Origin": "https://example.com"})[0], 403)

    def test_content_type_required(self):
        self.assertEqual(self.call("/api/ask", {"question": "VPN"}, {"Content-Type": "text/plain"})[0], 415)

    def test_static_and_security_headers(self):
        for path, content_type in (("/", "text/html"), ("/app.js", "text/javascript"), ("/style.css", "text/css")):
            status, headers, body = self.call(path)
            self.assertEqual(status, 200)
            self.assertIn(content_type, headers["Content-Type"])
            self.assertEqual(headers["X-Content-Type-Options"], "nosniff")
            self.assertTrue(body)

    def test_unknown_path_and_traversal(self):
        self.assertEqual(self.call("/missing")[0], 404)
        self.assertEqual(self.call("/../data/questions.json")[0], 404)


if __name__ == "__main__":
    unittest.main()
