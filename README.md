# getblock_e2e
This repository contains automated tests for UI/API components for Getblock.io

##REQUIREMENTS

You must have the Python version 3.8 or higher. Please run the following commands to get ready to work with framework:
    
    python3.8 -m venv .env
    source .env/bin/activate
    pip install -U pip
    pip install -U -r requirements.txt
    playwright install

##RUN TESTS

To run tests in specific directory use command below.
To run specific test add filename in the end of directory name. Example : pytest tests/tests_api_e2e/test_login_get_api_key_send_request.py
NOTE add the api_key/email/password for specified user

    pytest tests/tests_ui
    pytest tests/tests_ui_e2e/
    pytest tests/tests_api
    pytest tests/tests_api_e2e/
    