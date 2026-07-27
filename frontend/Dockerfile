FROM nginx:1.29-alpine

COPY . /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY config.template.js /etc/nginx/templates/config.js.template

EXPOSE 80
