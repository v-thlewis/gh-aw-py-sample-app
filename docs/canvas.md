# Engineering Canvas — `v-thlewis/gh-aw-py-sample-app`

## Scope
This canvas summarizes architecture, runtime flow, quality/performance/security/testing hotspots, and a prioritized improvement plan for this repository.

---

## 1) Repository Canvas

### Top-level map
```text
/
├─ README.md
├─ request_handler.py
├─ traffic_router.py
├─ data_processor.py
├─ ml_pipeline.py
├─ benchmark.py
├─ .github/
└─ .vscode/
```

### Functional ownership
- **`request_handler.py`**: request lifecycle orchestration (parse/validate/dispatch/respond)
- **`traffic_router.py`**: routing and path-selection policy
- **`data_processor.py`**: preprocessing/transformation logic
- **`ml_pipeline.py`**: model/pipeline execution path
- **`benchmark.py`**: performance and regression benchmarking

---

## 2) Architecture & Runtime Flow Canvas

### End-to-end flow
```text
Client/Input
   ↓
request_handler.py
   ├─ Parse + validate input
   ├─ Decide route (direct or via traffic_router.py)
   ├─ Transform payload (data_processor.py)
   ├─ Execute pipeline/inference (ml_pipeline.py)
   └─ Build + return response
```

### Integration boundaries
- **API/edge boundary**: request validation and response shape
- **Routing boundary**: policy decisions and fallback behavior
- **Transform boundary**: deterministic data contracts
- **Pipeline boundary**: compute-heavy execution and latency control
- **Observability boundary**: benchmark metrics and stage timings

### Architectural risks
- `request_handler.py` may become a multi-concern hotspot (orchestration + policy + transform coupling).
- Module interfaces likely rely on implicit dict contracts (drift risk).
- Benchmark representativeness may diverge from production-like request mixes.

---

## 3) Code Quality Canvas

### Hotspots (likely)
1. Long/mixed-responsibility functions in request handling.
2. Implicit interfaces between modules (untyped payload contracts).
3. Inconsistent error handling semantics across routing/processing/pipeline.
4. Repeated logic across request paths.

### Quality actions
- Introduce typed request/response contracts (e.g., dataclasses/typed models).
- Refactor request handling into explicit stages:
  - `parse_input`
  - `validate_input`
  - `resolve_route`
  - `execute_path`
  - `serialize_response`
- Establish one shared error model:
  - `error_code`
  - `message`
  - `retryable`
  - `context`

---

## 4) Performance & Efficiency Canvas

### Potential bottlenecks
1. Copy-heavy transforms in `data_processor.py`.
2. Repeated per-request setup in `ml_pipeline.py`.
3. Branching overhead / repeated predicate evaluation in `traffic_router.py`.
4. Multi-pass serialization in `request_handler.py`.

### Measurement model
Capture per-request stage timings:
- `t_parse_validate`
- `t_route`
- `t_process`
- `t_pipeline`
- `t_serialize`
- `t_total`

Track:
- p50 / p95 / p99 latency
- throughput
- error rate
- timeout rate

### Optimization actions
- Cache immutable artifacts (e.g., feature metadata, model descriptors).
- Minimize intermediate copies in transformation steps.
- Reduce repeated conditional checks in hot routing paths.
- Align benchmark scenarios with realistic input distributions.

---

## 5) Reliability Canvas

### Failure-mode risks
- Incomplete guardrails for malformed/partial input payloads.
- Non-uniform timeout/retry policy.
- Undefined fallback when route confidence/eligibility is unclear.
- Error classes not normalized across modules.

### Reliability actions
- Enforce schema validation at request boundary (fail closed).
- Define global request deadline with per-stage budgets.
- Add deterministic fallback policy + reason tagging.
- Standardize exception-to-response mapping.

---

## 6) Security Canvas

### Primary checks
- Input trust boundaries in `request_handler.py`.
- Dangerous execution primitives (`eval`, `exec`, shell subprocess usage).
- Sensitive values in logs and exception traces.
- Config/secret handling discipline.

### Security actions
- Centralized redaction/sanitization for logs.
- Explicit allow-lists for critical input fields where possible.
- CI static checks for unsafe API usage and secret patterns.
- Ensure errors do not leak sensitive internals in responses.

---

## 7) Testing Canvas

### Recommended test pyramid
- **Unit tests**
  - `traffic_router.py`: route matrix, edge conditions
  - `data_processor.py`: deterministic transforms, null/missing fields
  - `ml_pipeline.py`: behavior under sparse/invalid feature sets
- **Contract tests**
  - module-to-module input/output schema compatibility
- **Integration tests**
  - full request flow through `request_handler.py`
- **Performance tests**
  - `benchmark.py` thresholds as regression gates

### High-value missing tests (priority)
1. Router ambiguity and fallback determinism.
2. Processor idempotency and stability.
3. Pipeline behavior under invalid/missing features.
4. End-to-end negative paths (timeouts, invalid payloads, internal exceptions).

---

## 8) Operations Canvas

### Operational baseline
- Single source of truth for env vars and defaults.
- Structured logging with request/correlation IDs.
- Clear local run + benchmark + test commands in README.
- Optional health/readiness signals if service-like runtime is expected.

### Observability baseline
- Metrics: latency percentiles, success/error counts, fallback counts.
- Tracing/timing markers across handler/router/processor/pipeline.
- Benchmark trend tracking over time (not just point-in-time runs).

---

## 9) Prioritized Action Board

### P0 — Immediate (highest ROI)
1. Add stage-level timing + structured logs in request path.
2. Enforce strict request schema validation at ingress.
3. Normalize error model and fallback semantics.

### P1 — Near-term
4. Refactor `request_handler.py` into explicit orchestration stages.
5. Add contract tests across router/processor/pipeline boundaries.
6. Convert benchmark checks into CI pass/fail thresholds.

### P2 — Medium-term
7. Optimize data transform allocations and cache immutable pipeline artifacts.
8. Add security static checks for unsafe APIs and secret leakage patterns.
9. Keep this canvas current via PR checklist item (`docs/canvas.md updated`).

---

## 10) Definition of Done (for hardening milestone)

- [ ] Stage timings emitted and visible in benchmark/test output
- [ ] Input schema validation enforced before business logic
- [ ] Unified error envelope used by all failure paths
- [ ] Contract + integration tests covering critical flow and failures
- [ ] Benchmark thresholds enforced in CI
- [ ] Security redaction and static checks active
- [ ] `README.md` updated with run/test/benchmark instructions
- [ ] This canvas reviewed and updated post-refactor

---

## 11) Suggested PR sequence

1. **PR A**: observability + error envelope + validation scaffolding  
2. **PR B**: request handler staged refactor  
3. **PR C**: contract/integration test expansion  
4. **PR D**: benchmark CI thresholds + perf optimizations  
5. **PR E**: security hardening + docs finalization
