
# Αρχιτεκτονική & Διαγράμματα (υψηλού επιπέδου)

```
+-------------------+        +----------------+
|   GUI (Tkinter)   |  <-->  |  Command Ctr   |
+---------+---------+        +--------+-------+
          |                           |
          v                           v
   +------+-------+             +-----+------+
   |  Guardian    |             |  EABP      |
   |   Loop       |             | (Scaling)  |
   +------+-------+             +-----+------+
          |                           |
          v                           v
   +------+-------+             +-----+------+
   |  Agent Reg.  |<----------->|Computing  |
   |  + Agents    |             |   Pool    |
   +------+-------+             +-----+------+
          |                           |
          v                           v
   +------+-------+             +-----+------+
   |   OCR/Data   |             |  CAD/DXF   |
   +--------------+             +------------+
```

Κύρια modules (src/KidUltra_Python):
- `app.py` (GUI/entry)
- `core/agents.py` (Agent threads, queue, borrowing)
- `core/guardian.py` (watchdog/heartbeat)
- `core/eabp.py` (exponential borrowing)
- `core/progress.py` (shared store)
- `core/config.py` + `config.json`
- `core/ocr.py` / `core/dxf.py` (stubs → να αντικατασταθούν)

