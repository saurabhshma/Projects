#!/bin/bash
for ((i = 100; i <= 1000; i+=100));
do
#	./client $i 2000 output_2000_netem.txt 10.205.156.230
#	./client $i 8000 output_8000.txt 10.205.156.230
	./client $i 2000 test_output localhost
#	./client $i 2000 output_2000.txt 10.205.156.230
done
