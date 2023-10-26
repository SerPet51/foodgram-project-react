# build env
FROM node:13.12.0-alpine as build
WORKDIR /appсв
COPY . ./
RUN npm install
RUN npm install react-meta-tags
RUN npm run build
CMD cp -r build result_build
