"""
HARRISON_V0.1.py
Main program to run and monitor home automation programs.

Currently working on getting it to boot up log info correctly. 7/24/26

Todo:
Status
Stop
Kill-all
Dump logs

To Test:
Run
Start
"""
import sys
from datetime import date
import subprocess


def welcome(last_login):
    print('#######################################################################')
    print('#                                                                     #')
    print('#                                                                     #')
    print('#                                                                     #')
    print('#                             Welcome to                              #')
    print('#                                                                     #')
    print('#                                                                     #')
    print('#                                                                     #')
    print('#                    H . A . R . R . I . S . O . N                    #')
    print('#                    o   u   o   e   n   i   n   e                    #')
    print('#                    m   t   b   p   s   l   -   v                    #') 
    print('#                    e   o   o   e   t   e   a   e                    #')
    print('#                        m   t   a   r   n   n   r                    #')
    print('#                        a       t   u   t   d   -                    #')
    print('#                        t       i   c   l   -   c                    #')
    print('#                        i       n   t   y   o   e                    #')
    print('#                        o       g   i       n   a                    #')
    print('#                        n           o           s                    #')
    print('#                                    n           i                    #')
    print('#                                    s           n                    #')
    print('#                                                g                    #')
    print('#                                                                     #')
    print('#                                                                     #')
    print('#                                                                     #')     
    print('#                      Type "start" or "help"                         #')
    print('#                                                                     #')
    print('#                      Last login: ', last_login, '                   #')
    print('#                                                                     #')
    print('#                                                                     #')
    print('#                                                                     #')
    print('#######################################################################')


def config_file_read(config_file_name, config_file_location):
    # reads config file and returns last login date.
    # works 7/24/26

    last_login = ''

    with open(config_file_location + config_file_name) as config_file:
        config_contents = config_file.readlines()

    for line in config_contents:
        last_login = line.rstrip('\n')

    if last_login == '':
        last_login = 'None          '
    else:
        last_login = str(last_login) + '    '

    return last_login
    
    
def config_file_write(config_file_name, config_file_location):
    # writes login date on exit of program
    # works as of 7/24/26

    config_file = open(config_file_location + config_file_name, 'w')
    x = date.today()
    config_file.write(str(x))
    config_file.close()
    
    
def help():
    # prints list of commands
    # works as of 7/24/26

    print('This is the launch pad for the various home automation programs.')
    print('For now please enter all commands without spaces and lower case.')
    print('\n')
    print('welcome --> returns the welcome splash page.')
    print('help --> returns this menu.')
    print('status --> returns a detailed status page.')
    print('start --> runs the default starting sequence.')
    print('run "program name" --> run, one space, and the program name '
          'without quotes runs that program.')    
    print('stop "program name" --> stop, one space, and the program name '
          'without quotes stops that program.')
    print('kill-all --> ends all the programs.')
    print('dump logs --> copies and condenses all logs into one.')
    print('exit --> closes program, background programs continue to run.')
    
    
def status():
    # use all program/running programs list to display status
    # currently does not work 7/24/26

    print('Status')
    print('Command does not currently work.')

def start():
    # add program name as string in list below to run during start command.
    # currently works 7/24/26

    default_start_list = ['Air_Compressor_V0', 'Temperature_Logger_V0']
    
    for item in default_start_list:
        run_program(item)
        

def run_program(program):
    # untested as of 7/24/26

    prog_name = str(program) + '.py'
    p = subprocess.Popen(["python3", prog_name])
    returncode = p.wait()
    print('Running ', prog_name)

            
def stop(prog_to_run):
    # placeholder for stop module
    # currently does not work 7/24/26

    print('Stop: ', prog_to_run)
    print('Command currently does not work.')

def kill_all():
    # placeholder for kill-all, need a list of all programs/running programs
    # currently does not work 7/24/26

    print('kill-all')
    print('Command currently does not work.')

def dump_logs():
    # placeholder for dump logs, use list of all running programs
    # currently does not work

    print('dump logs')
    print('Command currently does not work 7/24/26.')
    
def end():
    # Ends program, might not actually be called in the program

    sys.exit


def main():
    config_file_name = '/HARRISON.config'
    config_file_location = '/home/peter/PythonProjects'
    last_login = config_file_read(config_file_name, config_file_location)
    welcome(last_login)
    prog_to_run = ''
    run = True
    program_list = ['Air_Compressor_V0', 'Temperature_Logger_V0']
    running_program_list = []
#    default_start_list = ['Temperature_Logger_V0']	# maybe have this here instead of in module

    while run:
        user_input = input('Enter command or "help" for list of commands: ')

        if user_input == 'welcome':
            welcome(last_login)
        elif user_input == 'help':
            help()
        elif user_input == 'status':  
            status()
        elif user_input == 'start':
            start()
        elif user_input[0:3] == 'run':
            prog_to_run = user_input[4:]
            run_program(prog_to_run)
        elif user_input[0:4] == 'stop':
            if user_input[5:] == 'air compressor':
                pass
                # end air compressor
            pass
            # write rest of individual programs
        elif user_input == 'kill-all':
            pass
            # end all programs
        elif user_input == 'dump logs':
            pass
            # write dump log program
        elif user_input == 'exit':
            run = False
            config_file_write(config_file_name, config_file_location)
        else:
            pass

    print('Goodbye.')        


if __name__ == '__main__':
    main()
