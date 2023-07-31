[![Build and deploy Python app to Azure Web App - algo-2-app](https://github.com/SENG499-COMPANY4/Algorithm-2/actions/workflows/master_algo-2-app.yml/badge.svg?branch=master)](https://github.com/SENG499-COMPANY4/Algorithm-2/actions/workflows/master_algo-2-app.yml)
[![Build and deploy Python app to Azure Web App - algo-2-app-staging](https://github.com/SENG499-COMPANY4/Algorithm-2/actions/workflows/staging_algo-2-app-staging.yml/badge.svg?branch=staging)](https://github.com/SENG499-COMPANY4/Algorithm-2/actions/workflows/staging_algo-2-app-staging.yml)

# README for Running Algo 2 Flask Application Locally

The Algo2 Flask application predicts the class sizes for the next year of the Software Engineering Uvic course using the SARIMA time series analysis model. This guide details how to set up and run the application on your local machine.

## Prerequisites

- Python 3: Check Python installation by typing `python --version` or `python3 --version` in your terminal. If not installed, download Python from [here](https://www.python.org/downloads/).
- Terminal (Linux/macOS) or Command Prompt/PowerShell (Windows).

## Steps to Run the Application

1. **Create a Virtual Environment**: For application dependencies isolation, create a virtual environment named `env`:

   ```sh
   python3 -m venv env
   ```

2. **Activate the Virtual Environment**:

   For Linux/macOS:

   ```sh
   source env/bin/activate
   ```

   For Windows (Command Prompt):

   ```sh
   env\Scripts\activate.bat
   ```

   For Windows (PowerShell):

   ```sh
   env\Scripts\Activate.ps1
   ```

3. **Install Dependencies**: Install the dependencies from `requirements.txt`:

   ```sh
   pip install -r requirements.txt
   ```

   For Windows, if you encounter an error installing the pip package:

   ```sh
   .\env\Scripts\python.exe -m pip install -r requirements.txt
   ```

4. **Run the Application using Gunicorn**: Start the application with 4 worker processes and bind it to `0.0.0.0:8000`:

   ```sh
   gunicorn -w 4 -b 0.0.0.0 wsgi:app
   ```

   Access your Flask application at [http://0.0.0.0:8000](http://0.0.0.0:8000).

## Interacting with the Application

Open a **new terminal window** to make POST and GET requests.

### Making a GET Request

To make a GET request to the root endpoint:

```sh
curl http://0.0.0.0:8000/
```

### Making a POST Request

Use the following structure for your JSON object:

```json
[
    {
        "course": "string",
        "Term": ["int"],
        "Year": "int",
        "pastEnrollment": [
            {
                "year": "int",
                "term": "int",
                "size": "int"
            }
        ]
    }
]
```

Run this example command with a sample JSON object:

```sh
curl -X POST -H "Content-Type: application/json" -d '[{"course": "csc115", "Term" : [5],"Year" : 2024, "pastEnrollment": [{"year": 2017,"term": 5,"size": 75}]}]' http://0.0.0.0:8000/predict_class_sizes
```

The output should look like this:

```
[{"course":"csc115","size":75,"term":5}]
```

## Making a Request via JSON File

### Create a JSON File

You can create a JSON file in your preferred text editor. Here is an example file named `input_data.json`:

```json
[
    {
        "course": "engr120",
        "Term" : [1],
        "Year" : 2024,
        "pastEnrollment": [
            {
                "year": 2017,
                "term": 1,
                "size": 393
            },
            {
                "year": 2018,
                "term": 1,
                "size": 393
            },
            {
                "year": 2019,
                "term": 1,
                "size": 356
            },
            {
                "year": 2020,
                "term": 1,
                "size": 354
            },
            {
                "year": 2021,
                "term": 1,
                "size": 346
            },
            {
                "year": 2022,
                "term": 1,
                "size": 338
            },
            {
                "year": 2023,
                "term": 1,
                "size": 319
            }
        ]
    }
]
```

### Use JSON File in Curl Command

To make a POST request using the JSON file, use this command (make sure that `input_data.json` is in the same directory):

```sh
curl -X POST -H "Content-Type: application/json" -d @input_data.json http://0.0.0.0:8000/predict_class_sizes
```

## Notes

- Ensure your virtual environment is active when running the application.
- Deactivate the virtual environment when you're done by typing `deactivate`.
- The POST request should follow the exact JSON structure.
- The more data provided, the better the prediction.
- The application is under development; some features may not be fully implemented yet.

## Troubleshooting

- Ensure the latest version of Python and pip.
- Ensure the virtual environment is activated, and all dependencies are installed before running.
- Check if the application is running and if the port is not blocked by your firewall if you get a 'Connection Refused' error.
- Ensure the JSON object is correctly formatted and matches the expected structure if your POST request isn't returning the expected response.

Additional troubleshooting tips will be added as needed.

