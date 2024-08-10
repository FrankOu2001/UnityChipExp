# Variables
TOP_ENTRY := ../rtl/RAS.sv
TOP_FILES := ./RAS.txt
TL ?= python

# Default target directory
TARGET ?= ./out/picker_out_RAS

# Verbosity
_VERBOSE := $(if $(VERBOSE), --verbose, )
_WAVEFORM := -w RAS.fst

# Targets
.PHONY: all ras clean

all: ras

ras:
	@echo "Building tag module with parameters:"
	@echo "TL=${TL}"
	@echo "TOP_ENTRY=${TOP_ENTRY}"
	@echo "TOP_FILES=${TOP_FILES}"
	@echo "TARGET=${TARGET}"
	@echo "WAVEFORM=${_WAVEFORM}"
	@echo "VERBOSE=${_VERBOSE}"
	@echo ""

	@mkdir -p $(dir ${TARGET})
	@rm -rf ${TARGET}
	@picker export ${TOP_ENTRY} --filelist ${TOP_FILES} --language ${TL} -c\
		 --target_dir ${TARGET} ${_WAVEFORM} ${_VERBOSE} --internal RAS_internals.yaml

clean:
	@echo "Cleaning up..."
	@rm -rf ./out
	@echo "Done."

