.DEFAULT_GOAL := build


.PHONY: sysdeps
sysdeps:  # run with sudo
	sudo apt-get install python3-dev
	sudo apt-get install libasound2-dev
	sudo apt-get install libjack-dev


.PHONY: ve deps
deps:
	ve/bin/pip install coconut  # functional programming addons to Python
	ve/bin/pip install python-rtmidi==1.1.0 mido  # MIDI IO
	ve/bin/pip install thespian  # actor system
	ve/bin/pip install green  # testing


.PHONY: clean-ve
clean-ve:
	rm -rf ve


.PHONY: clean-pycs
clean-pycs:
	find . -name *.pyc -delete


.PHONY: clean
clean: clean-ve clean-pycs


.PHONY: ve
ve:
	ls ve || virtualenv ve -p python3 --system-site-packages --clear


.PHONY: compile
compile:
	coconut --keep-lines --line-numbers --target 35 .


.PHONY:
test:
	green


.PHONY: build
build: ve deps compile
