# use base image
FROM python:3.12-slim-bookworm

# set up working directory 
WORKDIR /app

# TODO: need to look into minimizing this image
# install packages
RUN apt-get update && \
    apt-get install -y libpq-dev gcc curl

# copy project files
COPY requirements.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN rm -rf /var/lib/apt/lists/*

# command to run
CMD [ "python", "/app/src/backend_server.py" ]