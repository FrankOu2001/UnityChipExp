import sys
import os
import ras_wrapper as p
import random
import pytest
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "../out/picker_out_RAS"))
sys.path.append(os.path.join(os.path.dirname(__file__), "../utils"))

import UT_RAS as ras

def init_ras_pins():
    out_dir = os.path.join(os.path.dirname(__file__), "./report")
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    dut = ras.DUTRAS(
        waveform_filename=os.path.join(out_dir, f"RAS.fst"),
        coverage_filename=os.path.join(out_dir, f"RAS.dat")
    )
    dut.InitClock("clock")
    return p.RASPins(dut)

# picker_time = 0
# @pytest.fixture
# def ras_object():
#     print("Fixture setup started")
#     ras = init_ras_pins()
#     print("ras对象已创建")
#     start_time = time.time()
    
#     yield ras
    
#     print("Starting teardown...")
#     global picker_time
#     picker_time += (time.time() - start_time)
#     print("picker time = ", picker_time)
#     ras.Finish()
#     print("ras对象已销毁")

@pytest.fixture(scope="session")
def ras_object():
    print("Fixture setup started")
    ras = init_ras_pins()
    print("ras对象已创建")
    start_time = time.time()
    
    yield ras
    
    print("Starting teardown...")
    picker_time = time.time() - start_time
    print("picker time = ", picker_time)
    ras.Finish()
    print("ras对象已销毁")
##########################################################################

def test_ras_push(ras_object):

    ras = ras_object
    ras.reset()
    # create dut_pins
    push_num =  random.randint(1,32)    # spec max siez == 32
    push_addr = {}
    for i in range(push_num):
        ras.push(0x80000000 + i*4)
        push_addr[i] = 0x80000000 + i*4
    for i in range(push_num-1, -1, -1):
        atter_name  = f"RAS_RASStack_spec_queue_{i}_retAddr"
        spec_obj = getattr(ras, atter_name)
        assert spec_obj.value == push_addr[i]



def test_ras_spec_push_overflow(ras_object):  # spec压栈溢出
    # create dut_pins
    ras = ras_object
    ras.reset()
    push_num =  33 # spec max siez == 32
    push_addr = {}
    for i in range (push_num):
        push_addr[i] = 0x80000000 + i*4
    for i in range(push_num):
        ras.push(0x80000000 + i*4)
    assert(ras.dut.RAS_RASStack_spec_overflowed.value == 1)
    assert(ras.dut.RAS_RASStack_BOS_value.value == 1)



def test_ras_spec_pop(ras_object):  # spec pop
    # create dut_pins
    ras = ras_object
    ras.reset()
    push_num =  random.randint(1,32)    #max spec size == 32
    push_addr = {}
    for i in range (push_num):
        push_addr[i] = 0x80000000 + i*4
        ras.push(push_addr[i])
    for i in range(push_num-1, -1, -1):
        pop_addr = ras.pop()
        assert(pop_addr == push_addr[i])



# spec 压入相同的地址检查TOSR是否为0，0号地址的ctr是否为7
def test_ras_check_tosr_same_addr(ras_object):    # 测试spec count
    ras = ras_object
    # create dut_pins
    ras.reset()
    # test
    push_num = 8    #max sctr
    for _ in range(push_num+1):
        ras.push(0x80000000 )
        end_TOSR = ras.dut.RAS_RASStack_TOSR_value.value
    assert(end_TOSR == 0)
    assert(ras.dut.RAS_RASStack_spec_queue_0_ctr == 7)

# ###################################################################################
# # commit压栈

def test_ras_commit_push(ras_object): 
    ras = ras_object
    ras.reset()
    # set coverage
    size = 32    #max sctr
    meta = {}
    for i in range(size): 
        meta[i] =ras.push(0x80000000 + i*4)
    # set coverage
    commit_stack_addr = {}
    push_addr = {}
    commit_num = 16
    for i in range(commit_num):
        commit_stack_addr[i] = -1
        push_addr[i] = 0x80000000 + i*4

    for i in range(commit_num):
        atter_name  = f"RAS_RASStack_commit_stack_{int(meta[i+1%16]['ssp'])}_retAddr"
        commit_obj = getattr(ras.dut, atter_name)
        ras.commit_push(meta[i])
        assert(commit_obj.value == 0x80000000 + i*4)


