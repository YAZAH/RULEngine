/*
Robocup Serial Protocol V1.1
*/
#ifndef SERIALPROTOCOL_H
#define SERIALPROTOCOL_H
#include <string>
#include <iostream>

using namespace std;

namespace Streams{

typedef union DataConverter {
    float floatValue;
    int intValue;
    unsigned char charValues[4];
}DataConverter;

class SerialProtocol{
public:
    SerialProtocol();
    std::string createSpeedCommand(const float x,const float y,const float theta,const unsigned char id);
    std::string createSetPidCommand(const float p, const float i, const float d, const unsigned char id);

    static unsigned char STARTBYTE;
    static unsigned char STOPBYTE;
    static unsigned char ESCAPEBYTE;
    static unsigned char SPEEDCOMMAND_ID;
    static unsigned char PIDCOMMAND_ID;

private:
    void insertFloatInPacket(float data, std::string &buffer);
    void insertIntInPacket(int data, std::string &buffer);
    bool isEscapedByte(char byte);

    DataConverter dataConverter;
};

} //Streams namespace

#endif
