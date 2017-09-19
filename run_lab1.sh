#!/bin/bash

#PBS -N lab1
#PBS -q bitpedu
#PBS -o lab1.out
#PBS -e lab1.err
#PBS -l nodes=2
date
python lab1.py
date