# sepc 溢出 commit 压栈

def test_ras_spec_overflow_commit_push(ras_object): 
    ras = ras_object
    ras.reset()
    # set coverage
    size = 32    #max sctr
    meta = {}
    for i in range(size+1): 
        meta[i] =ras.push(0x80000000 + i*4)
   
    # set coverage
    commit_stack_addr = {}
    push_addr = {}
    for i in range(16):
        commit_stack_addr[i] = -1
        push_addr[i] = 0x80000000 + i*4

    for i in range(16):
        atter_name  = f"RAS_RASStack_commit_stack_{meta[i+1%16]['ssp']}_retAddr"
        commit_obj = getattr(ras.dut, atter_name)
        ras.commit_push(meta[i])
        assert(commit_obj.value == push_addr[i])



# spec压入相同的地址，commit之后检查commit的count和栈顶指针

def test_ras_spec_push_same_addr_and_commit_and_check_commit_count_and_top_ptr(ras_object): 
    ras = ras_object
    ras.reset()
    # create dut_pins
    meta = {}
    for i in range(8):
        meta[i] =ras.push(0x80000000)
    # cover ssp
    # set coverage
    for i in range(8):
        ras.commit_push(meta[i])
    assert(ras.dut.RAS_RASStack_commit_stack_1_retAddr.value == 0x80000000)
    assert(ras.dut.RAS_RASStack_commit_stack_1_ctr.value == 7)


# 随机COMMIT SPEC栈的元素
def test_ras_commit_random(ras_object): 
    ras = ras_object
    ras.reset()
    commit_addr = random.randint(2,30)
    meta = {}
    for i in range(32):
        meta[i] = ras.push(0x80000000 + i*4)
    # set coverage
    atter_name  = f"RAS_RASStack_commit_stack_{meta[commit_addr]['ssp']+1}_retAddr"
    commit_obj = getattr(ras.dut, atter_name)

    ras.commit_push(meta[commit_addr])
    assert(commit_obj.value == 0x80000000 + meta[commit_addr]['ssp']*4)


# 测试commit栈彻底被使用过一次之后BOS能否回归原位

def test_ras_commit_full_use(ras_object):
    ras = ras_object
    ras.reset()
    meta = {}

    for i in range(16):
        for j in range(8):
            meta[j] = ras.push(0x80000000 + i*4)
        for j in range(8):
             ras.commit_push(meta[j])
        for j in range(8):
             ras.pop()
        for j in range(8):
             ras.commit_pop(meta[j])

    for i in range(16):
        for j in range(8):
            meta[j] = ras.push(0x80000000)
        for j in range(8):
            ras.commit_push(meta[j])
    for i in range(16):
        for j in range(8):
            ras.pop()
        for j in range(8):
            ras.commit_pop(meta[j])
    m = ras.push(0x66666666)

    ras.commit_push(m)
    assert(ras.dut.RAS_RASStack_BOS_value.value == 0)

#--------------------------------------------------------------------------------------------------------------------------------------------------#
# spec栈满 S2 push，S3 keep -> spec pop

def test_ras_update_pop_1(ras_object): # 测试spec push
    ras = ras_object
    ras.reset()
    for i in range(32):
        ras.push(0x80000000 + i*4)
    ras.keep_after_push(0x80000000)
    assert(ras.dut.RAS_RASStack_spec_queue_31_retAddr.value == 0x80000000 + 31*4)


# spec还剩一个空间  keep -> spec pop

def test_ras_update_pop_1_spec_31_element(ras_object): # 测试spec push
    ras = ras_object
    ras.reset()
    for i in range(31):
        ras.push(0x80000000 + i*4)

    ras.keep_after_push(0x80000000)
    assert(ras.dut.RAS_RASStack_spec_queue_30_retAddr.value == 0x80000000 + 30*4)


# spec栈满 S2 push，S3 keep -> spec pop 再出栈

def test_ras_update_pop_1_spec_full(ras_object): # 测试spec push
    ras = ras_object
    ras.reset()
    for i in range(32):
        ras.push(0x80000000 + i*4)
    ras.keep_after_push(0x80000000)
    value = ras.pop()
    assert(value == 0x80000000+31*4)


# spec还剩一个空间  keep -> spec pop 再出栈

