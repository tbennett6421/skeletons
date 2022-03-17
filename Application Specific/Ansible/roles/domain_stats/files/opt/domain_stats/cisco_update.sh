#!/bin/bash
rm -f top-1m-cisco.csv.zip
/usr/bin/curl http://s3-us-west-1.amazonaws.com/umbrella-static/top-1m.csv.zip > top-1m-cisco.csv.zip
/usr/bin/unzip -o top-1m-cisco.csv.zip
mv top-1m.csv top-1m-cisco.csv
rm -f top-1m-cisco.csv.zip
