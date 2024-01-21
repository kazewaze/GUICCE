#!/bin/bash
# GUICCE Shell Script for running .c file with gcc.

eval "gcc $1.c -o $1 && ./$1"