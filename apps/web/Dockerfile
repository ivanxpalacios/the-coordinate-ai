FROM node:24.19.0-alpine

WORKDIR /app

COPY package*.json ./

RUN npm ci

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]