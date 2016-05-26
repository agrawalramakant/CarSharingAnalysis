# -*- coding: utf-8 -*-
"""
Created on Thu May 05 13:20:54 2016

@author: avinashchandra
"""

"""
Demonstrates how to use the gevent compatible scheduler to schedule a job that executes on 3 second
intervals.
"""

from datetime import datetime
import os

from apscheduler.schedulers.gevent import GeventScheduler


def tick():
    print('Tick! The time is: %s' % datetime.now())
def callMe():
    print "function called"


if __name__ == '__main__':
    scheduler = GeventScheduler()
    scheduler.add_job(callMe, 'interval', seconds=1)
    g = scheduler.start()  # g is the greenlet that runs the scheduler loop
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        g.join()
    except (KeyboardInterrupt, SystemExit):
        pass