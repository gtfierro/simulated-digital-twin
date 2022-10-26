#!/bin/bash
set -ex

git submodule init
git submodule update --init --recursive

cd boptest-bacnet-proxy
git apply ../boptest-proxy.patch
cp ../Dockerfile.boptest-proxy Dockerfile
cp ../run.sh .

cd ../project1-boptest
git apply ../boptest.patch

cd ..
make build
