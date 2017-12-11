RESOURCE_DIR = designer
COMPILED_DIR = gui/generated
UI_FILES = main_window.ui
PYUIC = pyuic5

COMPILED_UI = $(UI_FILES:%.ui=$(COMPILED_DIR)/ui_%.py)

all : ui

ui : $(COMPILED_UI)

$(COMPILED_DIR)/ui_%.py : $(RESOURCE_DIR)/%.ui
	$(PYUIC) $< -o $@