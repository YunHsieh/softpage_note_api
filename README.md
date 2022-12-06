# Softpage Note API

# Start up
```
python -m venv env
. env/bin/activate

pip3 install poetry
poetry install
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```


Add package
```
poetry add {new package}

```

Build in Docker
```
docker build . -t softpage_note_api
docker run -it --rm \
    -v $(pwd):/softpage_note_api \
    -p 8000:8000 softpage_note_api bash
```
