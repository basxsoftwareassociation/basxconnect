pip:
	rm -rf dist/
	python3 setup.py build sdist
	twine upload dist/*

locale:
	./manage.py makemessages -l de -l th -l nb_NO -l fr -l pt

checks:
	black --check basxconnect
	flake8 basxconnect

raise_and_release_minor_version:
	git push
	git pull
	NEWVERSION=$$(                              \
	   echo -n '__version__ = ' &&              \
	   cat basxconnect/__init__.py |            \
	   cut -d = -f 2 |                          \
	   python3 -c 'i = input().strip().strip("\""); print("\"" + ".".join(i.split(".")[:-1] + [str(int(i.split(".")[-1]) + 1) + "\""]))' \
    ) &&                                        \
	echo $$NEWVERSION > basxconnect/__init__.py
	git commit -m 'bump version' basxconnect/__init__.py && git push && git push --tags
