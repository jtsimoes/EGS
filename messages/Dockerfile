FROM node:20-alpine3.16

COPY app /usr/app

WORKDIR /usr/app

RUN npm init -y
RUN npm install


CMD [ "npm", "start" ]