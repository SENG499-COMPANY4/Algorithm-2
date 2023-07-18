from setup import app
import json
import unittest


class api_tests(unittest.TestCase):

    # executed before each test run
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

    def test_get(self):
        print("Testing GET")
        response = self.app.get("/predict_class_sizes") 
        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            response.data,
            b'{"error":"405 Method Not Allowed: The method is not allowed for the requested URL."}\n'
        )

    def test_get_to_wrong_URL(self):
        print("Testing GET to wrong URL")
        response = self.app.get("/predict_class_sizes/1") 
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data,
            b'{"error":"404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."}\n'
        )
    
    def test_post_to_wrong_URL(self):
        print("Testing POST to wrong URL")
        response = self.app.post("/predict_class_sizes/predict_class_sizes")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.data,
            b'{"error":"404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."}\n'
        )
    
    def test_post_no_json_file(self):
        print("Testing POST with no json file")
        response = self.app.post("/predict_class_sizes")
        self.assertEqual(response.status_code, 415)
        self.assertEqual(
            response.data,
            b'{"error":"415 Unsupported Media Type: Did not attempt to load JSON data because the request Content-Type was not \'application/json\'."}\n'
        )

    def test_post_None_json_file(self):
        print("Testing POST with None json file")
        response = self.app.post("/predict_class_sizes", json=None)
        self.assertEqual(response.status_code, 415)
        self.assertEqual(
            response.data,
            b'{"error":"415 Unsupported Media Type: Did not attempt to load JSON data because the request Content-Type was not \'application/json\'."}\n'
        )
    
    # TODO: Add test case where POST gives file in incorrect format then GET should produce 500 error
    def test_post_incorrect_file_not_list(self):
        print("Testing POST with incorrect file format (not a list)")
        response = self.app.post("/predict_class_sizes", json="./incorrect_file_format.json")
        self.assertEqual(response.status_code, 500)
        #self.assertEqual(
            #response.data,
            #b'{"error":"500 Internal Error: string indices must be integers, not \'str\'"}\n'
        #)

    def test_post_incorrect_file(self):
        print("Testing POST with incorrect file format (missing \"course\")")
        response = self.app.post("/predict_class_sizes", json="./incorrect_file_format_2.json")
        self.assertEqual(response.status_code, 500)
        #self.assertEqual(
            #response.data,
            #b'{"error":"500 Internal Error: string indices must be integers, not \'str\'"}\n'
        #)

if __name__ == "__main__":
    unittest.main()