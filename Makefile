RESOURCE_DIR = designer
COMPILED_DIR = gui/generated
UI_FILES = main_window.ui
MAIN = rawdisk-ui
PYUIC = pyuic5

COMPILED_UI = $(UI_FILES:%.ui=$(COMPILED_DIR)/ui_%.py)

clean :
	find . -name "*.pyc" -exec rm {} \;
	rm -rf dist/
	rm -rf build/
	rm -f ${MAIN}.spec
	rm -rf ${MAIN}.app

app :
	pyinstaller --noconsole --windowed ${MAIN}.py
	mv dist/${MAIN}.app .

ui : $(COMPILED_UI)

osx : clean ui app

$(COMPILED_DIR)/ui_%.py : $(RESOURCE_DIR)/%.ui
	$(PYUIC) $< -o $@