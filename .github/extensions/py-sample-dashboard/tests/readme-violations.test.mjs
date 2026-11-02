import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import { parseReadmeViolations } from "../readme-violations.mjs";

test("parses the per-file violations from the repository README", async () => {
  const readme = await readFile(new URL("../../../../README.md", import.meta.url), "utf8");

  assert.deepEqual(parseReadmeViolations(readme), [
    { file: "ml_pipeline.py", type: "Lazy Import Violations", count: 4 },
    { file: "data_processor.py", type: "Lazy Import Violations", count: 4 },
    { file: "request_handler.py", type: "If-Else Switch Violations", count: 5 },
    { file: "traffic_router.py", type: "If-Else Switch Violations", count: 1 },
  ]);
});

test("excludes summaries and unrelated sections while retaining nested details", () => {
  const readme = [
    "# Project",
    "## Test Files",
    "### `first.py`",
    "- **Lazy Import Violations**: 2 violations",
    "#### Details",
    "- **Additional Violations**: 1 violation",
    "## Total Violations",
    "- **Total**: 3 violations",
    "### Notes",
    "- **Noise**: 100 violations",
    "### `second.py`",
    "- **If-Else Switch Violations**: 4 violations",
  ].join("\n");

  assert.deepEqual(parseReadmeViolations(readme), [
    { file: "first.py", type: "Lazy Import Violations", count: 2 },
    { file: "first.py", type: "Additional Violations", count: 1 },
    { file: "second.py", type: "If-Else Switch Violations", count: 4 },
  ]);
});
