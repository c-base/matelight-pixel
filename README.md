# matelight-pixel

Pixel wall for Mate-Light

## How to setup development environment

You need:

- python 3.10+
- poetry (or pip)
- npm

How to install:

- `npm install` - installs tailwindcss
- install python dependencies with poetry:
  - `poetry set virtualenvs.in-project`  - to make sure your venv will be stored inside as '.venv/' this project folder
  - `poetry install` - installs all python dependencies
- if you want to use pip:
  - setup your virtual environment: `python3 -m venv .venv`
  - activate your virtual environment: `source .venv/bin/activate`
  - to install, run `pip install -r requirements.txt`

During development:

- Run `npm run dev` and leave it running, it will automatically scan your HTML files and only include CSS classes that are needed.
- Run `poetry run uvicorn matelight_pixel.main:app --reload` to start the development version of the server.
- Run `source .venv/bin/activate` then `uvicorn matelight_pixel.main:app --reload` if you are using pip.        
- Go to http://127.0.0.1:8000 to see the site.

