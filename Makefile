
install:
	sudo python setup.py install

clean:
	git stash
	sudo git clean -dxf

clean_install: clean install