def test_ras_spec_pop_update_pop_1_spec_31_element(ras_object): # 测试spec push
    ras = ras_object
    ras.reset()
    for i in range(31):
        ras.push(0x80000000 + i*4)
    ras.keep_after_push(0x80000000)
    value = ras.pop()
    assert(value == 0x80000000+30*4)


# spec为空的时候 S2 push，S3 keep -> spec pop

def test_ras_spec_pop_update_pop_1_spec_empty(ras_object):  
    ras = ras_object
    ras.reset()
    # set coverage
    ras.keep_after_push(0x80000000)
    value = ras.pop()
    assert(value == 0x00000000)


# spec有一个元素的时候 S2 push，S3 keep -> spec pop

def test_ras_spec_pop_update_pop_1_spec_1_element(ras_object):  
    ras = ras_object
    ras.reset()
    # set coverage
    ras.push(0x80000008)
    ras.keep_after_push(0x80000000) 
    value = ras.pop()
    assert(value == 0x80000008)


def test_ras_update_pop_2_spec_full(ras_object): # 测试spec push
    ras = ras_object
    ras.reset()
    for i in range(32):
        ras.push(0x80000000 + i*4)
    ras.pop_after_keep()
    value = ras.pop()
    assert(value == 0x80000000+(32-2)*4)


# # spec还剩一个空间 S2 keep，S3 Pop -> spec pop

def test_ras_update_pop_2_spec_31_element(ras_object): # 测试spec push
    ras = ras_object
    ras.reset()
    for i in range(31):
        ras.push(0x80000000 + i*4)
    ras.pop_after_keep()

    value = ras.pop()
    assert(value == 0x80000000+(31-2)*4)

# spec栈满 S2 keep，S3 Pop -> spec pop 再出栈

def test_ras_spec_pop_with_update_pop_2_spec_full(ras_object): # 测试spec push
    ras = ras_object
    ras.reset()
    for i in range(32):
        ras.push(0x80000000 + i*4)
    ras.pop_after_keep()

    # g.sample()
    value = ras.pop()
    assert(value == 0x80000000+(32-2)*4)


# spec还剩一个空间 S2 keep，S3 Pop -> spec pop再出栈

def test_ras_spec_pop_update_pop_2_spec_31_element(ras_object): # 测试spec push
    ras = ras_object
    ras.reset()
    for i in range(31):
        ras.push(0x80000000 + i*4)
    ras.pop_after_keep()

    value = ras.pop()
    assert(value == 0x80000000+29*4)


# spec为空的时候 S2 keep，S3 Pop -> spec pop

def test_ras_spec_pop_update_pop_2_empty(ras_object):  
    ras = ras_object
    ras.reset()
    ras.pop_after_keep()
    value = ras.pop()
    assert(value == 0x00000000)


# spec有一个元素的时候 S2 keep，S3 Pop -> spec pop

def test_ras_spec_pop_update_pop_2_spec_1_element(ras_object):  
    ras = ras_object
    ras.reset()
    ras.push(0x80000008)
    ras.pop_after_keep()
    value = ras.pop()
    assert(value == 0x0)


# #--------------------------------------------------------------------------------------------------------------------------------------------------#
# # S2 pop，S3 keep -> spec push 表现在地址空间上是spec不变
# # spec栈满 S2 pop，S3 keep -> spec push

def test_ras_update_push_1_spec_full(ras_object): # 测试spec push
    ras = ras_object
    ras.reset() 
    for i in range(32):
        ras.push(0x80000000+i*4)
    ras.keep_after_pop()  
    assert(ras.dut.RAS_RASStack_spec_queue_31_retAddr.value == 0x8000007c) 


# spec还剩一个空间  S2 pop，S3 keep -> spec push

def test_ras_update_push_1_spec_31_element(ras_object): # 测试spec push
    ras = ras_object
    ras.reset()
    for i in range(31):
        ras.push(0x80000000 + i*4)
    ras.keep_after_pop()

    value = ras.pop()
    assert(value == 0x80000000+30*4)


# spec full S2 pop，S3 keep -> spec push 再出栈

def test_ras_spec_pop_with_update_push_1_spec_full(ras_object): # 测试spec push
    ras = ras_object
    ras.reset()
    for i in range(32):
        ras.push(0x80000000 + i*4)
    ras.keep_after_pop()

    value = ras.pop()
    assert(value == 0x80000000+32*4)

