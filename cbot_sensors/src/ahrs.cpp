#include "cbot_sensors/ahrs.hpp"

AHRS::AHRS(const char *com_port_path_string, int BAUD_RATE) : SERIAL(com_port_path_string, BAUD_RATE)
{
    strcpy(com_port_path, com_port_path_string);
    BAUDRATE = BAUD_RATE;
}

cbot_ros_msgs::AHRS AHRS::checkAhrs(unsigned char *temp, int res) 
{
    int i;
    unsigned char chksum;
    cbot_ros_msgs::AHRS temp_ahrs_msg;
    if (*temp == SYNC)  {
        if (*(temp + 29) == checksumAhrs(temp, 28)) {
            temp_ahrs_msg = tokenizeAHRSData(temp);
        }
    }
    return temp_ahrs_msg;
}

unsigned char AHRS::checksumAhrs(unsigned char *buf, int res) 
{
    int i;
    unsigned char chsum = 0;
    for (i = 1; i < 29; i++) chsum += buf[i];
    chsum = chsum % 256;
    return chsum;
}

float AHRS::toFloat(unsigned char *buf)
{
    short s;
    s = ((*buf) * 256) + *(buf + 1);
    return ((float)s);
}


cbot_ros_msgs::AHRS AHRS::decode()
{
    cbot_ros_msgs::AHRS temp;
    unsigned char buf[128], chsum;
    int res, i;
    res = 0;
    for (i = 0; i < 30; i++) buf[i] = 0;
    res = read(fd, buf, 30);

    if (res == 30)  
        temp = checkAhrs(buf, res);
    else
        temp.AHRS_Status = AHRS_FAIL;
    
    buf[res] = 0;
    temp = tokenizeAHRSData(buf);
    return temp;
}


void AHRS::writeAhrs() {
    tcflush(fd, TCIFLUSH);
    write(fd, "G", 1);
}

void AHRS::initAhrs() {
    unsigned char *buf;
    int i;
    tcflush(fd, TCIFLUSH);
    tcflush(fd, TCOFLUSH);
    write(fd, "P", 1); 
    sleep(1);
    write(fd, "R", 1); 
    sleep(1);
    read(fd, buf, 5);
    write(fd, "a", 1); 
    sleep(1);
    read(fd, buf, 5);
    tcflush(fd, TCIFLUSH);
    tcflush(fd, TCOFLUSH);
    write(fd, "G", 1); 
    sleep(1);
}

cbot_ros_msgs::AHRS AHRS::tokenizeAHRSData(unsigned char *buf) 
{
    cbot_ros_msgs::AHRS temp;
    temp.Roll = toFloat(&buf[1]) * (0.0054931640625);
    temp.Pitch = toFloat(&buf[3]) * (0.0054931640625);
    temp.YawAngle = toFloat(&buf[5]) * (0.0054931640625);

    temp.RollRate = toFloat(&buf[7]) * 0.004577637;
    temp.PitchRate = toFloat(&buf[9]) * 0.004577637;
    temp.YawRate = toFloat(&buf[11]) * 0.004577637;

    temp.Xaccel = toFloat(&buf[13]) * 0.0000915527;
    temp.Yaccel = toFloat(&buf[15]) * 0.0000915527;
    temp.Zaccel = toFloat(&buf[17]) * 0.0000915527;

    temp.Temp = ((buf[25]) * 256 + buf[26]) * 0.054248 - 61.105;
    temp.AHRS_Status = AHRS_GOOD;

    return temp;
}
