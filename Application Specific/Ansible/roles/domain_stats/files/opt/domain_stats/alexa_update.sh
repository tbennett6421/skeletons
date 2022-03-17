#!/bin/bash
rm -f top-1m-alexa.csv.zip
/usr/bin/curl http://s3.amazonaws.com/alexa-static/top-1m.csv.zip > top-1m-alexa.csv.zip
/usr/bin/unzip -o top-1m-alexa.csv.zip
mv top-1m.csv top-1m-alexa.csv
rm -f top-1m-alexa.csv.zip
