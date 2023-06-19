from app import app
import unittest


class api_tests(unittest.TestCase):

    # executed before each test run
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

    
    def test_endpoint(self):
        print("Test test")
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            b'Hello World!',
        )
    
if __name__ == "__main__":
    unittest.main()