import os
import psutil


from jarvis.core import response


def get_memory_consumption():
    pid = os.getpid()
    py = psutil.Process(pid)
    memory_use = py.memory_info()[0] / 2. ** 30  # memory use in GB...I think
    return memory_use


def tell_memory_consumption(**kwargs):
    """
    Responds the memory consumption of the assistant process
    """
    memory = get_memory_consumption()
    response.assistant_response('I use {0:.2f} GB..'.format(memory))
