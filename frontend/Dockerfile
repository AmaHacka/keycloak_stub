FROM nginx:1.24-alpine

WORKDIR /app/web

RUN rm /etc/nginx/conf.d/default.conf

COPY config/nginx.conf /etc/nginx/conf.d/nginx.conf

COPY ./app /app/web

EXPOSE 8080

