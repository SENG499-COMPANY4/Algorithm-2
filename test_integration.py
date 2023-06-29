import requests
import unittest
import os
import json


def get_token():
    url = "https://login.microsoftonline.com/organizations/oauth2/v2.0/token"
    data = {
        "client_id": os.getenv("CLIENT_ID"),
        "scope": os.getenv("SCOPE"),
        "client_secret": os.getenv("CLIENT_SECRET"),
        "username": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD"),
        "grant_type": "password"
    }
    response = requests.post(url, data=data)
    response.raise_for_status()  # Raise an exception if the request failed
    return response.json()["access_token"]


class TestAzureApplication(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.token = get_token()

    def test_hello_world(self):
        url = "https://algo-2-app-staging.azurewebsites.net/"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception if the request failed
        self.assertEqual(response.text, "Hello World!")

    def test_class_size(self):
        url = "https://algo-2-app-staging.azurewebsites.net/predict_class_sizes"
        headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
        
        with open("./test/data/two_classes.json") as f:
            data = json.load(f)
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception if the request failed

        result = response.json()

        for class_info in result:
            # Check that each dictionary has the keys 'course', 'size', and 'term'
            self.assertIn('course', class_info)
            self.assertIn('size', class_info)
            self.assertIn('term', class_info)

            # Check that 'size' and 'term' are integers
            self.assertIsInstance(class_info['course'], str)
            self.assertIsInstance(class_info['size'], int)
            self.assertIsInstance(class_info['term'], int)

        self.assertEqual(result[0]["course"], "engr120")
        self.assertEqual(result[1]["course"], "csc115")
        self.assertEqual(result[2]["course"], "csc115")
        self.assertEqual(result[3]["course"], "csc115")
        # still needs to add stuff


if __name__ == "__main__":
    unittest.main()
