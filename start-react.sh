#!/bin/bash

echo "🚀 Setting up SPVP React Frontend..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Navigate to React frontend
cd react-frontend

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Start the React development server
echo "🌐 Starting React development server..."
npm start
