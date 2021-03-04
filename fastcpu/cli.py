import logging
# docs for fastcore.script can be found at https://github.com/fastai/fastscript
from fastcore.script import call_parse, Param
from .core import *

logging.basicConfig(format='[%(levelname)s] %(module)s %(name)s: %(message)s', level=logging.DEBUG)

logger = logging.getLogger(__name__)


@call_parse
def fastcpu_poll(
        path: Param("Path containing `to_run` directory", str) = '.',
        exit_when_empty: Param("Exit when `to_run` is empty", int) = 1,
        poll_interval: Param("The duration between polls", int) = 0.1,
):
    """
    "Poll `path` for scripts using `ResourcePoolCPU.poll_scripts`"

    usage:
      python -m fastcpu.cli --help

      if module installed via pip there is a command line method:
        fastcpu_poll --help
        fastcpu_poll --path /home/tawanda/source/repos/yesplz/fastcpu/test_scripts --exit_when_empty 0 --poll_interval 60
    """
    logger.debug("Starting poll")

    rp = ResourcePoolCPU(path=path)
    rp.poll_scripts(exit_when_empty=exit_when_empty, poll_interval=poll_interval)

