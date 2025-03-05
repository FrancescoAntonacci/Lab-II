// Definitions
const unsigned int analogPin=0; // define port A0 for analog input
const unsigned int sincPin = 5;  // define pin5 for sync input
const unsigned int refPin = 7; // define pin7 for digital output
const unsigned int ledPin = 13; // define LED_BUILTIN for built-in LED 
int i; // define variable i
int ii=0; // define variable ii
int delays; // define delays (will contain the delay in microseconds between one and the subsequent sampling)
int delays1; // define additional variable used to build delays
int delays2; 
int delays3;
int espo; // define variable espo used to determine the number of points
int syncflag; // define the syncflag variable (1 for synced acquisition)
int sampl; // define the sampl variable 
int npnts; // define the npnts variable (it will contain the number of points)
int V[4096]; // define the array V (it will contain data in digit)
int t[4096]; // define the array t (it will contain time in microseconds)
int tave[2048]; // define the array t (it will contain time in microseconds)
int Vave[2048]; // define the array V (it will contain data in digit)
int Vaveprev[2048]; // define the array V (it will contain data in digit)
int taveprev[2048]; // define the array t (it will contain time in microseconds)
int VM2[2048]; // define the array stdev of V (it will contain data in digit)
int tM2[2048]; // define the array stdev of t (it will contain time in microseconds)
int hiresflag; // define the hiresflag variable (1 for 12 bit data)
int StartTime; // define the variable StartTime
int start=0; // define the variable start (it will be one when the acqusition starts)
int sinc; // define the sinc variable needed to operate synchronously
int aveflag; // define the aveflag (base 10 exp of the number of averaged sweeps)
int ave; // define the ave variable containing the number of averaged sweeps
int iave; // counter for the average
int prec=100; // set the precision of the analysed data
int strlength = 7; // define the number of characters to be read
char char_array[7]; // define the character array that will contain the encoded data from the serial connection


// Initialization loop
void setup()
  {
   Serial.begin(119200); // serial port initialization at 19200 baud
   Serial.flush(); // clean the buffer 
   pinMode(sincPin, INPUT);  // set the sincPin as an input
   pinMode(ledPin,OUTPUT); // set the ledPin as an output
   digitalWrite(refPin, HIGH); // set to high the refPin
   digitalWrite(ledPin, LOW); // set the ledPin to low
  }