# spec还剩一个空间  S2 pop，S3 keep -> spec push再出栈

def test_ras_spec_pop_with_update_push_1_spec_31_element(ras_object): # 测试spec push
    ras = ras_object
    ras.reset()
    for i in range(31):
        ras.push(0x80000000 + i*4)
    ras.keep_after_pop()
    value = ras.pop()
    assert(value == 0x80000000+30*4)


# spec为空的时候 S2 pop，S3 keep -> spec push

def test_ras_spec_pop_with_update_push_1_empty(ras_object):  
    ras = ras_object
    ras.reset()
    # set coverage
    ras.keep_after_pop()
    value = ras.pop()
    assert(value == 0x00000000)

# spec有一个元素的时候S2 pop，S3 keep -> spec push

def test_ras_spec_pop_with_update_push_spec_1_element(ras_object):  
    ras = ras_object
    ras.reset()
    # set coverage
    ras.push(0x80000008)
    ras.keep_after_pop()
    value = ras.pop()
    assert(value == 0x00000008)


# # #--------------------------------------------------------------------------------------------------------------------------------------------------#
# # # spec栈满  S2 keep，S3 Push -> spec push

def test_ras_update_push_spec_full(ras_object): # 测试spec push
    ras = ras_object
    ras.reset()
    for i in range(32):
        ras.push(0x80000000 + i*4)
    ras.push_after_keep(0x88888888)
    assert(ras.dut.RAS_RASStack_spec_queue_0_retAddr.value == 0x88888888)

# spec还剩一个空间  keep -> spec pop

def test_ras_update_push_2_spec_31_element(ras_object): # 测试spec push
    ras = ras_object
    ras.reset()
    for i in range(31):
        ras.push(0x80000000 + i*4)

    ras.push_after_keep(0x88888888)
    assert(ras.dut.RAS_RASStack_spec_queue_31_retAddr.value == 0x88888888)

# spec栈满  S2 keep，S3 Push -> spec push 再出栈

def test_ras_spec_pop_with_update_push_2_spec_full(ras_object): # 测试spec push
    ras = ras_object
    ras.reset()
    for i in range(32):
        ras.push(0x80000000 + i*4)
    ras.push_after_keep(0x88888888)

    value = ras.pop()
    assert(value == 0x88888888)


# spec还剩一个空间  keep -> spec pop 再出栈

def test_ras_spec_pop_with_update_push_2_spec_31_element(ras_object): # 测试spec push
    ras = ras_object
    ras.reset()
    for i in range(31):
        ras.push(0x80000000 + i*4)
    ras.push_after_keep(0x88888888)
    value = ras.pop()
    assert(value == 0x88888888)


# spec为空的时候  S2 keep，S3 Push -> spec push

def test_ras_spec_pop_with_update_push_2_empty(ras_object):  
    ras = ras_object
    ras.reset()
    # set coverage
    ras.push_after_keep(0x88888888)
    value = ras.pop()
    assert(value == 0x88888888)


# spec有一个元素的时候  S2 keep，S3 Push -> spec push

def test_ras_spec_pop_with_update_push_2_spec_1_element(ras_object):  
    ras = ras_object
    ras.reset()
    ras.push(0x80000008)
    ras.push_after_keep(0x88888888)
    value = ras.pop()
    assert(value == 0x88888888)


# # # --------------------------------------------------------------------------------------------------------------------------------------------------#
# # redirect压栈

def test_ras_redirect_push(ras_object):
    ras = ras_object
    ras.reset()
    meta = {}
    size = random.randint(1,31)
    for i in range(size):
        meta[i] = ras.push(0x80000000 + i*4)
    redirect_num = random.randint(1, size-1)
    atter_name  = f"RAS_RASStack_spec_queue_{(int(meta[redirect_num]['TOSW_value']))}_retAddr"
    spec_obj = getattr(ras.dut, atter_name)
    ras.redirect_push(0x88888888, 0, meta[redirect_num])
    assert(spec_obj.value == 0x88888888+4)


# redirect 溢出压栈

def test_ras_redirect_push_with_overflow(ras_object):
    ras = ras_object
    ras.reset()
    meta = {}
    size = 33
    for i in range(size):
        meta[i] = ras.push(0x80000000 + i*4)
    redirect_num = random.randint(0,size-1)
    atter_name  = f"RAS_RASStack_spec_queue_{int (int(meta[redirect_num]['TOSW_value']))}_retAddr"
    spec_obj = getattr(ras.dut, atter_name)
    ras.redirect_push(0x88888888, 1, meta[redirect_num])
    assert(spec_obj.value == 0x88888888+2)


