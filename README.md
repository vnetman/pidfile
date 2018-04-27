# pidfile

Python module for managing pid files

Programs create .pid files (typically /var/run/user/<uid>/<program-name>.pid)
to keep track of the PIDs of running instances of the program. One of the uses
is to allow long-running programs or daemons to be killed using a script that
reads the .pid file.

This module provides basic management for .pid files.

Example usage:
=============

Part 1 (main program):
---------------------

      from pidfile import PidFile

      def main():
          global pid
          pid = PidFile('my-name') # Use "/var/run/user/1000/my-name.pid"
          pid.add()                # Add this instance's PID

          global get_out
          get_out = False

          signal.signal(signal.SIGUSR1, my_usr1_handler) # listen to SIGUSR1

          while not get_out:       # main loop runs forever until SIGUSR1
              do_some_work()

          # We must have got SIGUSR1
          sys.exit(0)

      def my_usr1_handler():
          global get_out
          get_out = True

      @atexit.register
      def goodbye():
          pid.remove()             # Remove this instance's PID


 Part 2 (program that kills the *last* running instance of 'my-name'):
 --------------------------------------------------------------------

      from pidfile import PidFile

      def main():
          pid = PidFile('my-name')
          pid_of_last_instance = p.last()
          if not pid_of_last_instance:
              print('No running instances of \'my-name\'')
          else:
              print('Killing {} ...'.format(pid_of_last_instance))
              os.kill(pid_of_last_instance, signal.SIGUSR1) # send SIGUSR1

 Restrictions:
 ------------
 Linux only
