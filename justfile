set shell := ["powershell.exe", "-c"]

run:
    @python src/main.py

test:
    @python -m unittest discover -s src -p "*_test.py"