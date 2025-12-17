#!/bin/bash

k=0
for i in *.jpg;do
	cp -p "$i" ./$k.jpeg
	k=$((k+1))
done
