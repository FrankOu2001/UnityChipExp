# Makefile

SIM = verilator
TOPLEVEL_LANG = verilog
TEST_SOURCE =  $(shell pwd)/../

waves = True
EXTRA_ARGS += --coverage --trace-fst --timescale 1ns/1ps
EXTRA_ARGS += -f ${TEST_SOURCE}/filelist.txt
PLUSARGS += --trace

# VERILOG_SOURCES = ${TEST_SOURCE}/rtl/TestTop.v
TOPLEVEL = TestTop
MODULE = TLTest

include $(shell cocotb-config --makefiles)/Makefile.sim

