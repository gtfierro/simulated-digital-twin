#!/bin/bash

while true ; do
    sleep 10 
    python BopTestProxy.py simple.ttl 19740 3600 --baseurl http://boptest:5000
done
