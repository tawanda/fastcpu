import logging

__all__ = ['setup_dirs', 'find_next_script', 'safe_rename', 'ResourcePoolBase', 'ResourcePoolCPU']

from datetime import datetime

logger  = logging.getLogger(__name__)

# Cell
import os
import subprocess
from copy import copy
from threading import Thread
from time import sleep
from uuid import uuid4

os.environ['CUDA_DEVICE_ORDER'] = 'PCI_BUS_ID'
from fastcore.all import *


# Cell
def setup_dirs(path):
    "Create and return the following subdirs of `path`: to_run running complete fail out"
    path.mkdir(exist_ok=True)
    dirs = L(path / o for o in 'to_run running complete fail out'.split())
    for o in dirs: o.mkdir(exist_ok=True)
    return dirs


def find_next_script(p):
    """Get the first script from `p` (in sorted order)"""
    files = p.ls().sorted().filter(Self.is_file())
    if files:
        return files[0]


def safe_rename(file, dest):
    """Move `file` to `dest`, prefixing a random uuid if there's a name conflict"""
    to_name = dest / file.name
    if to_name.exists():
        u = uuid4()

        date_now = datetime.now().strftime("%c").replace(":", "-").replace(" ", "_")
        file_name, file_extension = os.path.splitext(file.name)

        to_name = dest / f'{file_name}--{date_now}--{u}{file_extension}'

        logger.warning(f'Using unique name {to_name}')

    file.replace(to_name)
    return to_name


class ResourcePoolBase():
    def __init__(self, path):
        self.path = Path(path)
        setup_dirs(self.path)

    def _lockpath(self, ident):
        return self.path / f'{ident}.lock'

    def _is_locked(self, ident):
        return self._lockpath(ident).exists()

    def lock(self, ident, txt='locked'):
        self._lockpath(ident).write_text(str(txt))

    def unlock(self, ident):
        return self._lockpath(ident).unlink() if self._is_locked(ident) else None

    def is_available(self, ident):
        return not self._is_locked(ident)

    def all_ids(self):
        raise NotImplementedError

    def find_next(self):
        return first(o for o in self.all_ids() if self.is_available(o))

    def lock_next(self):
        ident = self.find_next()
        if ident is None:
            return

        self.lock(ident)
        return ident

    def _launch(self, script, ident, env):
        with (self.path / 'out' / f'{script.name}.stderr').open("w") as stderr:
            with (self.path / 'out' / f'{script.name}.stdout').open("w") as stdout:
                process = subprocess.Popen(str(script), env=env, stdout=stdout, stderr=stderr)
                self.lock(ident, str(process.pid))
                return process.wait()

    def _run(self, script, ident):
        logger.debug(f"running script ident: {ident}")
        failed = False
        env = copy(os.environ)

        try:
            res = self._launch(script, ident, env=env)

        except Exception as e:
            failed = str(e)
        (self.path / 'out' / f'{script.name}.exitcode').write_text(failed if failed else str(res))
        dest = self.path / 'fail' if failed or res else self.path / 'complete'
        finish_name = safe_rename(script, dest)
        self.unlock(ident)

    def run(self, *args, **kwargs):
        thread = Thread(target=self._run, args=args, kwargs=kwargs)
        logger.debug("Starting Thread..")
        thread.start()

    def poll_scripts(self, poll_interval=0.1, exit_when_empty=True):
        while True:
            sleep(poll_interval)
            script = find_next_script(self.path / 'to_run')
            if script is None:
                if exit_when_empty:
                    logger.debug("No more scripts to run, exit_when_empty set to True, exiting..")
                    break
                else:
                    continue

            logger.debug(f"Script found {script}")

            ident = self.lock_next()
            if ident is None: continue
            run_name = safe_rename(script, self.path / 'running')
            self.run(run_name, ident)


add_docs(ResourcePoolBase, "Base class for locked access to list of idents",
         unlock="Remove lockfile for `ident`",
         lock="Create lockfile for `ident`",
         is_available="Is `ident` available",
         all_ids="All idents (abstract method)",
         find_next="Finds next available resource, or None",
         lock_next="Locks an available resource and returns its ident, or None",
         run="Run `script` using resource `ident`",
         poll_scripts="Poll `to_run` for scripts and run in parallel on available resources")


# class FixedWorkerPool(ResourcePoolBase):
#     "Vends locked access to fixed list of idents"
#
#     def __init__(self, worker_ids, path):
#         super().__init__(path)
#         self.worker_ids = worker_ids
#
#     def all_ids(self):
#         "All available idents"
#         return self.worker_ids


# Cell
class ResourcePoolCPU(ResourcePoolBase):
    "Vends locked access to NVIDIA GPUs"

    def __init__(self, path):
        # assume a 2 core processor, these are fake id's to be implemented properly
        self.ids = [0, 1]
        super().__init__(path)

    def _launch(self, script, ident, env):
        return super()._launch(script, ident, env)

    # def is_available(self, ident):
    #     """
    #     Right now the CPU is always available, in next iteration we check if the CPU is overloaded or not
    #     :param ident:
    #     :return:
    #     """
    #     return True

    def all_ids(self):
        """All CPUs"""
        return self.ids