// Program loop
void loop()
  {
   char tmp;
    if (Serial.available() >0) // check for data in the serial buffer
      {
       for (ii=0;ii<strlength;ii++) // loop for serial data reading
     {
       char_array[ii]=Serial.read();
     }
       // attribute values to data coming from the serial communication according to a specific encoding
        delays1 = (char_array[0]-'0'); // this enables converting characters into integers 
        delays2 = (char_array[1]-'0'); 
        delays3 = (char_array[2]-'0'); 
        espo=(char_array[3]-'0');
        syncflag = (char_array[4] -'0'); // this is for the syncflag
        hiresflag = (char_array[5] -'0'); // this is for the hiresflag
        aveflag = (char_array[6] -'0'); // set the number of sweeps to average over
        Serial.flush(); // clean the serial buffer
  if (hiresflag==0) analogReadResolution(10); // set the data resolution to 10 bit (1024)
  if (hiresflag==1) analogReadResolution(12); // set the data resolution to 12 bit (4096)
  start=1; // set the start flag to one
  iave=1; // set the counter for the average
  delays=(delays3*100+delays2*10+delays1)*10; // set the delay between subsequent sampling in microseconds
  if (espo==0) npnts=128; // set the number of points of the data acqusition
  if (espo==1) npnts=256;
  if (espo==2) npnts=512;
  if (espo==3) npnts=1024;
  if (espo==4) npnts=2048;
  if (espo==5) npnts=4096;
  if (espo==6) npnts=8192;

  if (aveflag==0) ave=1;
  if (aveflag==2) ave=4;
  if (aveflag==3) ave=8;
  if (aveflag==4) ave=16;
  if (aveflag==5) ave=32;
  if (aveflag==6) ave=64;
      }      
 
  if(!start) return // if start flag is 0 does not execute the remaining instructions
    delay(2000); // wait 2000 ms to prevent casini
  if (npnts != 8192)
  {  
      while (iave < ave+1)
      {
          sinc = digitalRead(sincPin);// read the sincPin
          digitalWrite(ledPin, HIGH); // set to high the ledPIN
          if (syncflag == 1) // instructions to be carried out in case of synced acquisition (rising edge)
          {
          while (sinc==HIGH) // wait for syncPin to go low
          {sinc = digitalRead(sincPin);} // read sincPin
          while (sinc==LOW) // wait for syncPin to go high
          {sinc = digitalRead(sincPin);} // read sincPin 
          } 
          if (syncflag == 2) // instructions to be carried out in case of synced acquisition (falling edge)
          {
          while (sinc==LOW) // wait for syncPin to go low
          {sinc = digitalRead(sincPin);} // read sincPin
          while (sinc==HIGH) // wait for syncPin to go high
          {sinc = digitalRead(sincPin);} // read sincPin 
          }   
          StartTime=micros(); // set the starting time to zero
          for(i=0;i<npnts;i++) // measurement loop
          {
              t[i]=micros()-StartTime; // read time and put it into the array t
              V[i]=analogRead(analogPin); // read analogPin and put it into the array V
              delayMicroseconds(delays); // wait for the nominal sampling interval
          }
          if (ave!=1)
          {
            for(i=0;i<npnts;i++) // analysis loop
            {
              tave[i]+=t[i]*prec; // summed t[i]*prec
              Vave[i]+=V[i]*prec; // summed V[i]*prec        
            }        
             for(i=0;i<npnts;i++) // update VM2 and tM2
            {
              if (iave==1)
              {
                tM2[i]+=(t[i]*prec-tave[i]/iave)*(t[i]*prec-tave[i]/iave); // tM2
                VM2[i]+=(V[i]*prec-Vave[i]/iave)*(V[i]*prec-Vave[i]/iave); // VM2
              }
              else
              {
                tM2[i]+=(t[i]*prec-taveprev[i]/(iave-1))*(t[i]*prec-tave[i]/iave); // tM2
                VM2[i]+=(V[i]*prec-Vaveprev[i]/(iave-1))*(V[i]*prec-Vave[i]/iave); // VM2 
              }       
            }
          
            for(i=0;i<npnts;i++) // create previous average arrays
            {
              taveprev[i]=tave[i]; // previous summed t[i]*prec
              Vaveprev[i]=Vave[i]; // previous summed V[i]*prec        
            }
  
          }
            iave+=1; // increase iave by one
            digitalWrite(ledPin, LOW); // set to low the ledPIN
            delay(100); // add a short deadtime between subsequent sweeps
      }
      if(ave==1)
      {
      for(i=0;i<npnts;i++) // loop for data sending on serial communication (two column data)
        {
          Serial.print(t[i]); // write t[i]
          Serial.print(" "); // put a blank
          Serial.println(V[i]); // write V[i] and return
        }
      }
      
      if(ave!=1)
      {
      for(i=0;i<npnts;i++) // loop for data sending on serial communication (four column data)
        {
          Serial.print(tave[i]/ave); // write tave[i]
          Serial.print(" "); // put a blank
          Serial.print(tM2[i]/ave); // write tM2[i]
          Serial.print(" "); // put a blank
          Serial.print(Vave[i]/ave); // write Vave[i]
          Serial.print(" "); // put a blank
          Serial.println(VM2[i]/ave); // write VM2[i]
        }
      }
      
      
      start=0; // disable the flag
      Serial.flush(); // clean the serial buffer
  }
  else
        {
          sinc = digitalRead(sincPin);// read the sincPin
          digitalWrite(ledPin, HIGH); // set to high the ledPIN
          if (syncflag == 1) // instructions to be carried out in case of synced acquisition (rising edge)
          {
          while (sinc==HIGH) // wait for syncPin to go low
          {sinc = digitalRead(sincPin);} // read sincPin
          while (sinc==LOW) // wait for syncPin to go high
          {sinc = digitalRead(sincPin);} // read sincPin 
          } 
          if (syncflag == 2) // instructions to be carried out in case of synced acquisition (falling edge)
          {
          while (sinc==LOW) // wait for syncPin to go low
          {sinc = digitalRead(sincPin);} // read sincPin
          while (sinc==HIGH) // wait for syncPin to go high
          {sinc = digitalRead(sincPin);} // read sincPin 
          }   
          StartTime=micros(); // set the starting time to zero
          for(i=0;i<4096;i++) // measurement loop to fill t[i] and V[i]
          {
              t[i]=micros()-StartTime; // read time and put it into the array t
              V[i]=analogRead(analogPin); // read analogPin and put it into the array V
              delayMicroseconds(delays); // wait for the nominal sampling interval
          }
          for(i=0;i<2048;i++) // measurement loop to fill tave[i] and Vave[i]
          {
              tave[i]=micros()-StartTime; // read time and put it into the array t
              Vave[i]=analogRead(analogPin); // read analogPin and put it into the array V
              delayMicroseconds(delays); // wait for the nominal sampling interval
          }
          for(i=0;i<2048;i++) // measurement loop to fill taveprev[i] and Vaveprev[i]
          {
              taveprev[i]=micros()-StartTime; // read time and put it into the array t
              Vaveprev[i]=analogRead(analogPin); // read analogPin and put it into the array V
              delayMicroseconds(delays); // wait for the nominal sampling interval
          }
          digitalWrite(ledPin, LOW); // set to high the ledPIN
          for(i=0;i<4096;i++) // loop for data sending on serial communication (two column data)
        {
          Serial.print(t[i]); // write t[i]
          Serial.print(" "); // put a blank
          Serial.println(V[i]); // write V[i] and return
        }
        for(i=0;i<2048;i++) // loop for data sending on serial communication (two column data)
        {
          Serial.print(tave[i]); // write t[i]
          Serial.print(" "); // put a blank
          Serial.println(Vave[i]); // write V[i] and return
        }
        for(i=0;i<2048;i++) // loop for data sending on serial communication (two column data)
        {
          Serial.print(taveprev[i]); // write t[i]
          Serial.print(" "); // put a blank
          Serial.println(Vaveprev[i]); // write V[i] and return
        }
      start=0; // disable the flag
      Serial.flush(); // clean the serial buffer  
  }
  }
  
