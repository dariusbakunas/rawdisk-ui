RESOURCE_DIR = designer
COMPILED_DIR = gui/generated
UI_FILES = main_window.ui
MAIN = rawdisk-ui
PYUIC = pyuic5

COMPILED_UI = $(UI_FILES:%.ui=$(COMPILED_DIR)/ui_%.py)

clean :
	find . -name "*.pyc" -exec rm {} \;

app :
	pyinstaller --noconsole --windowed ${MAIN}.py
	mv dist/${MAIN}.app .
	rm -r dist/
	rm -r build/
	rm ${MAIN}.spec

all : uiy

ui : $(COMPILED_UI)

$(COMPILED_DIR)/ui_%.py : $(RESOURCE_DIR)/%.ui
	$(PYUIC) $< -o $@