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
  */1 * * * * /bin/bash /home/yourname/sleep.sh

And then you will run more than one process in backgroud at the same time::

  ps aux | grep '/home/yourname/sleep.sh'

Modify crontab with Process Count Supervisor::

  crontab -e
  */1 * * * * /bin/pcs /home/yourname/sleep.sh -m 1
