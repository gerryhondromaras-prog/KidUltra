
# Λειτουργικές & Μη-Λειτουργικές Προδιαγραφές (Specs)

## Στόχος
Παράδοση της εφαρμογής **Kid Ultra** με:
- Επιτραπέζια εφαρμογή (Windows, macOS) με GUI.
- Mobile Management (iOS/Android) για live παρακολούθηση/παρέμβαση.
- Agents που εκτελούν διεργασίες (UI update, OCR validation, DXF generation, QA/Auto-healing).
- Guardian Loop για ανίχνευση αδράνειας/αυτο-ανάκαμψη.
- EABP για εκθετική κλιμάκωση δανεισμένων agents.
- Real-time πίνακας προόδου, αυτόματες αναφορές.
- Υποστήριξη Ελληνικών/Αγγλικών με σωστή απόδοση χαρακτήρων.

## Κλάδοι (Branches) & Ενδεικτικοί Agents
- **Κλάδος 1: UI/UX & Modules**
  - Agents: UI Builder, Theme Engine, Widget Linter, Accessibility Checker
  - Διεργασίες: UI Update Module, Font embedding, i18n, theming.
- **Κλάδος 2: Data & OCR**
  - Agents: OCR Validator, OCR Trainer, PDF/Image Parser, Normalizer
  - Διεργασίες: Smart OCR validation (PaddleOCR/Tesseract), PDF parsing, error recovery.
- **Κλάδος 3: CAD & Exports**
  - Agents: DXF Generator, Geometry Validator, Layer Styler
  - Διεργασίες: Παραγωγή DXF, έλεγχος τοπολογίας, export pipelines.
- **Κλάδος 4: QA / Error Hunter (νέος)**
  - Agents: Fuzz Tester, Regression Runner, Log Analyzer, Auto-Fixer
  - Διεργασίες: Συνεχής εκτέλεση όλων των modules, εντοπισμός σφαλμάτων & άμεση επιδιόρθωση.
- **R&D**
  - Agents: Kernel Optimizer, Heuristics Tuner, Performance Profiler.
- **Command Center**
  - Agents: Orchestrator, Scheduler, Notifier.
- **Computing Pool (δανεισμός)**
  - Άπειροι ephemeral agents που δανείζονται με EABP.
- **External/Kernel**
  - Agent 0 (Kernel), Kernel Optimizer, Integrations.

## Πρωτόκολλα
- **Guardian Loop**
  - Heartbeat κάθε 3s, ανίχνευση αδράνειας ανά 30s (παράδειγμα).
  - Σε αδράνεια: auto-nudge + borrow agents.
- **EABP (Exponential Agent Borrowing Protocol)**
  - Διπλασιασμός δανεισμένων agents ανά 10s, έως σκληρό όριο (π.χ. 512).
  - AI-based adaptive priorities per task/branch.
- **Live Progress Feed**
  - Πίνακας real-time, καρφιτσωμένος στο UI.
  - Reporting slots: 10:00, 14:00, 19:00, 00:00 (Europe/Athens).

## Γλωσσική Υποστήριξη & Γραμματοσειρές
- Ενσωμάτωση γραμματοσειράς με πλήρες Greek charset (π.χ. Noto Sans, Inter).
- Σε PDF: embed fonts (subset) μέσω reportlab/WeasyPrint.
- Σε UI: επιβολή `font=("Segoe UI", 10)` σε Windows και fallback σε macOS/Linux.

## iOS/Android Διανομή
- iOS: TestFlight μέσω δικού σου Apple Developer account (απαιτείται εκτός αυτής της πλατφόρμας).
- Android: APK/Play Console.
- Σημαντικό: Ο παρών βοηθός *δεν μπορεί* να στείλει email/ανεβάσει σε stores ή cloud· ο προγραμματιστής το αναλαμβάνει.

## Μη-Λειτουργικά
- Απόκριση UI < 100ms.
- Safe multithreading (agents σε threads/processes).
- Logging, crash recovery, telemetry.
