TAGS_FILE = .tags

help:					# List all make commands
	@awk -F ':.*#' '/^[a-zA-Z_-]+:.*?#/ { printf "\033[36m%-15s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST) | sort

designer:  # Open QT designer
	qt6-tools designer

gen-interface:  # Genereate interface.py from interface.ui file
	pyside6-uic interface.ui -o interface.py

docker-windows:  # Build docker image to create windows executable
	docker build -t pyinstaller-python3.11.2 .

release-windows:
	@cmd='pyinstaller --onefile --windowed \
		--name CardioBrain --icon=/src/icons/brain.ico \
		--add-data="/src/icons/brain.ico:." \
		/src/main.py --dist /tmp/windows' && \
	docker run -it -v $$(pwd):/src/ pyinstaller-python3.11.2  $$cmd

release-linux:  # Release GNU/Linux executable
	@tmpdir=$$(mktemp -d) && \
	pyinstaller --onefile --windowed --name CardioBrain --collect-all PySide6 --icon=icons/brain.png main.py \
		--dist "$$tmpdir" && \
	echo "Final file at $$tmpdir"

release-mac:
	pyinstaller main.py \
    --name CardioBrain \
    --windowed \
    --icon icons/brain.png \
    --collect-submodules PySide6.QtWidgets \
    --collect-submodules PySide6.QtGui \
    --collect-submodules PySide6.QtCore \
    --dist ./dist/16_11_2025/

.PHONY: help
