"""
module TestTop(
  input          clock,
  input          reset,
  output         master_port_0_0_a_ready, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  input          master_port_0_0_a_valid, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  input  [2:0]   master_port_0_0_a_bits_opcode, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  input  [2:0]   master_port_0_0_a_bits_param, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  input  [2:0]   master_port_0_0_a_bits_size, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  input  [4:0]   master_port_0_0_a_bits_source, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  input  [23:0]  master_port_0_0_a_bits_address, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  input  [1:0]   master_port_0_0_a_bits_user_alias, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  input  [31:0]  master_port_0_0_a_bits_mask, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  input  [255:0] master_port_0_0_a_bits_data, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  input          master_port_0_0_a_bits_corrupt, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  input          master_port_0_0_b_ready, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  output         master_port_0_0_b_valid, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  output [2:0]   master_port_0_0_b_bits_opcode, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  output [1:0]   master_port_0_0_b_bits_param, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  output [2:0]   master_port_0_0_b_bits_size, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  output [4:0]   master_port_0_0_b_bits_source, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  output [23:0]  master_port_0_0_b_bits_address, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  output [31:0]  master_port_0_0_b_bits_mask, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  output [255:0] master_port_0_0_b_bits_data, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  output         master_port_0_0_b_bits_corrupt, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  output         master_port_0_0_c_ready, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  input          master_port_0_0_c_valid, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  input  [2:0]   master_port_0_0_c_bits_opcode, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  input  [2:0]   master_port_0_0_c_bits_param, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  input  [2:0]   master_port_0_0_c_bits_size, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  input  [4:0]   master_port_0_0_c_bits_source, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  input  [23:0]  master_port_0_0_c_bits_address, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  input  [1:0]   master_port_0_0_c_bits_user_alias, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  input  [255:0] master_port_0_0_c_bits_data, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  input          master_port_0_0_c_bits_corrupt, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  input          master_port_0_0_d_ready, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  output         master_port_0_0_d_valid, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  output [2:0]   master_port_0_0_d_bits_opcode, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  output [1:0]   master_port_0_0_d_bits_param, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  output [2:0]   master_port_0_0_d_bits_size, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  output [4:0]   master_port_0_0_d_bits_source, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  output [7:0]   master_port_0_0_d_bits_sink, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  output         master_port_0_0_d_bits_denied, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  output [255:0] master_port_0_0_d_bits_data, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  output         master_port_0_0_d_bits_corrupt, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  output         master_port_0_0_e_ready, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  input          master_port_0_0_e_valid, // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
  input  [7:0]   master_port_0_0_e_bits_sink // @[rocket-chip/src/main/scala/diplomacy/Nodes.scala 1649:17]
);
"""

import random
from typing import Union

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
import cocotb.triggers
from cocotb.types import LogicArray
from TLOP import *


async def AcquireBlock(dut, address: int):

    a = ChannleA()
    a.opcode = OPCodes.A.AcquireBlock
    a.size = 0x6
    a.address = address
    await sendA(dut, a)


async def GrantData(dut) -> Union[int,int]:
    d1 = await getD(dut) 
    while d1.opcode != OPCodes.D.GrantData:
        d1 = await getD(dut)
    d2 = await getD(dut)
    while d2.opcode != OPCodes.D.GrantData:
        d2 = await getD(dut)
    print(f"GrantData {hex(d1.data)} {hex(d2.data)}")
    return (d2.data << 64) | d1.data, d2.sink

async def GrantAck(dut, sink: int):
    e = ChannleE()
    e.sink = sink
    await sendE(dut, e)

async def ReleaseData(dut, address: int, data: int):
    c = ChannleC()
    c.opcode = OPCodes.C.ReleaseData
    c.size = 0x6
    c.address = address
    c.data = data & 0xFFFFFFFFFFFFFFFF
    print(f"ReleaseData {hex(data)}")
    print(f"ReleaseData {hex(c.data)}")
    await sendC(dut, c)
    c.data = (data >> 64) & 0xFFFFFFFFFFFFFFFF
    print(f"ReleaseData {hex(c.data)}")
    await sendC(dut, c)

async def ReleaseAck(dut):
    d = await getD(dut)
    while d.opcode != OPCodes.D.ReleaseAck:
        print(f"ReleaseAck {d.opcode}")
        d = await getD(dut)


    

@cocotb.test()
async def dff_simple_test(dut):
    clock = Clock(dut.clock, 1, units="ns")

    # Reset
    cocotb.start_soon(clock.start(start_high=True))
    dut.reset.value = 1
    for i in range(100):
        await RisingEdge(dut.clock)
    dut.reset.value = 0
    await RisingEdge(dut.clock)

    # AcquireBlock & WriteBack & ReadAgain
    ref_data = [0] * 0x10
    for i in range(100):

        # Read
        address = random.randint(0, 0xF) << 6
        await AcquireBlock(dut, address)
        r_data, sink = await GrantData(dut)
        print(f"Read {address} = {hex(r_data)}")
        assert r_data == ref_data[address>>6]
        await GrantAck(dut, sink)

        # Write
        data = random.randint(0, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF)
        await ReleaseData(dut, address, data)
        ref_data[address>>6] = data
        print(f"Write {address} = {hex(data)}")
        await ReleaseAck(dut)
    