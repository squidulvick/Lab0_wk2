"""!
@file step_response.py
This file produces a step response on the nucleo micro processor through the pin C0
and collects data from the pin B0 about the voltage of an RC circuit.  That data is
then printed in the console.
"""
import utime
import micropython
import cqueue

# defining pins
pinC0 = pyb.Pin(pyb.Pin.board.PC0, pyb.Pin.OUT_PP) # create output pin object
pinB0 = pyb.Pin(pyb.Pin.board.PB0, pyb.Pin.IN) # create input pin object
adc = pyb.ADC(pinB0)

# timer variable
COL_TIME = 1  # how long to collect data for, in seconds
FREQ = 100   # how often the program should collect data, in HZ

# creating queues for the voltage and time
v_queue = cqueue.IntQueue(COL_TIME*FREQ) # voltage queue for storing voltage data
t_queue = cqueue.IntQueue(COL_TIME*FREQ) # time queue for storing time data

# interupt callback fucntion
def timer_int(tim_num):
    """!
    Interrupt callback function to store the current ADC value in the queue
    """
         # Code goes here
    v_queue.put(adc.read()) # puts an integer into queue, which is read using adc (analog digital converter)      

def step_response (t_channel,frequency,collection_time):
    """!
    This function initiates a step output voltage in pin C0 and enables timer
    interrupts to allow for the accurate collection of RC voltage data through
    pin B0.  The function then generates a queue of time data based on the times
    the voltage data was collected and prints the time and voltage data to the
    console.
    @param   t_channel The timer channel to use for interrupts
    @param   frequency How often the program should collect data in Hz
    @param   collection_time How long the program should collect data for
    """
    # set up interrupt
    timmy = pyb.Timer(t_channel, freq = frequency) # create the timer object 
    timmy.callback(timer_int) # where to go when intuerupt occurs
    
    # turn on the pin
    pinC0.high()
    
    # We want to run this program until the keyboard interrupts the program so
    # that we can stop the program if necessary
    try:
        # interrupts are enabled, we want to wait here until the voltage queue is full
        while not v_queue.full():
            pass
        
        # queue is full, so disable interrupts
        timmy.callback(None)
        
        # create time data by using for loop to fill a queue
        for i in range(frequency*collection_time):
            t_queue.put(int(1/frequency*1000*i)) # the time in ms is going to be the current index times 1/frequency (Hz) times 1000ms/1s
        
        # print data while there is still data in the voltage queue
        while v_queue.any():
            # adc reads in an integer from 0->4095 to correspond with voltage from 0->3.3V so divide by 4096 and multiply by 3.3 to get voltage in Volts
            voltage = v_queue.get()/4096*3.3
            time = t_queue.get()
            print(f"{time}, {voltage}")
            
        # raise a keyboard interrupt to initiate turn off of program
        raise KeyboardInterrupt
    
    except KeyboardInterrupt:  # keyboard interrupt to exit program (ctrl+c)
            pinC0.low() # turn off C0 pin
            print("program ended")
            pass
        
        
# Run this program as main script
if __name__ == "__main__":
      step_response(1, FREQ, COL_TIME)