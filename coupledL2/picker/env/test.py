import mlvp
import random
from mlvp.triggers import *
from UT_CoupledL2 import DUTCoupledL2
from bundle import TileLinkBundle
from agent import TileLinkAgent

async def test_top(dut: DUTCoupledL2):
    mlvp.start_clock(dut)
    dut.reset.value = 1
    await ClockCycles(dut)
    dut.reset.value = 0

    tlbundle = TileLinkBundle.from_prefix("master_port_0_0_").bind(dut)
    tlbundle.set_all(0)
    tlagent = TileLinkAgent(tlbundle)


    ref_data = [0] * 0x10
    
    for _ in range(100):

        # Read
        address = random.randint(0, 0xF) << 6
        r_data = await tlagent.aquire_block(address)
        print(f"Read {address} = {hex(r_data)}")
        assert r_data == ref_data[address>>6]

        # Write
        send_data = random.randint(0, 2**512)
        await tlagent.release_data(address, send_data)
        ref_data[address>>6] = send_data
        print(f"Write {address} = {hex(send_data)}")


if __name__ == "__main__":
    mlvp.setup_logging(mlvp.INFO)
    dut = DUTCoupledL2()
    dut.InitClock("clock")
    dut.reset.AsImmWrite()

    mlvp.run(test_top(dut))

    dut.Finish()
