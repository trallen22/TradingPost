# use base image
FROM python:3.12-slim-bookworm

# set up working directory 
WORKDIR /app

# copy project files
COPY requirements.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN apt update && apt install -y curl

# command to run
CMD [ "python", "/app/src/backend_server.py" ]