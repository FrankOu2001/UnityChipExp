TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES = $(shell pwd)/../rtl/RAS.sv \
                  $(shell pwd)/../rtl/DelayN_2.sv \
                  $(shell pwd)/../rtl/RASStack.sv \
                  $(shell pwd)/../rtl/ext_sram.v \
                  $(shell pwd)/../rtl/DelayNWithValid.sv

TOPLEVEL = RAS
MODULE = test_ras

waves = True
# SIM ?= icarus
SIM ?= verilator

# Additional Verilator arguments (if using Verilator)
# Uncomment and use the following lines if you switch to Verilator
EXTRA_ARGS +=  --trace-fst --coverage
PLUSARGS += --trace
# VERILATOR_CXX_FLAGS += -I$(shell cocotb-config --share)/include
# VERILATOR_LDFLAGS += -L$(shell cocotb-config --lib-dir) -lcocotbvpi_verilator

# Include the modified verilator.cpp if necessary
# Uncomment the following line if you have a custom verilator.cpp file
# EXTRA_ARGS += --exe verilator.cpp

include $(shell cocotb-config --makefiles)/Makefile.sim

# Custom target to run pytest
.PHONY: pytest
pytest:
	pytest -v

# Run all targets
.PHONY: all
all: $(SIM) pytest
