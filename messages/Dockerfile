FROM node:20-alpine3.16

WORKDIR /usr/app

COPY app/package*.json /usr/app

RUN npm init -y
RUN npm install

COPY . . 
