#ifndef _GPS_H_
#define _GPS_H_

#include "ros/ros.h"
#include "cbot_common/serial.hpp"
#include "cbot_ros_msgs/GPS.h"

#define GPS_FAIL  0
#define GPS_FIX_NO  1
#define GPS_FIX_YES 2

int lat_deg, lon_deg;
int day, month, year, hour, min, sec;
float lon_min, lat_min, vel, course;
int num_of_sat, data_quality, lat_dir,lon_dir;
float latitude, longitude;


enum GPRMC_fields
{ 
    UtCTIME = 2, StAT = 3, LaT = 4, DiRN_LaT = 5, LoN = 6, DiRN_LoN = 7, SpD = 8, TrACK = 9, UtCDATE = 10, MaGVAR = 11, DiRN_MaG = 12
};

enum GPGGA_fields
{ 
    UtCTIME2 = 2, LaT2 = 3, DiRN_LaT2 = 4, LoN2 = 5, DiRN_LoN2 = 6, FixQual = 7, NoSat = 8, HDOP = 9, Alt=10, HOD=11, TLast = 12, DGPS = 13
};

class GPS: public SERIAL 
{
    public:
        GPS(const char *com_port_path_string, int BAUD_RATE);
        cbot_ros_msgs::GPS decode();
        int gprmc_valid;

    private:
        unsigned char getHex(char* value);
        int checksum(char* buf, int res, char*(chsum)); 
};

#endif