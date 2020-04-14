import datetime
import os
import psutil
import signal
import site
import sys


class findProcByName:
     pidList = []
     def __init__(self, processName):
          for proc in psutil.process_iter():
               try:
	          #Check if process name contains the passed in string - make the search case insensitive
                  if processName.lower() in proc.name().lower() and proc not in self.pidList:
                       self.pidList.append(proc)
               except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                  pass
          self.count=len(self.pidList)
          self.processName=processName
     def killAll(self):
          # print "running killAll"
          for p in self.pidList:
               print(str(datetime.datetime.now()) + " - killing " + str(p.pid))
               p.terminate()
               try:
                   p.wait(2)
               except (psutil.TimeoutExpired):
                   print(str(datetime.datetime.now()) + " - Time out waiting for process to terminate. Attempting to kill")
                   p.kill()
     def leaveOne(self):
          for i in range (0, self.count-1):
              self.pidList[i].terminate()
              try:
                  self.pidList[i].wait(2)
              except (psutil.TimeoutExpired): 
                   print(str(datetime.datetime.now()) + "- Time out waiting for process to terminate. Attempting to kill.")
                   self.pidList[i].kill()
     def refresh(self):
         del self.pidList[:] 
         self.__init__(self.processName)

def is_running(script):
    for q in psutil.process_iter():
        if q.name().startswith('python'):
            if len(q.cmdline())>1 and script in q.cmdline()[1] and q.pid !=os.getpid():
               # print("'{}' Process is already running".format(script))
                return True

    return False
def uptime():
    with open('/proc/uptime', 'r') as f:
         uptime_seconds = float(f.readline().split()[0])
         return uptime_seconds
class GracefulKiller:
  kill_now = False
  def __init__(self):
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully)

  def exit_gracefully(self,signum, frame):
    self.kill_now = True
#
# This is a workaround for python 2 packages that would otherwise
# run under python 3 except imports don't work 
# properly because they are releative rather than absolute.
# This function searches for the installation directory of the package.
# If it finds it it, it adds it to sys.path allowing the imports to work.
#
def add_package_path(package_name):
    path_list = []
    path_list = site.getsitepackages()
    print(path_list)
    user_path_list = site.getusersitepackages()
    print (user_path_list)
    path_list.append(user_path_list)
    print(path_list)
    for path in path_list:
        try:
            dir_list = os.listdir(path)
            if package_name in dir_list:
                sys.path.insert(0,path + "/" + package_name)
                return True
        except FileNotFoundError:
            # python sometimes reports a directory that doesn't exist so?
            pass
    return False
