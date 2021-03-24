pip:
	rm -rf dist/
	python3 setup.py build sdist
	twine upload dist/*

locale:
	./manage.py makemessages -l de -l th -l nb_NO -l fr

checks:
	black --check basxconnect
	flake8 basxconnect
