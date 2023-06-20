# README for Running Algo 2 Flask Application Locally

This README provides instructions on how to run the Algo2 Flask application locally on your machine.

## Prerequisites

- Python 3 installed on your machine.
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

Inside the virtual environment, install the dependencies from the `requirements.txt` file:

```sh
pip install -r requirements.txt
```

### 4. Run the Application using Gunicorn

Run the Flask application using Gunicorn. The following command starts the application with 4 worker processes (`-w 4`) and binds it to `0.0.0.0:5001` (`-b 0.0.0.0:5001`):

```sh
gunicorn -w 4 -b 0.0.0.0:5001 wsgi:app
```

Your Flask application should now be running at [http://0.0.0.0:5001](http://0.0.0.0:5001).

## Making Requests to the Application

After your application is running, open a **new terminal window**. Use the following `curl` commands to make POST and GET requests to your application.

### Making a POST Request

```sh
curl -X POST http://0.0.0.0:5001/
```

### Making a GET Request

```sh
curl http://0.0.0.0:5001/predict_class_sizes
```

## Notes

- Make sure your virtual environment is active when running the application.
- The POST request above does not contain any data. If your endpoint expects data, you will need to modify the curl command accordingly.
- You can deactivate the virtual environment when you're done by typing `deactivate`.