[![Build and deploy Python app to Azure Web App - algo-2-app-staging](https://github.com/SENG499-COMPANY4/Algorithm-2/actions/workflows/staging_algo-2-app-staging.yml/badge.svg?branch=staging)](https://github.com/SENG499-COMPANY4/Algorithm-2/actions/workflows/staging_algo-2-app-staging.yml)

# README for Running Algo 2 Flask Application Locally

This README provides instructions on how to run the Algo2 Flask application locally on your machine. The Algo2 Flask application is a service that predicts the class sizes for the next year of the Software Engineering Uvic course by analyzing previous class size trends. It does this by using the SARIMA time series analysis model.

## Prerequisites

- Python 3 installed on your machine. You can download Python from [here](https://www.python.org/downloads/). You can check if Python is installed by typing `python --version` or `python3 --version` in your terminal.
- Terminal (Linux/macOS) or Command Prompt/PowerShell (Windows).

## Steps to Run the Application

### 1. Create a Virtual Environment

It's a good practice to create a virtual environment to isolate the application dependencies.

Run the following command to create a virtual environment named `env`:

```sh
python3 -m venv env
```

### 2. Activate the Virtual Environment

Activate the virtual environment by running:

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

### 3. Install Dependencies

Inside the virtual environment, install the dependencies from the `requirements.txt` file located in the same directory as this README:

```sh
pip install -r requirements.txt
```

For Windows, if you encounter an error installing the pip package, try the following command:

```sh
.\env\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Run the Application using Gunicorn

Run the Flask application using Gunicorn. The following command starts the application with 4 worker processes (`-w 4`) and binds it to `0.0.0.0:8000` (`-b 0.0.0.0:8000`):

```sh
gunicorn -w 4 -b 0.0.0.0 wsgi:app
```

Your Flask application should now be running at [http://0.0.0.0:8000](http://0.0.0.0:8000).

## Making Requests to the Application

After your application is running, open a **new terminal window**. Use the following `curl` commands to make POST and GET requests to your application.

### Making a GET Request

For example, to make a GET request to the root endpoint:

```sh
curl http://0.0.0.0:8000/
```
To make a GET request to the `predict_class_sizes` endpoint, which will return the predicted class sizes for the next year based on the data provided by the POST request:

```sh
curl http://0.0.0.0:8000/predict_class_sizes
```

### Making a POST Request

To make a POST request to the `predict_class_sizes` endpoint, use the following command. Replace `{"key": "value"}` with your data. The expected data format is a JSON object with class size data for various classes for the time series analysis. The structure should be as follows:

```JSON
[
  {
    "course": "string",
    "prereq": [
      "string"
    ],
    "coreq": [
      "string"
    ],
    "pastEnrol": [
      {
        "year": 0,
        "term": 0,
        "size": 0
      }
    ]


  }
]
```

Here is an example of a curl command with a sample JSON object:

```sh
curl -X POST -H "Content-Type: application/json" -d '[{"course": "SE101", "prereq": ["SE100"], "coreq": [], "pastEnrol": [{"year": 2022, "term": 2, "size": 30}]}]' http://0.0.0.0:8000/predict_class_sizes
```

## Notes

- Make sure your virtual environment is active when running the application.
- You can deactivate the virtual environment when you're done by typing `deactivate`.

## Known Limitations and Requirements

- The POST request needs to follow the exact JSON structure specified above for the application to process the data correctly.  
- The application is under development, and some features may not be fully implemented yet.

## Troubleshooting and Verification

If you encounter issues while running the application or want to verify if it's running correctly, here are a few tips:

- Ensure you have the latest version of Python and pip installed. 
- Ensure your virtual environment is activated, and all dependencies are installed before running the application.
- If you get a 'Connection Refused' error when trying to access the application, check if the application is running and if the port is not blocked by your firewall.
- If your POST request isn't returning the expected response, ensure that the JSON object is correctly formatted and matches the expected structure.

[Further troubleshooting tips to be added as they become known]
