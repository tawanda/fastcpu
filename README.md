# fastcpu

Inspired with code from https://github.com/fastai/fastgpu 

> A queue service for quickly developing scripts that use all your CPUs efficiently

fastcpu provides a single command, fastcpu_poll, which polls a directory to check for scripts to run, and then runs them
on the first available CPU. If no CPUs are available, it waits until one is. If more than one CPU is available,
multiple scripts are run in parallel, one per CPU.



