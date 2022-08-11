## Initialize for dev update

```
$ python -m virtualenv venv --python=python3.10
$ (venv) pip install pygame 
$ pip freeze > requirements.txt
```

## Getting started
Windows
```
$ python -m virtualenv venv --python=python3.10
$ pip install -r requirements.txt 
$ venv\Scripts\activate
$ (venv) python index.py
```

## External Modules
- https://github.com/cosmologicon/pygame-text

## Build Exe File
```
$ pyinstaller -w -F --icon="resources/images/icon.png" index.py
```

## Preview
version 08/12
https://user-images.githubusercontent.com/12585089/184223333-b05d7020-5ea2-42ac-ae2a-23b32eff667b.mp4


version 08/11
https://user-images.githubusercontent.com/12585089/183978473-70ce7bbf-0685-431d-b12a-b625f2395bd1.mp4

