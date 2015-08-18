#include "SerialProtocol.h"

namespace Streams {

unsigned char SerialProtocol::STARTBYTE = 0x7E;
unsigned char SerialProtocol::STOPBYTE = 0x7F;
unsigned char SerialProtocol::ESCAPEBYTE = 0x7D;
unsigned char SerialProtocol::SPEEDCOMMAND_ID = 1;
unsigned char SerialProtocol::PIDCOMMAND_ID = 2;

SerialProtocol::SerialProtocol(){
}

std::string SerialProtocol::createSpeedCommand(const float x,
                                const float y,
                                const float theta,
                                const unsigned char id){
    std::string buffer;
    buffer += this->STARTBYTE;
    buffer += id;
    buffer += this->SPEEDCOMMAND_ID;
    this->insertFloatInPacket(x, buffer);
    this->insertFloatInPacket(y, buffer);
    this->insertFloatInPacket(theta, buffer);
    buffer += STOPBYTE;

    return buffer;
}

std::string SerialProtocol::createSetPidCommand(const float p,
                                         const float i,
                                         const float d,
                                         const unsigned char id){
    std::string buffer;
    buffer += this->STARTBYTE;
    buffer += id;
    buffer += this->PIDCOMMAND_ID;
    this->insertFloatInPacket(p, buffer);
    this->insertFloatInPacket(i, buffer);
    this->insertFloatInPacket(d, buffer);
    buffer += this->STOPBYTE;

    return buffer;
}

void SerialProtocol::insertFloatInPacket(float data, std::string &buffer){
    dataConverter.floatValue = data;
    for(int i = 0; i < 4; ++i){
        if(this->isEscapedByte(dataConverter.charValues[i])){
            buffer += this->ESCAPEBYTE;
        }
        buffer += dataConverter.charValues[i];
    }
}

void SerialProtocol::insertIntInPacket(int data, std::string &buffer){
    dataConverter.intValue = data;
    for(int i = 0; i < 4; ++i){
        if(this->isEscapedByte(dataConverter.charValues[i])){
            buffer += this->ESCAPEBYTE;
        }
        buffer += dataConverter.charValues[i];
    }
}

bool SerialProtocol::isEscapedByte(char byte){
    return byte == this->STARTBYTE || byte == this->ESCAPEBYTE || byte == this->STOPBYTE;
}

} //Streams namespace
