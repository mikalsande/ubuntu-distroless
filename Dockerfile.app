FROM builder-nodejs16 as builder

# Prepare build directory.
RUN mkdir /build
WORKDIR /build
COPY package.json .
COPY package-lock.json .

# Install dependencies.
RUN npm install

####################################

# Runtime image
FROM runner-nodejs16

# Copy dependencies from builder.
COPY --from=builder /build/node_modules /app/node_modules

# Copy application code.
COPY index.js /app
CMD ["node", "/app/index.js"]
