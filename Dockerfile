# Base docker image
FROM python:3.12-alpine
       
ADD . /src

# Intstall pymsf requirements
RUN pip install -r /src/requirements.txt 

WORKDIR /src

#Start bot
CMD [ "python", "/src/main.py" ]

