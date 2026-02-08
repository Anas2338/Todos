#syntax=docker/dockerfile:1

# === Build stage: Create optimized frontend build ===
FROM node:20-alpine AS builder

WORKDIR /app

# Install minimal build dependencies only when needed for native modules
RUN apk add --no-cache python3 make g++

# Copy package files first for better layer caching
COPY package*.json ./

# Install all dependencies (including dev dependencies) for the build process
RUN npm ci --legacy-peer-deps --no-audit --no-fund --progress=false && \
    npm cache clean --force && \
    rm -rf /root/.npm /root/.npm/_cacache /root/.node-gyp

# Copy source code and build (excluding unnecessary files via .dockerignore)
COPY . .

# Temporarily enable standalone output for minimal production build
RUN sed -i "s/const nextConfig = {/const nextConfig = {\n  output: 'standalone',/" next.config.js

# Run the build process
RUN npm run build

# === Production stage: Ultra-minimal runtime image ===
FROM node:20-alpine AS production

# Install only essential runtime dependencies and create user
RUN apk add --no-cache dumb-init && \
    addgroup -g 1001 -S nodejs && \
    adduser -S nextjs -u 1001 -G nodejs

WORKDIR /app

# Set production environment
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Copy only the standalone output and necessary files
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
COPY --from=builder --chown=nextjs:nodejs /app/public ./public

USER nextjs

EXPOSE 3000

# Use dumb-init to handle signals properly
ENTRYPOINT ["/usr/bin/dumb-init"]
CMD ["node", "server.js"]