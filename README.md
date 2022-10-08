# Competitive Programming Backend

## Installation

### Create Virtual Environment

After pulling the repository, create a virtual environment in the root folder (same level as setup.py).

For Windows:

```
python -m venv venv
```

For Mac:

```
python3 -m venv venv
```

If you do create a virtual environment some other way, please name it `venv`. **This is so the virtual environment is not pushed to the repository.**

### Activate Virtual Environment

After installing the virtual environment, activate the virtual environment on the command prompt. Make sure you're in the folder which contains `venv`, and run:

For Windows:

```
venv/Scripts/activate.bat
```

For Mac:

```
. venv/bin/activate
```

### Install Project Dependencies

Now, you have activated the python virtual environment onto your terminal. **You will need to perform the command above anytime you close your terminal.**

In the terminal which has activated the virtual environment you will now install the dependencies for the project. Run the command:

```
pip install -e .
```

Anytime you pull the repository, you will need to check for changes in the neccesary dependences. **If the dependencies have changed in the project, running the command above will install the newest dependencies.**

## Running the Project

Once you have installed the dependencies and are in the terminal which has your virtual environment activate, so long as you are in the same folder which contains setup.py, you can run:

```
flask --app competitive_programming_backend run
```

This will start up a local Flask instance, which you can use to test the routes of the backend.
