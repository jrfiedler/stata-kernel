import os
import re
import time
import tempfile

import win32com.client
from IPython.kernel.zmq.kernelbase import Kernel
from IPython.core.magic import register_line_cell_magic


class StataKernel(Kernel):
    implementation = 'StataKernel'
    implementation_version = '0.0.1'
    language = 'Stata Ado and Mata'
    language_version = 'any'
    banner = ''
    language_info = {
        'name': 'stata',
        'mimetype': 'text/x-stata',
        'file_extension': 'do',
    }
    
    log_address = os.path.join(tempfile.gettempdir(), 'stata_kernel_log.txt')
    
    def __init__(self, *args, **kwargs):
        super(StataKernel, self).__init__(*args, **kwargs)
        self.stata = win32com.client.Dispatch("stata.StataOLEApp")
        self.stata_do = self.stata.DoCommandAsync
        self.stata_do('log using {} , text replace'.format(self.log_address))
        self.stata_do('set more off')
        time.sleep(0.5)
        self.log_file = open(self.log_address)
        self.continuation = False
        
        print 'init complete'
        
    def remove_continuations(self, code):
        return re.sub(r'\s*\\\\\\\s*\n', ' ', code)
        
    def get_log_line(self, ntries=10):
        UtilIsStataFree = self.stata.UtilIsStataFree
        log_file = self.log_file
        log_line = log_file.readline()
        try_num = 1
        while not log_line and not UtilIsStataFree():
            time.sleep(0.05)
            log_line = log_file.readline()
            try_num += 1
        return log_line
            
    def ignore_output(self):
        get_log_line = self.get_log_line
        while get_log_line():
            pass
            
    def respond(self):
        lines = []
        UtilIsStataFree = self.stata.UtilIsStataFree
        log_file = self.log_file
        log_line = log_file.readline()
        while not log_line:
            time.sleep(0.05)
            log_line = log_file.readline()
        while log_line or not UtilIsStataFree():
            if log_line:
                stream_content = {'name': 'stdout', 'text': log_line}
                self.send_response(self.iopub_socket, 'stream', stream_content)
            else:
                time.sleep(0.05)
            log_line = log_file.readline()
    
    def do_execute(
        self,
        code,
        silent,
        store_history=True,
        user_expressions=None,
        allow_stdin=False
    ):
        self.continuation = False
        self.ignore_output()
        code = self.remove_continuations(code.strip())
        mata_magic = re.match(r'\s*%%mata\s+', code)
        if mata_magic:
            code = 'mata\n' + code[mata_magic.end():] + '\nend\n'
        try:
            self.stata_do('    ' + code + '\n')
            self.respond()
        except KeyboardInterrupt:
            self.stata.UtilSetStataBreak()
            self.respond()
            return {'status': 'abort', 'execution_count': self.execution_count}
            
        msg = {
            'status': 'ok',
            'execution_count': self.execution_count,
            'payload': [],
            'user_expressions': {}
        }
        return msg
        
    def do_shutdown(self, restart):
        self.stata_do('    exit, clear\n')
                
        
if __name__ == '__main__':
    from IPython.kernel.zmq.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=StataKernel)
