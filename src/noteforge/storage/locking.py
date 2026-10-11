"""Reentrant thread/process locks for jobs on a local filesystem."""

from __future__ import annotations

import errno
import os
import threading
import time
from pathlib import Path
from typing import Any

from noteforge.errors import ErrorCode, NoteForgeError

_guard = threading.Lock()
_locks: dict[tuple[int, str], Any] = {}


class JobLock:
    """OS-owned locks survive lock files and are released on process exit.

    Execution and storage use separate locks so status polling stays responsive.
    Lock files must not be deleted while any process could be using this root.
    """

    def __init__(self, job_id: str, output_root: Path | str, *, execution: bool = False, timeout: float = 30):
        suffix = ".run.lock" if execution else ".lock"
        self.path = Path(output_root).resolve() / ".locks" / (job_id + suffix)
        self.timeout = timeout
        key = (os.getpid(), os.path.normcase(str(self.path)))
        with _guard:
            self._state = _locks.setdefault(key, {"lock": threading.RLock(), "depth": 0, "handle": None})

    def __enter__(self):
        state = self._state
        if not state["lock"].acquire(timeout=max(0, self.timeout)):
            raise self._busy()
        if state["depth"]:
            state["depth"] += 1
            return self
        handle = None
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            handle = self.path.open("a+b")
            deadline = time.monotonic() + self.timeout
            while True:
                try:
                    handle.seek(0)
                    if os.name == "nt":
                        import msvcrt

                        msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                    else:
                        import fcntl

                        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except OSError as error:
                    if error.errno not in (errno.EACCES, errno.EAGAIN, errno.EDEADLK):
                        raise
                    if time.monotonic() >= deadline:
                        raise self._busy() from error
                    time.sleep(0.01)
            state.update(depth=1, handle=handle)
            return self
        except BaseException:
            if handle:
                handle.close()
            state["lock"].release()
            raise

    def __exit__(self, *_args):
        state = self._state
        state["depth"] -= 1
        try:
            if not state["depth"]:
                handle = state["handle"]
                try:
                    handle.seek(0)
                    if os.name == "nt":
                        import msvcrt

                        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
                    else:
                        import fcntl

                        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
                finally:
                    handle.close()
                    state["handle"] = None
        finally:
            state["lock"].release()

    def _busy(self):
        return NoteForgeError(ErrorCode.STORAGE_FAILED, "job is busy; retry later", retryable=True)
