# Use the official Node.js 20 base image
FROM node:20-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install application dependencies
RUN npm install

# Copy application code
COPY . .

EXPOSE 5000

# Install OpenSSL 1.1
RUN apt-get update -y && apt-get install -y openssl

# Set the command to start the server
CMD ["npm", "prod"]