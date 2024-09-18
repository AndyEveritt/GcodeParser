SHELL := /bin/bash
verbosity=1

#########################################
# bumpversion Usage
#########################################
# `bumpversion [major|minor|patch|build]`
# `bumpversion --tag release

update_dist:
	python -m pytest
	rm dist/* -f
	python setup.py sdist bdist_wheel

check_dist: update_dist
	python -m twine check dist/*

upload_test: check_dist
	python -m twine upload --repository testpypi dist/*

upload: check_dist
	python -m twine upload dist/*