# matelight-pixel

Pixel wall for Mate-Light

## How to setup development environment

You need:

- python 3.10+
- poetry
- npm

How to install:

- `npm install` - installs tailwindcss
- `poetry set virtualenvs.in-project`  - to make sure your venv will be stored inside as '.venv/' this project folder
- `poetry install` - installs all python dependencies

During development:

- Run `npm run dev` and leave it running, it will automatically scan your HTML files and only include CSS classes that are needed.
- Run `poetry run uvicorn matelight_pixel.main:app --reload` to start the development version of the server.
- Go to http://localhost:8000 to see the site.

