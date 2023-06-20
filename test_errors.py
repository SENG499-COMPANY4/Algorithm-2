from app import app
import json
import unittest


class api_tests(unittest.TestCase):

    # executed before each test run
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

    def test_get_to_wrong_URL(self):
        print("Testing GET to wrong URL")
        response = self.app.get("/predict_class_sizes/1") 
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data,
            b'{"error":"404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."}\n'
        )
    
    def test_no_json_file(self):
        print("Testing POST with no json file")
        response = self.app.post("/predict_class_sizes")
        self.assertEqual(response.status_code, 415)
        self.assertEqual(
            response.data,
            b'{"error":"415 Unsupported Media Type: Did not attempt to load JSON data because the request Content-Type was not \'application/json\'."}\n'
        )


    def test_None_json_file(self):
        print("Testing POST with None json file")
        response = self.app.post("/predict_class_sizes", json=None)
        self.assertEqual(response.status_code, 415)
        self.assertEqual(
            response.data,
            b'{"error":"415 Unsupported Media Type: Did not attempt to load JSON data because the request Content-Type was not \'application/json\'."}\n'
        )
    
    # TODO: Add test case where POST gives file in incorrect format then GET should produce 500 error

if __name__ == "__main__":
    unittest.main()