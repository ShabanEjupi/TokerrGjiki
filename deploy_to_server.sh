#!/bin/bash
# Deployment script for PySpark Retail Profiler
# Target server: 185.182.158.150:8022

SERVER="185.182.158.150"
PORT="8022"
REMOTE_DIR="/home/user/pyspark_retail"  # Adjust username and path as needed

echo "=========================================="
echo "PySpark Retail Profiler - Server Deployment"
echo "=========================================="
echo "Target: ${SERVER}:${PORT}"
echo ""

# Check if SSH key exists
if [ ! -f ~/.ssh/id_rsa ]; then
    echo "⚠ No SSH key found. Generating..."
    ssh-keygen -t rsa -b 4096 -f ~/.ssh/id_rsa -N ""
fi

echo "Step 1: Testing SSH connection..."
ssh -p ${PORT} -o ConnectTimeout=10 -o StrictHostKeyChecking=no ${SERVER} "echo 'Connection successful!'" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Cannot connect to server. Please ensure:"
    echo "   1. Server is accessible at ${SERVER}:${PORT}"
    echo "   2. You have provided your credentials"
    echo "   3. SSH service is running on the server"
    echo ""
    echo "To connect manually, use:"
    echo "   ssh -p ${PORT} username@${SERVER}"
    echo ""
    exit 1
fi

echo "✓ Connection successful!"
echo ""

echo "Step 2: Creating remote directory..."
ssh -p ${PORT} ${SERVER} "mkdir -p ${REMOTE_DIR}"

echo "Step 3: Uploading files..."
scp -P ${PORT} retail_profiler.py ${SERVER}:${REMOTE_DIR}/
scp -P ${PORT} data_kaggle/online_retail.xlsx ${SERVER}:${REMOTE_DIR}/

echo "Step 4: Installing dependencies on remote server..."
ssh -p ${PORT} ${SERVER} << 'ENDSSH'
cd ${REMOTE_DIR}
pip install --user pyspark openpyxl pandas
ENDSSH

echo "Step 5: Running the script on remote server..."
ssh -p ${PORT} ${SERVER} << 'ENDSSH'
cd ${REMOTE_DIR}
python retail_profiler.py
ENDSSH

echo ""
echo "=========================================="
echo "✓ Deployment complete!"
echo "=========================================="
echo "To download results:"
echo "  scp -P ${PORT} -r ${SERVER}:${REMOTE_DIR}/out_retail ."
echo ""
