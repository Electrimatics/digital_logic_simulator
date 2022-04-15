# digital_logic_simulator
Repo for UMBC CMSC 447 (Software Engineering) project.  Our project: Digital Logic Simulator

## Installation
Use the package manager pip to install django and remaining dependencies in requirements.txt within a your virtualenv

```bash
pip install django
```

Set up git and clone the repository 

```bash
git clone https://github.com/Electrimatics/digital_logic_simulator.git
```

## Required Dependencies
The required python packages are found in the [requirements.txt](./requirements.txt) file.  To install them:
```bash
pip install -r requirements.txt
```
No additional configuration is necessary.

Additionally, in order to run the web application and test suite,
you must create a `.env` file in the same directory as `manage.py` with the following information:
```
SECRET_KEY = "MY_SECRETE_KEY"
DEBUG = True
```
Set your secrete key to something else, ideally!

## Running Test Suites
The Django test framework allows you to either run every unittest at the same time or individual ones.  To run all unit tests, navigate to the directory where [manage.py](./manage.py) and run:
```bash
python3 manage.py test
```
To run all the tests in a module, run
```bash
python3 manage.py [module_name].tests
```
To run a specific test case in a module, run
```bash
python3 manage.py [module_name].tests.[case_name]
```
For additional information on running tests, visit the [DJango test tutorial](https://docs.djangoproject.com/en/4.0/topics/testing/overview/)

### Example
To run all the tests in the `gates` module, run
```bash
python3 manage.py test gate.tests
```
To run the TestGenericLogicGate case specifically, run
```bash
python3 manage.py test gates.tests.TestGenericLogicGate
```
