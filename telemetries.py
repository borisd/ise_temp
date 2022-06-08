from multiprocessing import Process
import sys
from encoder_telemetries import encoder_scheduler
from decoder_telemetries import decoder_scheduler


# This starts two processes for running the encoder and decoder schedulers.

if __name__ == '__main__':
    try:
        p1=Process(target=encoder_scheduler)
        p1.start()
        p2=Process(target=decoder_scheduler)
        p2.start()

        p1.join()
        p2.join()

    except:
        sys.exit()










