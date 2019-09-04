#!/bin/bash
dir=$1

cd $dir
gcc main.c
cat ../input_output/input.txt | ./a.out
