#!/bin/bash
echo "Clean __pycache__."
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

DIR="build_dir"
 
if [ -d $DIR ];then
  echo "Clean Build Dir."
  rm -rf $DIR
fi

mkdir -p $DIR/function
pip install \
    --platform manylinux2014_x86_64 \
    --target=$DIR/function \
    --implementation cp \
    --python 3.10 \
    --only-binary=:all: --upgrade \
    -r requirements.txt
cd $DIR/function

zip -r9 ../function.zip .
cd ../../
zip -g $DIR/function.zip -r app