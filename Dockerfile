# Base docker image
FROM python:3.6-alpine
       
ADD . /src

# install gcc 
# RUN pip install --upgrade pip \
#     && pip install -r requirements.txt

# Intstall pymsf requirements
RUN pip install -r /src/requirements.txt 

WORKDIR /src

#Start bot
CMD [ "python", "/src/main.py" ]

