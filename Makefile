ACTIVATE_VENV = . .venv/bin/activate

dev-env:
	python3 -m venv .venv
	.venv/bin/pip install -r requirements.txt

clean-env:
	rm -rf .venv

start:
	$(ACTIVATE_VENV); uvicorn service:app --reload

test:
	$(ACTIVATE_VENV); pytest .
