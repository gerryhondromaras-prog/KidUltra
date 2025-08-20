# -*- coding: utf-8 -*-
import threading, time, math

class EABPManager:
    """
    Exponential Agent Borrowing Protocol (EABP)
    - Every interval, for tasks not finished, double borrowed agents up to hard cap.
    """
    def __init__(self, registry, progress_store, events, doubling_interval_sec=10, hard_cap=512):
        self.registry = registry
        self.progress = progress_store
        self.events = events
        self.interval = doubling_interval_sec
        self.hard_cap = hard_cap
        self._stop = threading.Event()
        self._thr = threading.Thread(target=self._loop, daemon=True)

    def start(self):
        self._thr.start()

    def stop(self):
        self._stop.set()

    def _loop(self):
        while not self._stop.is_set():
            snap = self.progress.snapshot()
            for tid, info in snap.items():
                if info["progress"] >= 100.0:
                    continue
                cur = self.registry.borrowed_count(tid)
                nxt = min(self.hard_cap, max(1, cur * 2) if cur else 1)
                if nxt > cur:
                    self.registry.borrow_agents(tid, nxt - cur)
                    self.events.put(f"[EABP] Διπλασιασμός δανεισμένων για {tid[:8]}: {cur} ➜ {nxt}")
            time.sleep(self.interval)
