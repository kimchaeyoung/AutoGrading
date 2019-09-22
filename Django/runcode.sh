#!/bin/bash

cd $1
gcc main.c
cat /input_output/input.txt | ./a.out
