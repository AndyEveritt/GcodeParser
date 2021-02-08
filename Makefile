SHELL := /bin/bash
verbosity=1

#########################################
# bumpversion Usage
#########################################
# `bumpversion [major|minor|patch|build]`
# `bumpversion --tag release

update_dist:
	rm dist/* -f
	python setup.py sdist bdist_wheel

check_dist:
	twine check dist/*

upload_test: check_dist
	twine upload --repository testpypi dist/*

upload: check_dist
	twine upload dist/*