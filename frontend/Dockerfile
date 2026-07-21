FROM node:20.19.5-alpine3.22 AS build

WORKDIR /app
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci --legacy-peer-deps
COPY frontend/ ./
RUN npm run build

FROM nginx:1.27.4-alpine

COPY infra/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/build/ /usr/share/nginx/html/
COPY docs/ /usr/share/nginx/html/api/docs/

EXPOSE 8080
