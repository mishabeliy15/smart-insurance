FROM node:18-alpine3.14

WORKDIR /app


ENV PATH /app/node_modules/.bin:$PATH


COPY package.json /app
COPY package-lock.json /app
COPY yarn.lock /app

RUN yarn install

COPY . /app

CMD ["yarn", "run", "start"]