# -*- coding: utf-8 -*-
import threading, time, uuid, random

class Task:
    def __init__(self, name, initial_progress=0.0, target=100.0, priority=1, branch="generic"):
        self.id = str(uuid.uuid4())
        self.name = name
        self.progress = initial_progress
        self.target = target
        self.priority = priority
        self.branch = branch

class Agent(threading.Thread):
    def __init__(self, agent_id, registry, progress_store, events):
        super().__init__(daemon=True)
        self.agent_id = agent_id
        self.registry = registry
        self.progress_store = progress_store
        self.events = events
        self._stop = threading.Event()

    def run(self):
        self.events.put(f"[Agent#{self.agent_id}] Εκκίνηση.")
        while not self._stop.is_set():
            task = self.registry.get_task_for_agent(self.agent_id)
            if task is None:
                time.sleep(0.2)
                continue
            self._work_on_task(task)

    def _work_on_task(self, task: Task):
        self.events.put(f"[Agent#{self.agent_id}] Εργασία στο: {task.name}")
        # Simulated work
        for _ in range(25):
            if self._stop.is_set(): break
            inc = random.uniform(0.5, 2.5)
            task.progress = min(task.target, task.progress + inc)
            self.progress_store.update(task.id, progress=task.progress, status=f"working:{task.name}")
            time.sleep(random.uniform(0.2, 0.6))
            if task.progress >= task.target:
                break
        self.progress_store.update(task.id, status="done")
        self.events.put(f"[Agent#{self.agent_id}] Ολοκλήρωσε: {task.name} ({task.progress:.1f}%)")

    def stop(self):
        self._stop.set()

class AgentRegistry:
    def __init__(self, progress_store, events, max_agents_per_branch=64):
        self.progress = progress_store
        self.events = events
        self.max_agents_per_branch = max_agents_per_branch
        self._lock = threading.Lock()
        self._agents = {}   # agent_id -> Agent
        self._queue = []    # task list
        self._borrowed = {} # task_id -> borrowed_count
        # bootstrap a small pool
        for i in range(8):
            self._spawn_agent()

    def _spawn_agent(self):
        agent_id = len(self._agents) + 1
        ag = Agent(agent_id, self, self.progress, self.events)
        self._agents[agent_id] = ag
        ag.start()
        self.events.put(f"[Registry] Νέος agent: #{agent_id}")

    def enqueue_task(self, task: Task):
        with self._lock:
            self._queue.append(task)
            self.progress.update(task.id, progress=task.progress, borrowed=self._borrowed.get(task.id,0), status="queued")

    def get_task_for_agent(self, agent_id):
        with self._lock:
            # pick highest priority first or earliest
            if not self._queue:
                return None
            # simple heuristic: pick first not-done
            for t in list(self._queue):
                # if not done:
                snap = self.progress.snapshot().get(t.id, {})
                if snap.get("progress", 0.0) < 100.0:
                    return t
                else:
                    self._queue.remove(t)
                    continue
            return None

    def borrow_agents(self, task_id, count):
        with self._lock:
            cur = self._borrowed.get(task_id, 0)
            self._borrowed[task_id] = cur + count
            self.progress.update(task_id, borrowed=self._borrowed[task_id])
            # spawn if needed
            for _ in range(count):
                self._spawn_agent()

    def borrowed_count(self, task_id):
        with self._lock:
            return self._borrowed.get(task_id, 0)

    def tasks(self):
        with self._lock:
            return list(self._queue)

    def stop_all(self):
        for a in list(self._agents.values()):
            a.stop()
        self.events.put("[Registry] Στάλθηκε σήμα τερματισμού σε όλους τους agents.")
