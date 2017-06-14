
from winpty.cywinpty import Agent
import win32file


class PTY(Agent):
    def __init__(self, cols, rows):
        Agent.__init__(self, cols, rows, True)
        self.conin_pipe = win32file.CreateFileW(self.conin_pipe_name,
                                                win32file.GENERIC_WRITE,
                                                0, None,
                                                win32file.OPEN_EXISTING,
                                                0, None)
        self.conout_pipe = win32file.CreateFileW(self.conout_pipe_name,
                                                 win32file.GENERIC_READ,
                                                 0, None,
                                                 win32file.OPEN_EXISTING,
                                                 0, None)

    def read(self, length=1000):
        size = win32file.GetFileSize(self.conout_pipe)
        data = ''
        if size > 0:
            _, data = win32file.ReadFile(self.conout_pipe, length)
        return data

    def write(self, data):
        data = bytes(data, 'utf-8')
        _, num_bytes = win32file.WriteFile(self.conin_pipe, data)
        return num_bytes

    def close(self):
        win32file.CloseHandle(self.conout_pipe)
        win32file.CloseHandle(self.conin_pipe)