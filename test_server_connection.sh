#!/bin/bash
# Test server connection and environment

SERVER="185.182.158.150"
PORT="8022"

echo "=========================================="
echo "Server Environment Test"
echo "=========================================="

# Prompt for username
read -p "Enter SSH username: " USERNAME

if [ -z "$USERNAME" ]; then
    echo "❌ Username cannot be empty"
    exit 1
fi

echo ""
echo "Testing connection to ${USERNAME}@${SERVER}:${PORT}..."
echo ""

# Test 1: Basic connectivity
echo "Test 1: Connection test..."
ssh -p ${PORT} -o ConnectTimeout=10 ${USERNAME}@${SERVER} "echo '✓ Connection successful'" 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Connection failed"
    exit 1
fi

echo ""
echo "Test 2: Checking Python..."
ssh -p ${PORT} ${USERNAME}@${SERVER} "python3 --version" 2>&1

echo ""
echo "Test 3: Checking Java (required for PySpark)..."
ssh -p ${PORT} ${USERNAME}@${SERVER} "java -version" 2>&1

echo ""
echo "Test 4: Checking pip..."
ssh -p ${PORT} ${USERNAME}@${SERVER} "pip3 --version" 2>&1

echo ""
echo "Test 5: Checking disk space..."
ssh -p ${PORT} ${USERNAME}@${SERVER} "df -h ~" 2>&1

echo ""
echo "Test 6: Checking installed Python packages..."
ssh -p ${PORT} ${USERNAME}@${SERVER} "pip3 list | grep -E '(pyspark|pandas|openpyxl)'" 2>&1

echo ""
echo "=========================================="
echo "Test complete!"
echo "=========================================="
echo ""
echo "To proceed with deployment:"
echo "1. Edit deploy_to_server.sh and set USERNAME variable"
echo "2. Run: ./deploy_to_server.sh"
echo ""
