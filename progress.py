# -*- coding: utf-8 -*-
import threading, time

class ProgressStore:
    def __init__(self):
        self._lock = threading.Lock()
        self._data = {}  # task_id -> dict(progress, borrowed, status, last_update)

    def update(self, task_id, progress=None, borrowed=None, status=None):
        with self._lock:
            it = self._data.setdefault(task_id, {"progress":0.0, "borrowed":0, "status":"pending", "last_update":time.time()})
            if progress is not None:
                it["progress"] = max(0.0, min(100.0, progress))
            if borrowed is not None:
                it["borrowed"] = borrowed
            if status is not None:
                it["status"] = status
            it["last_update"] = time.time()

    def snapshot(self):
        with self._lock:
            return {k:v.copy() for k,v in self._data.items()}

    def total_progress(self):
        snap = self.snapshot()
        if not snap: return 0.0
        return sum(v["progress"] for v in snap.values()) / len(snap)

    def stale_tasks(self, older_than_sec):
        now = time.time()
        snap = self.snapshot()
        return [tid for tid, v in snap.items() if now - v["last_update"] > older_than_sec]
