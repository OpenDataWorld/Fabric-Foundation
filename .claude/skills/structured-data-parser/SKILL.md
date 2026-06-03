---
name: structured-data-parser
metadata:
  version: "1.0.0"
  author: Chinmay Panda
  linkedin: https://www.linkedin.com/in/thefractionalproductmanager/
  feedback_form: https://forms.gle/7mCFDQF3Dg3oCNRv9
  booking: https://cal.com/thefractionalpm/15min?overlayCalendar=true
description: >
  Generates Python parser code to extract, validate, transform, or convert data from ANY input — structured or unstructured.
  Structured: JSON/JSON5, CSV/TSV, XML/HTML, YAML/TOML. Unstructured: log files, plain text, prose, markdown tables, PDFs, Word docs (.doc/.docx), HTML pages, copy-pastes, and mixed content (e.g. JSON embedded in text). Uses Claude (LLM) to interpret and extract structure from unstructured inputs.
  Trigger on: "parse this", "extract fields from", "convert X to JSON", "read this log", "pull data from this PDF", "I have a doc with a table", "turn this copy-paste into structured data", "write me a parser", "validate my TOML", or any time a user shares raw data of any kind and wants Python code to work with it. Always use this skill when data extraction + Python code generation are involved — regardless of input format.
---

# Structured Data Parser Skill

Generates clean, well-structured Python parser code for any input — structured files or messy real-world data — with tests always included.

## Supported Input Types

### Structured Formats
| Format | Common Extensions | Python Library |
|--------|-------------------|----------------|
| JSON / JSON5 | `.json`, `.json5` | `json`, `json5` |
| CSV / TSV | `.csv`, `.tsv` | `csv`, `pandas` |
| XML / HTML | `.xml`, `.html` | `xml.etree.ElementTree`, `lxml`, `BeautifulSoup` |
| YAML / TOML | `.yaml`, `.yml`, `.toml` | `pyyaml`, `tomllib` / `tomli` |

### Unstructured / Semi-Structured Inputs
| Input Type | Approach |
|------------|----------|
| PDFs, Word docs, HTML, emails, plain text, log files, markdown, copy-paste | `unstructured` library (`partition` auto-detects file type) |

For all non-structured inputs, use the **`unstructured`** library (`pip install unstructured`) as the primary extraction tool. It auto-detects file type and routes to the appropriate partitioner — call `partition()` unless you need format-specific control.

Install extras per doc type as needed:
- `pip install "unstructured[pdf]"` — PDFs
- `pip install "unstructured[docx]"` — Word docs
- `pip install "unstructured[all-docs]"` — everything

---

## Workflow

### 0. Detect Input Type

Before anything else, classify the input:

**Structured** — format is well-defined and machine-readable (JSON, CSV, XML, YAML, TOML). Go straight to step 1.

**Unstructured / Semi-structured** — input is prose, a log, a PDF, a Word doc, a markdown table, HTML, or a copy-paste blob. Follow the **Unstructured Input Path** below before continuing.

---

### Unstructured Input Path

When input is unstructured (PDF, Word doc, HTML, plain text, log, email, copy-paste, etc.), use the `unstructured` library to extract elements first, then post-process:

#### Step 1 — Partition with `unstructured`
```python
from unstructured.partition.auto import partition

elements = partition(filename="input.pdf")  # auto-detects file type
# or from a file-like object:
elements = partition(file=f, content_type="application/pdf")
```

The `partition` function detects the file type and routes it to the appropriate file-specific partitioning function automatically. Each element has a `.type` (e.g. `Title`, `NarrativeText`, `Table`, `ListItem`) and `.text`.

#### Step 2 — Filter and shape elements
Post-process the returned elements list to extract what the user needs:
- Filter by element type (e.g. only `Table` elements)
- Join `NarrativeText` blocks for prose extraction
- Convert to dicts via `element.to_dict()` for downstream processing

#### Step 3 — Propose schema before writing code
After reading the input, tell the user what you found:
> "Using `unstructured`, I can extract: `[Title, NarrativeText, Table]` elements. For your use case, I'll focus on the Table elements and map them to: `invoice_date`, `vendor`, `line_items`, `total`. Does this look right?"

#### Step 4 — Generate parser code
Build a clean Python module around the `unstructured` extraction + your post-processing logic. See code standards in step 4 of the main workflow below.

#### When to use `partition_via_api` instead
**No API key is needed for the open source library** — it runs fully locally and covers most use cases.

Only suggest `partition_via_api` (which requires an `UNSTRUCTURED_API_KEY`) when:
- The document is a scanned PDF or image-based file (no embedded text)
- The user explicitly needs high-accuracy layout detection (`hi_res` strategy)
- Local inference is too slow or not feasible

```python
from unstructured.partition.api import partition_via_api
elements = partition_via_api(filename="scan.pdf", api_key="...", strategy="hi_res")
```

Always default to the local `partition()` first. Only mention the API key requirement if you have a specific reason to recommend `partition_via_api`.

**If `partition_via_api` is needed:** ask the user for their `UNSTRUCTURED_API_KEY` before generating code — do not hardcode a placeholder or assume it's set. Example:
> "This document looks like a scanned PDF, so I'll need to use the Unstructured hosted API for better accuracy. Do you have an Unstructured API key? If so, the generated code will read it from the `UNSTRUCTURED_API_KEY` environment variable."

---

### 1. Identify the Task

