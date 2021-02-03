DOCKERIZE_PY_APP_PATH = 'DOCKERIZE_PY_APP/'
DOCKERIZE_PY_APP_FILE = 'app.py'
DOCKERIZE_PY2_APP_FILE = 'app2.py'
DOCKER_COMPOSE_APP_PATH= 'DOCKER_COMPOSE_DEMO_APP/'

DOCKER_FILE_TEMPLATE = """
# set base image (host OS)
FROM python:{PY_VERSION}

# set the working directory in the container
WORKDIR /{BASE_DIR}

# copy the dependencies file to the working directory
{IS_REQ_FILE_EXIST}COPY requirements.txt .

# install dependencies
{IS_REQ_FILE_EXIST}RUN pip install -r requirements.txt

# copy the content of the directory to the working directory
COPY ./ .

# command to run on container start
CMD [ "python", "{EXEC_FILE}" ]
"""
