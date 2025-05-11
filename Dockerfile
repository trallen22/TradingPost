# use base image
FROM python:3.12-slim-bookworm

# set up working directory 
WORKDIR /app

# copy project files
COPY . .

# install dependencies
RUN pip install --no-cache-dir -r dependencies.txt

# setup default command
CMD [ "python", "src/ticker_news.py" ]