# # redirect出栈

def test_ras_redirect_pop(ras_object):
    ras = ras_object
    ras.reset()
    meta = {}
    for i in range(31):
        meta[i] = ras.push(0x80000000 + i*4)
    redirect_num = random.randint(1,31)
    pop_value = ras.redirect_pop(meta[redirect_num])
    assert(pop_value == (0x80000000+(int(meta[redirect_num]['TOSR_value'])-2)*4))


# redirect出栈2号元素

def test_ras_full_redirect_pop_1st(ras_object):
    ras = ras_object
    ras.reset()
    meta = {}
    for i in range(32):
        meta[i] = ras.push(0x80000000 + i*4)
    # redirect_num = random.randint(0,9)
    redirect_num = 1
    pop_value = [-1]
    ras.redirect_pop(meta[redirect_num])
    pop_value = ras.pop()
    assert(pop_value == 0x80000000 + (int(meta[redirect_num]['TOSR_value'])-2)*4)


# # redirect出栈32号元素

def test_ras_full_redirect_pop_31st(ras_object):
    ras = ras_object
    ras.reset()
    meta = {}
    for i in range(32):
        meta[i] = ras.push(0x80000000 + i*4)
    # redirect_num = random.randint(0,9)
    redirect_num = 31
    pop_value = [-1]
    ras.redirect_pop(meta[redirect_num])
    pop_value = ras.pop()
    assert(pop_value == 0x80000000 + (int(meta[redirect_num]['TOSR_value'])-2)*4)


# if __name__ == "__main__":

#     ras = init_ras_pins()

#     start_time = time.time()
    
#     test_ras_push()

#     test_ras_spec_push_overflow()  # spec压栈溢出

#     test_ras_spec_pop()  # spec pop

#     test_ras_check_tosr_same_addr()    # 测试spec count

#     test_ras_commit_push() 

#     test_ras_spec_overflow_commit_push() 

#     test_ras_spec_push_same_addr_and_commit_and_check_commit_count_and_top_ptr() 

#     test_ras_commit_random() 

#     test_ras_commit_full_use()

#     test_ras_update_pop_1() # 测试spec push

#     test_ras_update_pop_1_spec_31_element() # 测试spec push

#     test_ras_update_pop_1_spec_full() # 测试spec push
    
#     test_ras_spec_pop_update_pop_1_spec_31_element() # 测试spec push

#     test_ras_spec_pop_update_pop_1_spec_empty()  

#     test_ras_spec_pop_update_pop_1_spec_1_element()  

#     test_ras_update_pop_2_spec_full() # 测试spec push

#     test_ras_update_pop_2_spec_31_element() # 测试spec push

#     test_ras_spec_pop_with_update_pop_2_spec_full() # 测试spec push

#     test_ras_spec_pop_update_pop_2_spec_31_element() # 测试spec push

#     test_ras_spec_pop_update_pop_2_empty()  

#     test_ras_spec_pop_update_pop_2_spec_1_element()  

#     test_ras_update_push_1_spec_full() # 测试spec push

#     test_ras_update_push_1_spec_31_element() # 测试spec push

#     test_ras_spec_pop_with_update_push_1_spec_full() # 测试spec push

#     test_ras_spec_pop_with_update_push_1_spec_31_element() # 测试spec push

#     test_ras_spec_pop_with_update_push_1_empty()  

#     test_ras_spec_pop_with_update_push_spec_1_element()  

#     test_ras_update_push_spec_full() # 测试spec push

#     test_ras_update_push_2_spec_31_element() # 测试spec push

#     test_ras_spec_pop_with_update_push_2_spec_full() # 测试spec push
#     test_ras_spec_pop_with_update_push_2_spec_31_element() # 测试spec push
#     test_ras_spec_pop_with_update_push_2_empty()  
#     test_ras_spec_pop_with_update_push_2_spec_1_element()  
#     test_ras_redirect_push()
#     test_ras_redirect_push_with_overflow()
#     test_ras_redirect_pop()
#     test_ras_full_redirect_pop_1st()
#     test_ras_full_redirect_pop_31st()

