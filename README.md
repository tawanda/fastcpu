Inspired with code from https://github.com/fastai/fastgpu 

# fastcpu

> A queue service for quickly developing scripts that use all your CPUs efficiently

fastcpu provides a single command, fastcpu_poll, which polls a directory to check for scripts to run, and then runs them
on the first available CPU. If no CPUs are available, it waits until one is. If more than one CPU is available,
multiple scripts are run in parallel, one per CPU.
(Note currently the CPU load checking is not implemented, the scripts are run sequentially at polling interval)

## Installation

`pip install fastcpu`

## How to use

--help provides command help:

```
$ fastgpu_poll --help

optional arguments:

  -h, --help                         show this help message and exit
  --path PATH                        Path containing `to_run` directory (default: .)
  --exit_when_empty EXIT_WHEN_EMPTY  Exit when `to_run` is empty (default: 1)
  --poll_interval POLL_INTERVAL      The duration between polls (default: 0.1)
```

If installed via pip there is a handy command line method available

`fastcpu_poll --path /path/to/scripts --exit_when_empty 0 --poll_interval 60`

If running as a module 

`python -m fastcpu.cliu --path /path/to/scripts --exit_when_empty 0 --poll_interval 60` 

The above examples will run scrips located in the to_run subdirectory of the directory being monitored
The program will not exit when there are no scripts left to run, it will keep polling since we set that to 0
the polling interval is 60 seconds, it can be set as fractions of a second e.g 0.1

once the program starts it creates the following directory structure. you can then  your scripts in the to_run folder,
and the scrips are run sequentially

```
.
├── complete
├── fail
├── out
├── running
└── to_run
    ├── script_example1.sh
    └── script_example2.sh
```


`fastcpu_poll` will run each script in `to_run` in sorted order. 
Each script will be assigned to one CPU (*future*)

Once a script is selected to be run, it is moved into a directory called `running`. Once it's finished,
it's moved into complete or fail as appropriate. stdout and stderr are captured to files with the same name as the script,
plus stdout or stderr appended.

If exit_when_empty is 1 (which is the default), then once all scripts are run, `fastcpu_poll` will exit.
If it is 0 then `fastcpu_poll` will continue running until it is killed; it will keep polling for any new scripts that are added to `to_run`.



