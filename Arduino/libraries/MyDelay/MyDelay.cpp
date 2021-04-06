#include "Arduino.h"
#include "MyDelay.h"

MyDelay::MyDelay(const unsigned long t_delay, void (*func)())
  : t_prev(0), t_delay(t_delay), func(func){}
  
void MyDelay::run()
{
   unsigned long t_now = millis();
     if(t_now - t_prev >= t_delay){
        t_prev = t_now;

        func();
      }
}