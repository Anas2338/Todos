#!/usr/bin/env node

// Script to extract only production dependencies from package.json

const fs = require('fs');
const path = require('path');

// Read the original package.json
const packageJsonPath = path.join(process.cwd(), 'fullstack-todo', 'frontend', 'package.json');
const originalPackageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));

// Create a new package.json with only production dependencies
const productionPackageJson = {
  name: originalPackageJson.name,
  version: originalPackageJson.version,
  private: originalPackageJson.private,
  scripts: {
    start: originalPackageJson.scripts.start,
    build: originalPackageJson.scripts.build
  },
  dependencies: originalPackageJson.dependencies
};

// Write the production-only package.json
const outputPath = path.join(process.cwd(), 'fullstack-todo', 'frontend', 'package.prod.json');
fs.writeFileSync(outputPath, JSON.stringify(productionPackageJson, null, 2));

console.log('Production-only package.json created at package.prod.json');