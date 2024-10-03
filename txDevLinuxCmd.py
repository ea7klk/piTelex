#!/usr/bin/python3
"""
Telex Device - Linux Command Line Interface
"""
__author__      = "Assistant"
__copyright__   = "Copyright 2023"
__license__     = "GPL3"
__version__     = "0.0.1"

import subprocess
import shlex
import logging
l = logging.getLogger("piTelex." + __name__)

import txBase
import txCode

class TelexLinuxCmd(txBase.TelexBase):
    def __init__(self, **params):
        super().__init__()
        self.id = 'LnxCmd'
        self.params = params
        self._rx_buffer = []

    def read(self) -> str:
        if self._rx_buffer:
            return self._rx_buffer.pop(0)
        return ''

    def write(self, a: str, source: str):
        if a == '\r':
            command = ''.join(self._rx_buffer)
            self._rx_buffer.clear()
            self._execute_command(command)
        elif a != '\n':
            self._rx_buffer.append(a)

    def _execute_command(self, command: str):
        try:
            args = shlex.split(command)
            result = subprocess.run(args, capture_output=True, text=True, timeout=30)
            output = result.stdout + result.stderr
            for char in output:
                self._rx_buffer.append(txCode.BaudotMurrayCode.ascii_to_tty_text(char))
            self._rx_buffer.append('\r\n')
        except subprocess.TimeoutExpired:
            error_msg = "Command execution timed out\r\n"
            self._rx_buffer.extend(list(error_msg))
        except Exception as e:
            error_msg = f"Error executing command: {str(e)}\r\n"
            self._rx_buffer.extend(list(error_msg))

    def idle(self):
        pass

    def idle20Hz(self):
        pass

    def idle2Hz(self):
        pass