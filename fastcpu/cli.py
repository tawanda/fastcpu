from fastcore.script import call_parse,Param
# docs for fastcore.script can be found at https://github.com/fastai/fastscript

# from .core import *


"""
usage 

python -m fastcpu.cli --help

"""
@call_parse
def fastcpu_poll(
    path:Param("Path containing `to_run` directory", str)='.',
    exit:Param("Exit when `to_run` is empty", int)=1,
):
    "Poll `path` for scripts using `ResourcePoolGPU.poll_scripts`"
    # rp = ResourcePoolGPU(path=path)
    # rp.poll_scripts(exit_when_empty=exit)
    print('yay')

