#ifndef MyDelay_h_
#define MyDelay_h_

class MyDelay
{
  private:
    unsigned long t_prev;
    const unsigned long t_delay;
    void (*func)();
    
  public:
    MyDelay(const unsigned long t_delay, void (*func)());
    void run();
};

#endif