# terra-test-runner-dashboard (Under Development)
This is the codebase for Terra Test Runner Dashboard.

# Setting up development environment for this repo
* Install [PyCharm Professional](https://www.jetbrains.com/pycharm/)
* You will need Python version 3. Install the latest version of Python if needed. Currently, the latest version is [3.10.0](https://www.python.org/downloads/) for macOS.
  * [How to set up Python 3 as default on macOS](https://opensource.com/article/19/5/python-3-default-mac)
* Install the latest version of [pip](https://pip.pypa.io/en/stable/installation/) if needed
  * To upgrade `pip`, run `python3 -m pip install --upgrade pip`
* Update gcloud components
  * Config gcloud to use the latest version of Python, run `export CLOUDSDK_PYTHON=/usr/bin/python3`.
  * Run `gcloud components update`
* `npm` is needed. Using Node version manager to install the latest version of [`npm`](https://nodejs.org/en/download/)
* Import this repo into `PyCharm` as a `Flask` project with the following settings:
  * Select `Virtualenv` as New environment
  * Use default `Location`
  * Select the `Base interpreter` location (e.g. `/usr/local/bin/python3.8`)
  * Keep the default settings (Template language: `Jinga2`, Template folder: `templates`) under `More Settings`

# Build the project
1. Run the following command in the root directory
```commandline
pip install -r requirements.txt
```
2. Change directory to `test_runner_components` and execute the following commands in order
   
* Install all dependencies in `package.json`. After executing the following command, a new `node_modules` subdirectory that contains all the dependent modules will be created.
```commandline
npm install
```

* Run build script. Compile the `React.js` components in `src/lib/components` and convert them into `Python` modules consumable by the `Dash MVC` framework. The modules are created under the `test_runner_components` subdirectory.
```commandline
npm run build
```
  * In case of build failure related to `dash`, install `dash` by run `pip install dash`
# Test your environment

In the `test_runner_components` directory, run the following command and point your browser to `https://localhost:8050`

```commandline
python usage.py
```
  * In case it failes with `ImportError: No module named 'yaml'`
    * run `sudo python3 -m pip install pyyaml`)

  * If all goes well, your browser should render the `ExcampleComponent` and you should be able to interact with the text field and observe corresponding response to `onchange` events.

# Deployment of Main `Dash` Application

The project is structured such that the main application resides in the root directory separate from `test_runner_components`. 

This promotes clean separation between UI code and Application Context.

In order for the main `Dash` application to use the custom `test_runner_components`, we need to install them first by executing the following command from the root directory. This will build and create the wheel for `test_runner_components` and install the packages.

```commandline
pip install ./test_runner_components/
```

DEPRECATION Note: A future pip version will change local packages to be built in-place without first copying to a temporary directory. We recommend you use `--use-feature=in-tree-build` to test your packages with this new behavior before it becomes the default. 
`pip 21.3` will remove support for this functionality. You can find discussion regarding this at https://github.com/pypa/pip/issues/7555.

To test that installation of `test_runner_components`, run the following `example.py` from the root directory and point your browser at http://127.0.0.1:8050/

```commandline
python example.py
```

If all goes well, your browser should render the `ExcampleComponent` and you should be able to interact with the text field and observe corresponding response to `onchange` events.
