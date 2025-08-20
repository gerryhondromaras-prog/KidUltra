
# Οδηγός Υλοποίησης (Developer Playbook)

## 1. Setup
- Python 3.11/3.12 (64-bit)
- `pip install -r requirements.txt` (προσθέστε εδώ pytesseract, ezdxf κλπ όταν μπουν)

## 2. OCR
- Επιλογή: `pytesseract` ή `paddleocr`
- Εγκατάσταση Tesseract engine σε Windows και ρύθμιση PATH
- Normalization (fix Greek diacritics), quality filters
- Hook: `core/ocr.py::ocr_validate` να επιστρέφει structured output

## 3. DXF
- Βιβλιοθήκη: `ezdxf`
- Δημιουργία layers, styles, units
- Hook: `core/dxf.py::create_dxf_from_params`

## 4. Guardian Loop
- Παραμετροποίηση intervals στο `config.json`
- Προσθήκη στρατηγικών recovery (restart agents, task requeue, backoff)

## 5. EABP
- Προσαρμογή hard cap/intervals
- ΠΡΟΣΟΧΗ σε oversubscription: βελτίωση με process pool ή asyncio για βαριές δουλειές

## 6. Reporting
- Προγραμματισμός reports στις 10:00/14:00/19:00/00:00 (τοπική ώρα)
- Export HTML/PDF με embedded fonts
