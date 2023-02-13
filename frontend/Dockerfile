FROM node:16-alpine

LABEL name="frontend"

WORKDIR /

COPY . /

RUN npm install 

EXPOSE 8080:8080

CMD [ "npm", "run", "dev" ]