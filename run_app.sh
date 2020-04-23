#!/bin/sh
docker build -t flask-app .
docker run --name flask-app -p 5000:5000 -v $(pwd):/app/ -itd flask-app