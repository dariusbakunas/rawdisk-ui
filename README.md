# rawdisk-ui

![Main Window](/docs/screens/screen02.png?raw=true "Main Window")

### Dependencies

* PyQt5
* Qt 5
* Python 3

### TODO:

* Add address section
* Add ascii section
* Add cursor
* Add ability to highlight sections
* Use rawdisk library for fs detection

### Install requirements:

    % pip install -r requirements.txt

### Compiling qt templates:

    % pyuic5 -x designer/main_window.ui -o gui/generated/ui_main_window.py

    or

    % make ui

### Building OSX app bundle:
    
    % make app

#### Resources

* [makefile for pyqt](https://mplicka.cz/en/blog/compiling-ui-and-resource-files-with-pyqt)