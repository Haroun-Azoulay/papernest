# Stage 1: Build the Angular application
FROM node:alpine AS build

WORKDIR /usr/src/app

COPY package.json package-lock.json ./

RUN npm install

COPY . .

RUN npm run build --prodi

FROM nginx:alpine

COPY --from=build /usr/src/app/dist/front/browser /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
