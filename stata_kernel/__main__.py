from IPython.kernel.zmq.kernelapp import IPKernelApp
from .stata_kernel import StataKernel
IPKernelApp.launch_instance(kernel_class=StataKernel)