# order-management-service
Order Management Service

You can setup FastAPI project in the following ways.

1. Using pipenv
2. Using pipx and poetry

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

   

