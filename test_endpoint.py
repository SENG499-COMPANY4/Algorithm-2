from app import app
import json
import unittest


class api_tests(unittest.TestCase):

    # executed before each test run
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

    
    def test_hello_world(self):
        print("Test test")
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            b'Hello World!',
        )
    
    def test_predictor_one_class(self):
        print("testing predictor with one class")
        f = open("test/data/one_class.json")
        d = json.load(f)
        f.close()
        response = self.app.post("/predict_class_sizes",json=d)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            b'{"message":"Data received and processed"}\n',
        )

    def test_predictor_two_class(self):
        print("testing predictor with two classes")
        f = open("test/data/two_classes.json")
        d = json.load(f)
        f.close()
        response = self.app.post("/predict_class_sizes",json=d)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            b'{"message":"Data received and processed"}\n',
        )

    def test_predictor_one_class_only_spring(self):
        print("testing predictor with one class and only enrolment data for spring")
        f = open("test/data/one_class_only_spring_sem.json")
        d = json.load(f)
        f.close()
        response = self.app.post("/predict_class_sizes",json=d)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            b'{"message":"Data received and processed"}\n',
        )
    
if __name__ == "__main__":
    unittest.main()