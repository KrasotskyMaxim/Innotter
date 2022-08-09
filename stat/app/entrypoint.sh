#!/bin/bash

sleep 20

python3 consumer.py &
python3 -m uvicorn main:app --host 0.0.0.0 --port 7000 --reload