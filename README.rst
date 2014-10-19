Process Count Supervisor
========================

This is easy monitor tool to control your process count when your process runtime could more than your cronjob schedule.

Example
-------

Create a bash to sleep 200 seconds, it's meant run more than one minute::

  echo '#!/bin/bash' > /home/yourname/sleep.sh
  echo 'sleep 200' > /home/yourname/sleep.sh

Create crontab run every minute::

  crontab -e
  */1 * * * * /bin/bash /home/yourname/sleep.sh > /dev/null 2>&1

And then, you could find more than one process in backgroud at the same time::

  ps aux | grep '/home/yourname/sleep.sh'

Modify crontab with Process Count Supervisor::

  crontab -e
  */1 * * * * /home/yourname/pcs.py -m 1 /home/yourname/sleep.sh > /dev/null 2>&1

Finlly, you could find only one process in backgroud at the same time.
