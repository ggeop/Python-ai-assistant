import os
import psutil


from jarvis.utils.response_utils import assistant_response


def tell_memory_consumption(**kwargs):
    """
    Responds the memory consumption of the assistant process
    """
    pid = os.getpid()
    py = psutil.Process(pid)
    memoryUse = py.memory_info()[0] / 2. ** 30  # memory use in GB...I think
    assistant_response('I use {} GB..'.format(memoryUse))
