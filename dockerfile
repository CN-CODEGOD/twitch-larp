FROM nginx:alpine

COPY --chmod=644 twitch.html /usr/share/nginx/html/index.html

EXPOSE 80
