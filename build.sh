#!/usr/bin/env bash

rm -rf ./dist/

python setup.py sdist
python setup.py bdist_wheel
python setup.py clean

rm -rf ./build
rm -rf ./*.egg-info
