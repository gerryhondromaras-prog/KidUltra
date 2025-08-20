# -*- coding: utf-8 -*-
import threading, time

class GuardianLoop:
    def __init__(self, registry, progress_store, events, inactivity_check_sec=30, heartbeat_sec=3):
        self.registry = registry
        self.progress = progress_store
        self.events = events
        self.inactivity_check_sec = inactivity_check_sec
        self.heartbeat_sec = heartbeat_sec
        self._stop = threading.Event()
        self._thr = threading.Thread(target=self._loop, daemon=True)

    def start(self):
        self._thr.start()

    def stop(self):
        self._stop.set()

    def _loop(self):
        last_total = -1.0
        last_change_ts = time.time()
        while not self._stop.is_set():
            total = self.progress.total_progress()
            if abs(total - last_total) > 1e-6:
                last_change_ts = time.time()
                last_total = total
            else:
                # no change tracked
                pass

            # inactivity check
            if time.time() - last_change_ts > self.inactivity_check_sec:
                self.events.put("[Guardian] Αδράνεια ανιχνεύθηκε — ανατροφοδότηση και ώθηση EABP.")
                # nudge: borrow small count to reignite
                for tid in self.progress.snapshot().keys():
                    self.registry.borrow_agents(tid, 1)
                last_change_ts = time.time()

            self.events.put(f"[Guardian] Heartbeat: συνολική πρόοδος {total:.1f}%")
            time.sleep(self.heartbeat_sec)
