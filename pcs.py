#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Author: Hans Liu
Backyard: hcliu
'''

import time
import os, sys, signal, shutil
from subprocess import call, Popen, PIPE
from subprocess import check_call, check_output, CalledProcessError

import argparse
from argparse import RawTextHelpFormatter # support describe

class ProcessCountSupervisor(object):
  '''docstring for ProcessCountSupervisor
  This is easy monitor tool to control your process count,
  when your process runtime could more than your cronjob schedule.
  '''
  def __init__(self, proc_cmd_list, proc_max=1):
    super(ProcessCountSupervisor, self).__init__()
    self.ts = str(time.time())
    self.__process_command = " ".join(proc_cmd_list)
    self.__process_path = proc_cmd_list[0]
    self.__process_cur_count = 0
    self.__process_max_count = proc_max

  def run(self):
    if not self.check_process_path():
      return False
    if not self.check_process_count():
      return False
    # call process by limit
    while self.__process_cur_count < self.__process_max_count:
      self.call_process()
    # kill process by limit
    # because we cannot kill sub process, disable now
    #while self.__process_cur_count > self.__process_max_count:
    #  self.kill_process()
    return True

  def check_process_path(self):
    '''
    >>> cmd_list = '/home'.split()
    >>> p = ProcessCountSupervisor(cmd_list)
    >>> print p.check_process_path()
    False
    >>> cmd_list = '/bin/bash'.split()
    >>> p = ProcessCountSupervisor(cmd_list)
    >>> print p.check_process_path()
    True
    '''
    if os.path.isfile(self.__process_path):
      return True
    return False

  def check_process_count(self):
    '''
    >>> cmd_list = '/bin/bash'.split()
    >>> p = ProcessCountSupervisor(cmd_list)
    >>> print p.check_process_count()
    True
    '''
    cmd = """ps aux | grep '{0}' | grep -v pcs | grep -v grep | grep -v sudo | wc -l""".format(self.get_process_pattern())
    try:
      stdout = check_output(cmd, shell=True)
      self.__process_cur_count = int(stdout)
    except CalledProcessError as e:
      #e.returncode
      return False
    except Exception as e:
      return False
    return True

  def call_process(self):
    '''
    >>> cmd_list = '/bin/echo hello > /dev/null 2>&1'.split()
    >>> p = ProcessCountSupervisor(cmd_list, 1)
    >>> print p.get_process_count()
    0
    >>> print p.call_process()
    True
    >>> print p.get_process_count()
    1
    '''
    cmd = "{0} &".format(self.__process_command)
    try:
      #p = Popen(cmd, stdout=PIPE, shell=True)
      check_call(cmd, shell=True)
    except CalledProcessError as e:
      #e.returncode
      return False
    except Exception as e:
      return False
    self.__process_cur_count += 1
    return True

  def kill_process(self):
    '''
    >>> from subprocess import call
    >>> cmd = '/bin/sleep 21 > /dev/null 2>&1'
    >>> cmd_list = cmd.split()
    >>> out = call("{0} &".format(cmd), shell=True)
    >>> p = ProcessCountSupervisor(cmd_list, 0)
    >>> print p.get_process_count()
    0
    >>> print p.kill_process()
    True
    >>> print p.get_process_count()
    -1
    '''
    cmd = """ps aux | grep '{0}' | grep -v pcs | grep -v grep | grep -v sudo |  sort -nk 2 | head -1""".format(self.get_process_pattern())
    try:
      stdout = check_output(cmd, shell=True)
      pid = int(stdout.split()[1])
      os.kill(pid, signal.SIGKILL)
    except CalledProcessError as e:
      #e.returncode
      return False
    except Exception as e:
      print e
      return False
    self.__process_cur_count -= 1
    return True

  def get_process_pattern(self):
    if '>' in self.__process_command:
      pattern = self.__process_command[0:self.__process_command.index('>')].strip()
    else:
      pattern = self.__process_command.strip()
    return pattern

  def get_process_count(self):
    return self.__process_cur_count

def parse_options():
  '''
  Handle command-line options with argparse.
  Return list of arguments, largely for use in `_argument`.
  '''
  #
  # Initialize
  parser = argparse.ArgumentParser(prog='pcs', usage=("pcs [options] <command>"), add_help=True)
  parser.add_argument('proc_cmd_list',
    nargs='*',
    metavar='command',
    help="please input process absolute path with variable to run."
  )
  parser.add_argument('-m', '--max',
    metavar='N',
    dest='proc_max',
    type=int,
    default=1,
    help="the limit process could run by cronjob. (default:1)"
  )
  parser.add_argument('-l', '--list',
    action='store_true',
    dest='proc_list',
    default=False,
    help="show process list."
  )
  parser.add_argument('-t', '--test',
    action='store_true',
    dest='pcs_test',
    default=False,
    help="run doctest."
  )
  args = parser.parse_args()
  return parser, args

def main():
  parser, args = parse_options()
  try:
    if args.pcs_test:
      import doctest
      doctest.testmod()
    if args.proc_list:
      pcs_obj = ProcessCountSupervisor(args.proc_cmd_list)
      print('Command: {0}, Run in backgroud: {1}'," ".args.proc_cmd_list, pcs_obj.get_process_count())
    if len(args.proc_cmd_list) > 0:
      pcs_obj = ProcessCountSupervisor(args.proc_cmd_list, args.proc_max)
      pcs_obj.run()
    else:
      parser.print_help()
  except AttributeError as e:
    if "'str' object has no attribute 'args'" == e.message:
      parser.print_usage()
      print("pcs: error: missing command to show")
  except Exception as e:
    raise e
  pass

if __name__ == "__main__":
  main()
