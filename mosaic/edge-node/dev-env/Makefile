
SHELL := /bin/bash

OAR_PATH=owo-app/target/owo-app-1.0-SNAPSHOT.oar
CONTROLLER=localhost
APP=org.owo.app
USER=karaf
PASSWD=karaf

all:
	source ./tools/devrc

init:
	cd tools && git clone https://github.com/opennetworkinglab/onos.git

build:
	cd owo-app && mvn clean install 

install:
	make build
	onos-app $(CONTROLLER) install! $(OAR_PATH)

clean:
	onos-app $(CONTROLLER) uninstall org.owo.app
