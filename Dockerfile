# use base image
FROM python:3.14.0b1-slim-bookworm

# set up working directory 
WORKDIR /Users/tristanallen/Desktop/TradingPost/src

# copy project files
COPY . .

# install dependencies
# RUN pip install

# setup default command
CMD [ "python" ]