FROM node:21-alpine3.19

ARG VITE_RECAPTCHA_SITE_KEY
ARG VITE_API_URL

ENV VITE_RECAPTCHA_SITE_KEY=$VITE_RECAPTCHA_SITE_KEY
ENV VITE_API_URL=$VITE_API_URL

WORKDIR /app 

COPY yarn.lock package.json ./

RUN yarn config set ignore-engines true
RUN yarn install

COPY . . 

EXPOSE 8080

