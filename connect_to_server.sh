#!/bin/bash
# Manual connection script for server
# Use this to connect to the server and run commands manually

SERVER="185.182.158.150"
PORT="8022"

echo "=========================================="
echo "Connecting to server..."
echo "Server: ${SERVER}:${PORT}"
echo "=========================================="
echo ""
echo "After connecting, you can:"
echo "  1. Navigate to the project: cd ~/pyspark_retail"
echo "  2. Run the script: python retail_profiler.py"
echo "  3. View results: ls -lh out_retail/"
echo ""
echo "Connecting now..."
echo ""

ssh -p ${PORT} ${SERVER}
