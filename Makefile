pip:
	rm -rf dist/
	python3 setup.py build sdist
	twine upload dist/*

locale:
	cd basxconnect/core && ../../manage.py makemessages -l de
