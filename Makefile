
install:
	sudo python setup.py install

clean:
	git stash
	sudo git clean -dxf

tests:
	radish $(RADISH_OPTS) -b tests/ tests/features/active/*

clean_install: clean install

.PHONY: tests clean install