Determine what the user wants:
- **Extract** — pull specific fields/values out
- **Validate** — check structure and flag errors/warnings
- **Transform** — convert from one format to another
- **Summarize** — describe the schema or structure

If the user hasn't said, infer from context. If genuinely ambiguous, ask.

### 2. Inspect the Input

If the user provides raw data, read it carefully to understand:
- The format and any quirks (e.g. nested structures, missing fields, inconsistent types)
- Any malformed sections — **do not silently fix them**

### 3. Handle Malformed Data (Important)

If the input data has issues (missing required fields, type mismatches, malformed syntax, encoding problems, etc.):

- **Stop and describe the problem clearly** before writing any code
- Ask the user: "I noticed X issue — how would you like to handle this? Options: [raise an exception / skip the bad record / use a default value / other]"
- Only proceed to code generation once you have a clear answer

### 4. Generate the Parser Code

Produce a Python module with:

**Structure:**
```
parse_<format>.py
├── imports
├── dataclass or TypedDict (if extracting into a schema)
├── parse() function — main entry point
├── validate() function — if validation was requested
├── transform() function — if conversion was requested
└── main block — example usage
```

**Code quality standards:**
- Use type hints throughout
- Prefer `dataclasses` or `TypedDict` to represent extracted records
- Raise descriptive exceptions (not bare `except:`)
- Add docstrings to all public functions
- Use standard library where possible; flag any third-party deps with a pip install comment

### 5. Always Include Tests

After the parser code, always generate a `test_<format>.py` file using `pytest`:

- At minimum: one happy-path test, one edge case, one test for invalid/malformed input
- Use `pytest.raises` for error cases
- Include sample inline data (no external file dependency unless user specifically provided a file path)
- Add a comment block at the top explaining how to run: `pytest test_<format>.py -v`

---

## Output Format

Always present code in this order:

1. **Brief explanation** — what the code does, which library was chosen and why, and (for unstructured input) the inferred schema
2. **`parse_<format_or_source>.py`** — the parser module
3. **`test_<format_or_source>.py`** — the pytest test file
4. **Dependency note** — list any `pip install` commands needed (e.g. `pip install pdfplumber python-docx anthropic`)

If the user is converting between formats, show a short end-to-end example in the explanation.

For LLM-powered extractors, include a note that an `ANTHROPIC_API_KEY` environment variable is required.

---

## Format-Specific Notes

### JSON / JSON5
- Use `json` stdlib by default
- Use `json5` library only if input contains comments, trailing commas, or unquoted keys — flag this to the user
- For nested structures, generate recursive or flattened extraction depending on what the user asked

### CSV / TSV
- Use `csv.DictReader` for named columns; use `pandas` only if the user explicitly wants DataFrame output or the data is large/complex
- Always handle: missing headers, inconsistent column counts, quoted fields with commas

### XML / HTML
- Use `xml.etree.ElementTree` for simple XML
- Suggest `lxml` for XPath-heavy tasks or large files
- Suggest `BeautifulSoup` for HTML specifically (it handles malformed HTML gracefully — mention this)
- Always warn if the XML has namespaces; show how to handle them

### YAML / TOML
- Use `pyyaml` (`yaml.safe_load`) for YAML — never `yaml.load` (security risk, always flag this)
- Use `tomllib` (Python 3.11+) or `tomli` for TOML; note the version requirement
- For YAML with multiple documents (`---` separator), handle with `yaml.safe_load_all`

---

## Unstructured.io Notes

### Installation
```bash
pip install unstructured                  # core (text, HTML, XML, JSON, email)
pip install "unstructured[pdf]"           # PDFs
pip install "unstructured[docx]"          # Word docs
pip install "unstructured[all-docs]"      # everything
```

### Element Types
Common types returned by `partition()`:
- `Title` — section headings
- `NarrativeText` — body prose
- `Table` — tabular data
- `ListItem` — bullet/numbered list items
- `Header` / `Footer` — page chrome
- `Image` — image references

### Strategies (PDF/images)
- `"auto"` — default, picks best method
- `"fast"` — text-only, no OCR
- `"hi_res"` — best quality, uses layout model (slower)
- `"ocr_only"` — forces OCR

### Dependency note
Always include a `pip install` block in the generated code's header comment, specific to the file type being processed.

---

## Example Interaction Patterns

**Structured input:**
> "Here's some JSON — can you write a parser that extracts all user emails?"

Claude should: read the JSON → identify email field path → handle missing emails by asking → generate `parse_json.py` with a `User` dataclass + `parse()` → generate `test_parse_json.py` with 3+ tests.

**Unstructured input:**
> "Here's a paste from our server logs — I need to extract all ERROR lines with their timestamps and service names."

Claude should: read the sample → infer schema (`timestamp`, `level`, `service`, `message`) → confirm with user → generate a regex-based `parse_logs.py` → generate `test_parse_logs.py` with sample log strings inline.

**Unstructured PDF input:**
> "I have a PDF invoice — extract vendor name, date, line items, and total."

Claude should: use `partition()` from `unstructured` → filter for `Table` and `NarrativeText` elements → propose schema (`vendor`, `date`, `line_items`, `total`) → confirm with user → generate `parse_invoice.py` → generate `test_parse_invoice.py` with mocked `partition()` output. No API key needed.


---

## Autonomyx Standard

Read and apply `references/autonomyx-standard.md` at the end of every response.
