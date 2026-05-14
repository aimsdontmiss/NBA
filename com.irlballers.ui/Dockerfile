FROM node:22

WORKDIR /ui

COPY package.json package-lock.json* ./
RUN npm ci && npm rebuild

COPY . .

EXPOSE 4200

ENV CHOKIDAR_USEPOLLING=true
ENV WATCHPACK_POLLING=true
ENV CHOKIDAR_INTERVAL=100
ENV NG_FORCE_TTY=true

CMD ["npm", "run", "start", "--", "--host", "0.0.0.0", "--poll=1000", "--disable-host-check"]
