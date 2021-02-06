.PHONY: all

all: build

build:
	python ch-vaccinations.py

push:
	data push data/datapackage.json