# Twine
twine: niemarkov/__init__.py niemarkov/niemarkov.py
	python3 setup.py sdist bdist_wheel
	twine upload dist/*.tar.gz
clean:
	$(RM) -r build dist *.egg-info
