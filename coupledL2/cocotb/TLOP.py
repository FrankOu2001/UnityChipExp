from cocotb.triggers import RisingEdge

# TileLink TL-C operation codes
class OPCodes:
    class A:
        PutFullData = 0x0
        PutPartialData = 0x1
        ArithmeticData = 0x2
        LogicalData = 0x3
        Get = 0x4
        Hint = 0x5
        AcquireBlock = 0x6
        AcquirePerm = 0x7

    class B:
        ProbeBlock = 0x6
        ProbePerm = 0x7

    class C:
        ProbeAck = 0x4
        ProbeAckData = 0x5
        Release = 0x6
        ReleaseData = 0x7

    class D:
        AccessAck = 0x0
        AccessAckData = 0x1
        HintAck = 0x2
        Grant = 0x4
        GrantData = 0x5
        ReleaseAck = 0x6

    class E:
        GrantAck = 0x4

class Channel:

    def __str__(self):
        res = self.__class__.__name__
        for name in self.__dict__:
            res += f"\n{name}: {getattr(self, name)}"
        res += "\n ---------------------"
        return res

class ChannleA(Channel):

    def __init__(self):
        self.opcode = 0x0
        self.param = 0x0
        self.size = 0x0
        self.source = 0x0
        self.address = 0x0
        self.user_alias = 0x0
        self.mask = 0x0
        self.data = 0x0
        self.corrupt = 0x0


class ChannleB(Channel):

    def __init__(self):
        self.opcode = 0x0
        self.param = 0x0
        self.size = 0x0
        self.source = 0x0
        self.address = 0x0
        self.mask = 0x0
        self.data = 0x0
        self.corrupt = 0x0

class ChannleC(Channel):

    def __init__(self):
        self.opcode = 0x0
        self.param = 0x0
        self.size = 0x0
        self.source = 0x0
        self.address = 0x0
        self.user_alias = 0x0
        self.data = 0x0
        self.corrupt = 0x0

class ChannleD(Channel):

    def __init__(self):
        self.opcode = 0x0
        self.param = 0x0
        self.size = 0x0
        self.source = 0x0
        self.sink = 0x0
        self.denied = 0x0
        self.data = 0x0
        self.corrupt = 0x0

class ChannleE(Channel):
    
    def __init__(self):
        self.sink = 0x0
        
async def sendA(dut, a: ChannleA):
    while dut.master_port_0_0_a_ready.value == 0x0:
        await RisingEdge(dut.clock)
    dut.master_port_0_0_a_valid.value = 0x1
    for name in a.__dict__:
        getattr(dut, f"master_port_0_0_a_bits_{name}").value = getattr(a, name)
    await RisingEdge(dut.clock)
    dut.master_port_0_0_a_valid.value = 0x0

async def getB(dut) -> ChannleB:
    dut.master_port_0_0_b_ready.value = 0x1
    while dut.master_port_0_0_b_valid.value == 0x0:
        await RisingEdge(dut.clock)
    b = ChannleB()
    for name in b.__dict__:
        setattr(b, name, getattr(dut, f"master_port_0_0_b_bits_{name}").value)
    await RisingEdge(dut.clock)
    dut.master_port_0_0_d_ready.value = 0x0
    return b

async def sendC(dut, c: ChannleC):
    while dut.master_port_0_0_c_ready.value == 0x0:
        await RisingEdge(dut.clock)
    dut.master_port_0_0_c_valid.value = 0x1
    for name in c.__dict__:
        getattr(dut, f"master_port_0_0_c_bits_{name}").value = getattr(c, name)
    await RisingEdge(dut.clock)
    dut.master_port_0_0_c_valid.value = 0x0

async def getD(dut) -> ChannleD:
    dut.master_port_0_0_d_ready.value = 0x1
    while dut.master_port_0_0_d_valid.value == 0x0:
        await RisingEdge(dut.clock)
    d = ChannleD()
    for name in d.__dict__:
        setattr(d, name, getattr(dut, f"master_port_0_0_d_bits_{name}").value)
    await RisingEdge(dut.clock)
    dut.master_port_0_0_d_ready.value = 0x0
    return d

async def sendE(dut, e: ChannleE):
    while dut.master_port_0_0_e_ready.value == 0x0:
        await RisingEdge(dut.clock)
    dut.master_port_0_0_e_valid.value = 0x1
    for name in e.__dict__:
        getattr(dut, f"master_port_0_0_e_bits_{name}").value = getattr(e, name)
    await RisingEdge(dut.clock)
    dut.master_port_0_0_e_valid.value = 0x0