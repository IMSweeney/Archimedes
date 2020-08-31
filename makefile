test:
	python -m unittest discover tests

run:
	python application.py

profile:
	python -m cProfile -o program.prof application.py
	python -m snakeviz program.prof

view_profile:
	python -m snakeviz program.prof