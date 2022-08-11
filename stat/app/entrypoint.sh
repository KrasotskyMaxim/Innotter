#!/bin/bash

sleep 20

python3 consumer.py &
echo "start 15 seconds..."
sleep 15 # need to make dynamodb operations before seconad app will starts (in case of localstack only)
python3 -m uvicorn main:app --host 0.0.0.0 --port 7000 --reload