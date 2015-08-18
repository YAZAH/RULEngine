# distutils: language = c++
# distutils: sources = SerialProtocol.cpp

from libcpp.string cimport string
cdef extern from "SerialProtocol.h" namespace "Streams":
    cdef cppclass SerialProtocol:
        SerialProtocol() except +
        string createSpeedCommand(const float,const float,const float,const unsigned char)
        string createSetPidCommand(const float, const float, const float, const unsigned char)

        unsigned char STARTBYTE
        unsigned char STOPBYTE
        unsigned char ESCAPEBYTE
        unsigned char SPEEDCOMMAND_ID
        unsigned char PIDCOMMAND_ID

cdef class serial_protocol:
    cdef SerialProtocol *thisptr
    def __cinit__(self):
        self.thisptr = new SerialProtocol()
    def __dealloc__(self):
        del self.thisptr
    def createSpeedCommand(self, const float x, const float y, const float theta, const unsigned char id):
        return self.thisptr.createSpeedCommand(x, y, theta, id)
