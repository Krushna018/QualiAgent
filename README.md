# 🧪 QualiAgent — Multi-Agent Software Test Quality Analysis

> **A research-oriented multi-agent framework for automated, evidence-grounded analysis of Python software test quality.**

QualiAgent analyzes Python repositories to identify potential test-quality problems such as **weak assertions, redundant assertions, flaky-test indicators, excessive test complexity, outdated testing APIs, and missing test oracles**.

The framework combines **static code analysis, specialized agents, optional LLM reasoning, evidence-based review, reproducible benchmarking, and human evaluation support**.

---

## 📌 Overview

Software tests are critical for maintaining reliable software, but poorly designed tests can create false confidence and increase maintenance costs.

Traditional static-analysis approaches can identify predefined patterns, but many test-quality problems require contextual interpretation.

**QualiAgent addresses this through a specialized multi-agent workflow** where each stage performs a distinct responsibility:

```text
Python Repository
       │
       ▼
┌─────────────────────────┐
│ Repository Context      │
│ Agent                   │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Static Analysis         │
│ Agent                   │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Test Quality            │
│ Agent                   │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Reviewer Agent          │
└────────────┬────────────┘
             │
             ▼
     Accepted Findings
```

An optional **LLM Reasoning Agent** is also included as a separate single-agent experimental path for comparison with the multi-agent approach.

---

# ✨ Key Features

* 🤖 **Four-Agent Analysis Pipeline**
* 🔍 **Automated Test-Smell Detection**
* 🧾 **Evidence-Grounded Findings**
* 🎯 **Severity & Confidence Scoring**
* 👨‍⚖️ **Evidence-Aware Reviewer**
* 💡 **Automated Remediation Recommendations**
* 🧠 **Optional LLM-Based Reasoning**
* 📴 **Offline Deterministic Execution**
* 🧪 **Reproducible 1,500-Test Benchmark**
* 👨‍🔬 **600-Item Stratified Review Dataset**
* 📂 **Local Python Repository Analysis**
* 📊 **Precision / Recall / F1 Evaluation Utilities**

---

# 🧩 Multi-Agent Architecture

## 1. Repository Context Agent

The **Repository Context Agent** analyzes the repository before quality analysis begins.

It extracts:

* Repository name
* Number of files
* Number of test cases
* Frequently used imports
* Available repository metadata

This contextual information is passed to downstream agents.

---

## 2. Static Analysis Agent

The **Static Analysis Agent** applies explicit, traceable rules to Python test cases.

Currently implemented detectors include:

| Detector                    | Purpose                                         |
| --------------------------- | ----------------------------------------------- |
| `weak_assertion`            | Detects assertions that provide weak validation |
| `redundant_assertion`       | Detects duplicate assertions                    |
| `flaky_test_indicator`      | Detects timing or nondeterministic operations   |
| `excessive_test_complexity` | Detects tests with excessive branching          |
| `outdated_test_dependency`  | Detects legacy testing APIs                     |

Examples of analyzed patterns include:

```text
assert True
assert value is not None
time.sleep(...)
random.random(...)
datetime.now(...)
time.time(...)
mock.patch
nose.tools
pytest.yield_fixture
```

Each detector produces traceable evidence when a pattern is identified.

---

## 3. Test Quality Agent

The **Test Quality Agent** performs AST-based analysis of individual test cases.

It currently reasons about:

### Missing Test Oracles

Tests without assertions or `pytest.raises` expectations are flagged as potential missing-oracle cases.

### Oversized Tests

Tests exceeding the configured source-length threshold are flagged as potentially difficult to maintain and recommended for decomposition.

The agent uses Python's `ast` module to inspect test structure rather than relying only on raw text matching.

---

## 4. Reviewer Agent

The **Reviewer Agent** validates candidate findings before they are returned as accepted findings.

The reviewer considers:

* Finding confidence
* Supporting evidence
* Repository context
* Issue information

A finding is accepted only when the reviewer determines that sufficient evidence exists.

### Offline Reviewer

When no LLM is configured, QualiAgent uses deterministic evidence-based reviewer logic.

### LLM Reviewer

When an OpenAI-compatible endpoint is configured, the reviewer can use LLM reasoning while being instructed to reason only from the supplied evidence.

This hybrid design allows the system to remain **reproducible and runnable without network access**.

---

# 🧠 Optional LLM Reasoning Agent

QualiAgent also implements an optional **single-agent LLM reasoning path**.

The `LLMReasoningAgent` receives:

* Test source code
* Repository context

and requests structured output containing:

```text
issue_type
severity
confidence
evidence
recommendation
```

This component is intended for experimental comparison between:

```text
Rule-Based Analysis
        │
        ├───────────────┐
        ▼               ▼
Single-Agent LLM   Multi-Agent Workflow
                        │
                        ▼
                Evidence + Reviewer
```

This supports the project's research question:

> **When does a specialized multi-agent workflow improve software-test quality analysis relative to simpler rule-based and single-agent approaches?**

