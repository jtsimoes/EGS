FROM node:latest

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 4000

CMD [ "npm", "run", "devStart"]

# build: docker build -t payment -f deploy\DockerFile.payment ..\payment\
