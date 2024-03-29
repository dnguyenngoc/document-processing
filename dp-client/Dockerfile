FROM node:14.17-alpine3.13 as builder

WORKDIR /app

ENV PATH /app/node_modules/.bin:$PATH

COPY ./package.json /app/package.json
COPY ./package-lock.json /app/package-lock.json

RUN yarn install

COPY . .

RUN yarn build:production


FROM nginx 

WORKDIR /usr/share/nginx/html

ARG DOMAIN
ARG BE_HOST
ARG BE_PORT

RUN rm -v /etc/nginx/nginx.conf
RUN rm -v /etc/nginx/conf.d/default.conf
COPY ./nginx.conf /etc/nginx/

RUN rm -rf ./*

COPY ./m_nginx.conf .
COPY ./local_nginx.conf .
COPY ./custom_nginx.sh .
RUN chmod +x custom_nginx.sh
RUN ./custom_nginx.sh

COPY --from=builder /app/build .

EXPOSE 80 443

ENTRYPOINT ["nginx", "-g", "daemon off;"]