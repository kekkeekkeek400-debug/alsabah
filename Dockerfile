FROM ghcr.io/puppeteer/puppeteer:latest

USER root
WORKDIR /app
ENV NODE_OPTIONS="--max-old-space-size=150"

COPY package*.json ./
RUN npm install

COPY . .

CMD ["node", "index.js"]
