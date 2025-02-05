#to build the base image which we got from the dockerhub which has an OS and python installed
FROM python:3.10-slim
# in that mini-computer, create a new folder called flask-docker
WORKDIR /flask-docker

# since my python version is old, upgrade my pip
RUN python3 -m pip install --upgrade pip
#copy the requirements.txt file from the local folder to the folder in the mini computer
COPY requirements.txt requirements.txt
# run the pip install to install the requirements.txt in the mini computer
RUN pip install -r requirements.txt

COPY models ./models
COPY app.py ./app.py
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]

