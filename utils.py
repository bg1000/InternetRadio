import psutil
import signal
import os
import datetime

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