---

# 🔎 Evidence-Grounded Findings

QualiAgent does not return only natural-language explanations.

Each finding is represented using structured information:

```text
Finding
├── repository
├── path
├── test_name
├── issue_type
├── severity
├── confidence
├── evidence
├── recommendation
└── source_agent
```

After reviewer validation, additional review information is attached:

```text
review_confidence
review_rationale
```

This makes findings easier to inspect, evaluate, and reproduce.

---

# 📋 Example Finding

A detected issue follows the following conceptual structure:

```json
{
  "repository": "example_repo",
  "path": "tests/test_example.py",
  "test_name": "test_value",
  "issue_type": "weak_assertion",
  "severity": "medium",
  "confidence": 0.88,
  "evidence": [
    "matched weak assertion pattern"
  ],
  "recommendation": "Replace weak assertions with behavior-specific expectations.",
  "source_agent": "static_analysis"
}
```

The actual output is generated programmatically by the framework.

---

# 🧪 Reproducible Benchmark

QualiAgent includes a deterministic benchmark generator for controlled experimentation.

Run:

```bash
python scripts/generate_benchmark.py
```

The generator creates:

| Benchmark Component  |  Quantity |
| -------------------- | --------: |
| Repositories         |    **30** |
| Tests per repository |    **50** |
| Total test cases     | **1,500** |
| Issue categories     |     **6** |

The six benchmark categories are:

1. `weak_assertion`
2. `redundant_assertion`
3. `flaky_test_indicator`
4. `excessive_test_complexity`
5. `outdated_test_dependency`
6. `missing_oracle`

The benchmark generation uses a fixed random seed, making the dataset reproducible.

---

# 📊 Benchmark Analysis

Run the complete multi-agent benchmark using:

```bash
python scripts/run_benchmark.py
```

The script:

1. Loads each benchmark repository.
2. Builds the repository artifact.
3. Executes the four-agent pipeline.
4. Collects accepted findings.
5. Stores the results in:

```text
results/multi_agent_findings.csv
```

The benchmark runner reports:

```text
Repositories analyzed
Accepted findings
Output location
```

---

# 👨‍🔬 Human Evaluation

QualiAgent includes a stratified sampling pipeline for human evaluation.

Generate the review dataset:

```bash
python scripts/create_manual_review_sample.py
```

This creates:

```text
data/manual_review_600.csv
```

The review sample contains:

* **600 examples**
* **6 issue classes**
* **100 examples per class**

The CSV includes fields for:

```text
repository
path
test_name
label
reviewer_label
reviewer_notes
```

Human reviewers can populate `reviewer_label` and `reviewer_notes` to evaluate the correctness of automated classifications.

---

# 📈 Evaluation Metrics

The project includes evaluation utilities using `scikit-learn`.

Supported evaluation approaches include:

### Binary Classification

```python
evaluate_binary(labels, predictions)
```

Returns:

* Precision
* Recall
* F1-score

### Multiclass Classification

```python
evaluate_multiclass(labels, predictions)
```

Produces a multiclass classification report.

### Agreement Rate

```python
agreement_rate(a, b)
```

Measures agreement between two sequences of labels.

---

# 🔬 Research Design

QualiAgent is designed around the following experimental comparison:

| Approach             | Description                                         |
| -------------------- | --------------------------------------------------- |
| **Rule-Based**       | Explicit static-analysis rules                      |
| **Single-Agent LLM** | Optional LLM reasoning agent                        |
| **Multi-Agent**      | Context → Static Analysis → Test Quality → Reviewer |

The objective is to investigate whether specialized agent collaboration can improve the reliability and explainability of automated test-quality analysis.

### Recommended Metrics

* Precision
* Recall
* F1-score
* Per-class performance
* Agreement rate
* Unsupported recommendation rate
* Evidence consistency

---

# 🛠️ Technologies Used

| Category                          | Technologies                           |
| --------------------------------- | -------------------------------------- |
| **Programming Language**          | Python                                 |
| **Code Analysis**                 | Python `ast`, Regular Expressions      |
| **Machine Learning / Evaluation** | scikit-learn                           |
| **Data Processing**               | Pandas, NumPy                          |
| **LLM Integration**               | OpenAI-Compatible Chat Completions API |
| **HTTP Client**                   | Requests                               |
| **Testing**                       | Pytest                                 |
| **Data Format**                   | JSON, CSV                              |
| **Architecture**                  | Multi-Agent Workflow                   |

---

# 📁 Project Structure

