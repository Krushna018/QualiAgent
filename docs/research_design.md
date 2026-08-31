
# QualiAgent Research Design

## Research question
When does a specialized multi-agent workflow improve software-test quality analysis
relative to simpler rule-based and single-agent approaches?

## Four-agent workflow
1. **Repository Context Agent** — extracts repository/test context and metadata.
2. **Static Analysis Agent** — detects traceable code/test smells through explicit rules.
3. **Test Quality Agent** — reasons over assertions, test oracles, complexity, and structure.
4. **Reviewer Agent** — validates findings against evidence and rejects unsupported output.

The reviewer supports an OpenAI-compatible LLM endpoint when configured, while
retaining an offline deterministic mode so the project is reproducible without API access.

## Benchmark design
The included generator creates:
- **30 repositories**
- **50 tests per repository**
- exactly **1,500 benchmark test cases**
- 6 labeled software-test quality issue categories

The generated benchmark is for development/reproducibility. For a resume or research
application, claims about *open-source repositories* should only be made after replacing
or supplementing the generated benchmark with actual public repositories.

## Manual validation
The included sampling script creates a **600-item stratified review set**:
- 6 issue types
- 100 findings/examples per class

A human reviewer can fill in reviewer labels and notes. Do not claim a 600-finding
manual evaluation until the review is actually completed.

## Baselines
The architecture is intended to compare:
- rule-based detector
- optional single-agent LLM analysis
- four-agent evidence/reviewer workflow

## Metrics
Recommended:
- precision
- recall
- F1
- per-class performance
- agreement rate
- unsupported recommendation rate
- explanation/evidence consistency

Specific performance improvements should be reported only after running and reviewing
the corresponding experiment.
