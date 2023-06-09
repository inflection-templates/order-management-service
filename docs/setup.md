## Local Setup

You can setup FastAPI project in the following ways.

1. Using venv
2. Using pipenv
3. Using pipx and poetry

### Setup using venv

1. Create virtual environment.
`$ python3 -m venv env`

2. Activate virtual environment.
`$ source env/bin/activate`

3. Install dependencies.
`$ pip install -r requirements.txt `

4. To freeze the dependecnies to requirement.txt.
`$ pip freeze > requirement.txt`

### Setup using pipenv
1. Install pipenv.
`$ pip3 install pipenv`

2. Create pipenv shell.
`$ pipenv shell`
This will create a virtual environment in your C:\Users\<user-name>\.virtualenvs\ folder.
For example, - ```Virtualenv location: C:\Users\Admin\.virtualenvs\fastapi-exp-2-Foeb76tt```. This will create

3. Install fastapi.
`$ pipenv install fastapi`

4. Install uvicorn.
`$ pipenv install uvicorn`

5. To install dev dependencies.
`$ pipenv install pytest --dev`

6. To lock environment for dependencies.
`$ pipenv lock`

7. To install from dependencies from lock file.
`$ pipenv install --ignore-pipfile`

8. Start uvicorn server.
`$ uvicorn main:app --reload`

9. In case you want to remove the created virtual environment, run the following
`$ pipenv --rm`

For further pipenv information, please refer to https://realpython.com/pipenv-guide/.

### Setup using pipx and poetry

1. Install pipx (On windows). For other operating systems, please visit https://pypa.github.io/pipx/.
`$ pip install --user pipx`

2. Install poetry.
`$ pipx install poetry`
Check the installation using `$ poetry --version`.
You can update the poetry version using poetry itself like `$ poetry self update` or using pip as `$ pip install --upgrade poetry`.

3. Update PATH variables.
   Go to `C:\Users\<Username>\.local\bin` and run `pipx ensurepath`. Close the terminal and open again.

4. Initialize a new project with poetry as below.
   `$ poetry new <project-name>`
   Or if the project folder already exists, generate the pyproject.toml interactively using poetry using `$ poetry init`.
   Specify the dependencies during the whole process.

### PLEASE NOTE
We are using poetry to setup order management service.
For any new package installation, please use
`$ poetry add <package-name>`

## Run Server from Command Line

`$ uvicorn main:app --port 12345`

## Run server in debug mode from VSCode through Debugger

1. Select debugging button on the left most toolbar.
2. Select 'Launch Server' from drop down menu.
3. Click on 'Start Debugging' button or press F5.
4. Add breakpoints in code wherever needed.

## Run Tests from command line

To run the tests from command line, run the following
`$ pytest`

## Run the tests from VSCode's Test Functionality

1. Select 'Test' button on the left most toolbar.
2. All the tests in the code will be hierarchically displayed.
3. Run all the tests in 'Run' Mode or in 'Debug' mode. In debug mode, you can add breakpoints in server-code or in test-code.
4. Test results will be displayed in the adjacent panel.