```text
QualiAgent/
│
├── data/
│   ├── benchmark_repos/
│   ├── benchmark_manifest.json
│   └── manual_review_600.csv
│
├── docs/
│   └── research_design.md
│
├── qualiagent/
│   ├── agents/
│   │   ├── repository_context.py
│   │   ├── static_analysis.py
│   │   ├── quality_agent.py
│   │   ├── reviewer.py
│   │   └── llm_reasoner.py
│   │
│   ├── llm/
│   │   └── provider.py
│   │
│   ├── rules/
│   │   └── static_rules.py
│   │
│   ├── benchmark.py
│   ├── models.py
│   ├── pipeline.py
│   └── repository.py
│
├── scripts/
│   ├── generate_benchmark.py
│   ├── run_benchmark.py
│   ├── create_manual_review_sample.py
│   └── analyze_repository.py
│
├── tests/
│   └── test_project.py
│
├── requirements.txt
└── README.md
```

---

# 💻 Installation

## Prerequisites

* Python 3.x
* pip
* Optional: OpenAI-compatible LLM endpoint

## 1. Clone Repository

```bash
git clone https://github.com/Krushna018/QualiAgent.git
cd QualiAgent
```

## 2. Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python -m venv .venv
source .venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Usage

## Run Automated Tests

```bash
pytest -q
```

The project includes tests covering:

* Weak-assertion detection
* Four-agent pipeline configuration
* Local repository test extraction
* Offline pipeline execution

---

## Generate Benchmark

```bash
python scripts/generate_benchmark.py
```

Expected benchmark:

```text
30 repositories
1,500 test cases
```

---

## Run Multi-Agent Analysis

```bash
python scripts/run_benchmark.py
```

Results are saved to:

```text
results/multi_agent_findings.csv
```

---

## Generate Human Review Sample

```bash
python scripts/create_manual_review_sample.py
```

Output:

```text
data/manual_review_600.csv
```

---

## Analyze a Local Repository

```bash
python scripts/analyze_repository.py /path/to/repository
```

This allows QualiAgent to analyze a local Python project outside the included benchmark.

---

# 🤖 LLM Configuration

QualiAgent supports OpenAI-compatible chat-completion APIs.

Set:

```bash
QUALIAGENT_LLM_BASE_URL="https://api.openai.com/v1"
QUALIAGENT_LLM_API_KEY="YOUR_KEY"
QUALIAGENT_LLM_MODEL="YOUR_MODEL"
```

Example:

```bash
export QUALIAGENT_LLM_BASE_URL="https://api.openai.com/v1"
export QUALIAGENT_LLM_API_KEY="YOUR_KEY"
export QUALIAGENT_LLM_MODEL="YOUR_MODEL"
```

The provider sends structured JSON requests with:

* Temperature = `0`
* JSON response format
* System instructions
* Repository/test context

Compatible local endpoints can also be supplied through the base URL.

> **Security:** Never commit API keys or secrets to GitHub.

---

# 📴 Offline Mode

QualiAgent does **not require an LLM API to run the main pipeline**.

Without LLM configuration:

```text
Repository
    ↓
Context Agent
    ↓
Static Analysis Agent
    ↓
Test Quality Agent
    ↓
Deterministic Reviewer
    ↓
Accepted Findings
```

This makes the core framework suitable for reproducible local experiments.

---

# 🧪 Testing

Run:

```bash
pytest -q
```

The test suite verifies the core implementation, including:

```text
✓ Static analysis
✓ Four-agent pipeline
✓ Repository loading
✓ Test extraction
✓ Offline reviewer execution
```

---

# 📊 Project Scale

| Component                     |                       Implementation |
| ----------------------------- | -----------------------------------: |
| Main pipeline agents          |                                **4** |
| Optional LLM reasoning agent  |                                **1** |
| Test-quality issue categories |                                **6** |
| Benchmark repositories        |                               **30** |
| Benchmark tests               |                            **1,500** |
| Human-review sample           |                              **600** |
| Evaluation metrics            | **Precision, Recall, F1, Agreement** |

---

# 🎯 Research Contributions

QualiAgent explores several aspects of AI-assisted software engineering:

### Multi-Agent Software Analysis

Specialized agents divide software-quality analysis into focused responsibilities rather than relying on a single general-purpose component.

### Evidence-Grounded Reasoning

Candidate findings contain concrete evidence that can be inspected before acceptance.

### Hybrid AI Architecture

The framework combines:

```text
Deterministic Static Analysis
          +
AST-Based Test Analysis
          +
Optional LLM Reasoning
          +
Evidence-Based Review
```

### Reproducible Evaluation

The benchmark generator produces a controlled and repeatable dataset for evaluating the framework.

### Human-in-the-Loop Validation

A stratified 600-item sample provides a mechanism for comparing automated findings against human judgments.

---

# 🚀 Future Work

Potential extensions include:

* Evaluation on real-world open-source repositories
* Additional test-smell detectors
* Advanced flaky-test detection
* Cross-file contextual reasoning
* Larger benchmark datasets
* LLM model comparison
* Human–AI agreement analysis
* CI/CD integration
* Automated pull-request test-quality feedback
* Test-quality visualization dashboards

---

## 📚 Research Documentation

Additional research methodology and experimental design are available in:

```text
docs/research_design.md
```

The document describes the research question, benchmark design, baselines, manual-validation strategy, and evaluation metrics.
