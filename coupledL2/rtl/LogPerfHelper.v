`ifndef SIM_TOP_MODULE_NAME
  `define SIM_TOP_MODULE_NAME SimTop
`endif

/*verilator tracing_off*/

module LogPerfHelper (
  output [63:0] timer,
  output        logEnable,
  output        clean,
  output        dump
);

  assign timer = 64'h0;
  assign logEnable = 1'b0;
  assign clean = 1'b0;
  assign dump = 1'b0;

endmodule

