FROM node:19-alpine as node-builder
COPY client /client
WORKDIR /client
RUN npm install && npm run build

CMD ["sh", "-c", "node ./.output/server/index.mjs"]