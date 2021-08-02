# terra-test-runner-dashboard (Under Development)
This is the codebase for Terra Test Runner Dashboard.

# Setting up development environment for this repo
* Download [PyCharm Professional](https://www.jetbrains.com/pycharm/).
* Make sure to have the latest [Python 3](https://www.python.org/download/releases/3.0/) installed.
* Import this repo into `PyCharm` as a `Flask` project with the following settings:
  * Select `Virtualenv` as New environment
  * Use default `Location`
  * Select the `Base interpreter` location (e.g. `/usr/local/bin/python3.8`)
  * Keep the default settings (Template language: `Jinga2`, Template folder: `templates`) under `More Settings`

# Build the project
1. Run the following command in the root directory
```
pip install -r requirements.txt
```
2. Change directory to `react` and execute the following commands in order
   
* Install all dependencies in `package.json`
```
npm install
```

* Compilation / Transpilation (Generate component library)
```
npm build
```