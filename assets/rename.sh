#!/bin/bash

k=10
for i in *.jpg;do
	cp -p "$i" ./$k.jpeg
	k=$((k+1))
done
