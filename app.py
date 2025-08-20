# -*- coding: utf-8 -*-
import threading
import queue
import tkinter as tk
from tkinter import ttk, messagebox
from core.config import load_config
from core.progress import ProgressStore
from core.agents import AgentRegistry, Task
from core.guardian import GuardianLoop
from core.eabp import EABPManager

APP_TITLE = "Kid Ultra – Python Edition (Demo)"
REFRESH_MS = 500  # refresh UI every 0.5s

class KidUltraApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("980x620")
        self.minsize(900, 580)

        self.cfg = load_config()
        self.progress = ProgressStore()
        self.events = queue.Queue()

        self.registry = AgentRegistry(self.progress, self.events, max_agents_per_branch=64)
        self.eabp = EABPManager(self.registry, self.progress, self.events,
                                doubling_interval_sec=self.cfg["eabp"]["interval_sec"],
                                hard_cap=self.cfg["eabp"]["hard_cap"])
        self.guardian = GuardianLoop(self.registry, self.progress, self.events,
                                     inactivity_check_sec=self.cfg["guardian"]["inactivity_check_sec"],
                                     heartbeat_sec=self.cfg["guardian"]["heartbeat_sec"])

        self._build_ui()
        self._start_background_threads()

    # ---------------- UI ----------------
    def _build_ui(self):
        top = ttk.Frame(self); top.pack(fill="x", padx=12, pady=8)
        ttk.Label(top, text="Πίνακας Ελέγχου – Ζωντανή πρόοδος", font=("Segoe UI", 14, "bold")).pack(side="left")
        ttk.Button(top, text="Έναρξη Demo", command=self.start_demo).pack(side="right", padx=6)
        ttk.Button(top, text="Στοπ Demo", command=self.stop_demo).pack(side="right")

        mid = ttk.Frame(self); mid.pack(fill="both", expand=True, padx=12, pady=8)

        # Progress tree
        left = ttk.Frame(mid); left.pack(side="left", fill="both", expand=True)
        self.tree = ttk.Treeview(left, columns=("progress","borrowed","status"), show="headings", height=18)
        self.tree.heading("progress", text="Πρόοδος (%)")
        self.tree.heading("borrowed", text="Δανεισθέντες Agents")
        self.tree.heading("status", text="Κατάσταση")
        self.tree.column("progress", width=120, anchor="center")
        self.tree.column("borrowed", width=160, anchor="center")
        self.tree.column("status", width=220, anchor="w")
        self.tree.pack(fill="both", expand=True, side="top")

        # Log box
        right = ttk.Frame(mid); right.pack(side="left", fill="both", padx=8)
        ttk.Label(right, text="Ζωντανά Συμβάντα (Guardian/EABP/Agents)").pack(anchor="w")
        self.log = tk.Text(right, width=48, height=22)
        self.log.pack(fill="both", expand=True)

        # Status bar
        self.status_var = tk.StringVar(value="Έτοιμο.")
        status = ttk.Frame(self); status.pack(fill="x", padx=12, pady=4)
        ttk.Label(status, textvariable=self.status_var).pack(side="left")

        self.after(REFRESH_MS, self._on_timer)

    def _start_background_threads(self):
        self.bg_running = True
        self.bg = threading.Thread(target=self._event_pump, daemon=True)
        self.bg.start()

        self.guardian.start()
        self.eabp.start()

    def _event_pump(self):
        while self.bg_running:
            try:
                event = self.events.get(timeout=0.2)
                self._append_log(event)
            except Exception:
                pass

    def _append_log(self, txt):
        self.log.insert("end", txt + "\n")
        self.log.see("end")

    def _on_timer(self):
        # refresh tree
        self.tree.delete(*self.tree.get_children())
        snapshot = self.progress.snapshot()
        for task_id, info in snapshot.items():
            self.tree.insert("", "end", values=(f'{info["progress"]:.1f}', info["borrowed"], info["status"]))
        total = self.progress.total_progress()
        self.status_var.set(f"Συνολική πρόοδος: {total:.1f}% | Συνολικά tasks: {len(snapshot)}")
        self.after(REFRESH_MS, self._on_timer)

    # ---------- Demo control ----------
    def start_demo(self):
        # Seed demo tasks across branches
        demo_tasks = [
            ("Branch-1:UI Update Module", 0.0),
            ("Branch-2:OCR Validator", 0.0),
            ("Branch-3:DXF Generator", 0.0),
            ("Branch-R&D:Auto Healing", 0.0),
            ("Branch-4:QA & Error Hunter", 0.0),
        ]
        for name, p in demo_tasks:
            t = Task(name=name, initial_progress=p, target=100.0, priority=1)
            self.registry.enqueue_task(t)
            self.events.put(f"[Init] Προστέθηκε task: {name}")
        messagebox.showinfo("Kid Ultra", "Ξεκίνησε το demo. Οι agents εργάζονται με EABP & Guardian Loop.")

    def stop_demo(self):
        self.registry.stop_all()
        self.events.put("[System] Σταμάτησαν οι agents.")

    def on_close(self):
        if messagebox.askyesno("Έξοδος", "Θέλεις σίγουρα να κλείσεις;"):
            self.bg_running = False
            self.registry.stop_all()
            self.guardian.stop()
            self.eabp.stop()
            self.destroy()

if __name__ == "__main__":
    app = KidUltraApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
