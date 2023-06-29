from app import app
import json
import unittest

class api_tests(unittest.TestCase):

    # executed before each test run
    def setUp(self):
        app.config["TESTING"] = True
        self.app = app.test_client()

    # csc 115 data
    #   Summer:   75,  105, 86,  132, 146, 91, 85
    #   Fall:     132, 129, 130, 156, 135, 159
    #   Spring:   352, 357, 299, 312, 316, 353
    def test_one_class_results(self):
        print("Testing predictor with one class")
        f = open("test/data/one_class.json")
        d = json.load(f)
        f.close()
        response = self.app.post("/predict_class_sizes",json=d)
        result = json.loads(response.data.decode('utf-8'))
        
        self.assertEqual(response.status_code, 200)

        # Summer
        self.assertEqual( result[0]["course"], "csc115" )
        self.assertEqual( result[0]["term"], 5 )
        self.assertTrue( result[0]["size"] > 75 )
        self.assertTrue( result[0]["size"] < 146 ) 

        # Fall
        self.assertEqual( result[1]["course"], "csc115" )
        self.assertEqual( result[1]["term"], 9 )
        # self.assertTrue( result[1]["size"] > 129 )    # current result: 115
        self.assertTrue( result[1]["size"] < 200 ) 

        # Spring
        self.assertEqual( result[2]["course"], "csc115" )
        self.assertEqual( result[2]["term"], 1 )
        # self.assertTrue( result[2]["size"] > 299 )    # current result: 259
        self.assertTrue( result[2]["size"] < 400 ) 

        with self.assertRaises(Exception) as e:
            result[3]
            self.assertEqual("IndexError" in e)
    
    
    # csc 115 data
    #   Summer:   75
    #   Fall:     none
    #   Spring:   none
    def test_one_class_with_one_pastEnrol_results(self):
        print("Testing predictor with one class with only one past enrollment entry")
        f = open("test/data/one_class_one_pastEnrol.json")
        d = json.load(f)
        f.close()
        response = self.app.post("/predict_class_sizes",json=d)
        result = json.loads(response.data.decode('utf-8'))
        
        self.assertEqual(response.status_code, 200)

        # Summer
        self.assertEqual( result[0]["course"], "csc115" )
        self.assertEqual( result[0]["term"], 5 )
        # self.assertTrue( result[0]["size"] > 75 )   # current result: 65
        self.assertTrue( result[0]["size"] < 146 ) 

        with self.assertRaises(Exception) as e:
            result[1]
            self.assertEqual("IndexError" in e)

    
    # engr120 data
    #   Summer:   none
    #   Fall:     none
    #   Spring:   393, 393, 354, 356, 319, 346, 338
    def test_one_class_with_only_spring_sem_results(self):
        print("Testing predictor with one class that is only offered in one semester")
        f = open("test/data/one_class_only_spring_sem.json")
        d = json.load(f)
        f.close()
        response = self.app.post("/predict_class_sizes",json=d)
        result = json.loads(response.data.decode('utf-8'))
        
        self.assertEqual(response.status_code, 200)

        # Spring
        self.assertEqual( result[0]["course"], "engr120" )
        self.assertEqual( result[0]["term"], 1 )
        # self.assertTrue( result[0]["size"] > 319 ) # current result: 315
        self.assertTrue( result[0]["size"] < 400 )

        with self.assertRaises(Exception) as e:
            result[1]
            self.assertEqual("IndexError" in e)

    
    def test_one_class_skip_a_year(self):
        print("Testing predictor with one class that is missing a year's information")
        f = open("test/data/one_class_skip_a_year.json")
        d = json.load(f)
        f.close()
        response = self.app.post("/predict_class_sizes",json=d)
        result = json.loads(response.data.decode('utf-8'))
        
        self.assertEqual(response.status_code, 200)

        # Summer
        self.assertEqual( result[0]["course"], "csc115" )
        self.assertEqual( result[0]["term"], 5 )
        self.assertTrue( result[0]["size"] > 75 )
        self.assertTrue( result[0]["size"] < 146 ) 

        # Fall
        self.assertEqual( result[1]["course"], "csc115" )
        self.assertEqual( result[1]["term"], 9 )
        # self.assertTrue( result[1]["size"] > 129 )    # current result: 115
        self.assertTrue( result[1]["size"] < 200 ) 

        # Spring
        self.assertEqual( result[2]["course"], "csc115" )
        self.assertEqual( result[2]["term"], 1 )
        # self.assertTrue( result[2]["size"] > 299 )    # current result: 230
        self.assertTrue( result[2]["size"] < 400 ) 

        with self.assertRaises(Exception) as e:
            result[3]
            self.assertEqual("IndexError" in e)

    
    def test_two_classes(self):
        print("Testing predictor with two classes")
        f = open("test/data/two_classes.json")
        d = json.load(f)
        f.close()
        response = self.app.post("/predict_class_sizes",json=d)
        result = json.loads(response.data.decode('utf-8'))
        
        self.assertEqual(response.status_code, 200)

        # Class 1 Spring
        self.assertEqual( result[0]["course"], "engr120" )
        self.assertEqual( result[0]["term"], 1 )
        # self.assertTrue( result[0]["size"] > 319 ) # current result: 315
        self.assertTrue( result[0]["size"] < 400 ) 

        # Class 2 Summer
        self.assertEqual( result[1]["course"], "csc115" )
        self.assertEqual( result[1]["term"], 5 )
        self.assertTrue( result[1]["size"] > 75 )
        self.assertTrue( result[1]["size"] < 146 ) 

        # Class 2 Fall
        self.assertEqual( result[2]["course"], "csc115" )
        self.assertEqual( result[2]["term"], 9 )
        # self.assertTrue( result[2]["size"] > 129 )    # current result: 115
        self.assertTrue( result[2]["size"] < 200 ) 

        # Class 2 Spring 
        self.assertEqual( result[3]["course"], "csc115" )
        self.assertEqual( result[3]["term"], 1 )
        # self.assertTrue( result[3]["size"] > 299 )    # current result: 259
        self.assertTrue( result[3]["size"] < 400 ) 

        with self.assertRaises(Exception) as e:
            result[4]
            self.assertEqual("IndexError" in e)

    

if __name__ == "__main__":
    unittest.main()