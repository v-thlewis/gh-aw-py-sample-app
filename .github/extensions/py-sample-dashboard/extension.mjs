import { spawn } from "node:child_process";
import { readFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { createCanvas } from "@github/copilot-canvas";

const __dirname = dirname(fileURLToPath(import.meta.url));
const REPO_ROOT = resolve(__dirname, "..", "..", "..");
const README_PATH = join(REPO_ROOT, "README.md");

const MODULES = [
  {
    name: "request_handler.py",
    purpose: "HTTP-style request branching examples",
    highlights: ["if-else switch chains", "event processing"],
  },
  {
    name: "traffic_router.py",
    purpose: "Region routing decision tree examples",
    highlights: ["if-else switch chain", "short-chain control"],
  },
  {
    name: "data_processor.py",
    purpose: "Data processing and cloud utility examples",
    highlights: ["lazy import opportunities", "analytics helpers"],
  },
  {
    name: "ml_pipeline.py",
    purpose: "ML pipeline with heavy dependency usage",
    highlights: ["lazy import opportunities", "GPU helper"],
  },
  {
    name: "benchmark.py",
    purpose: "Wall-clock and memory benchmark harness",
    highlights: ["import-time benchmark", "dispatch benchmark"],
  },
];

function normalizePositiveInt(value, fallback) {
  const n = Number(value);
  if (!Number.isFinite(n)) {
    return fallback;
  }
  const rounded = Math.floor(n);
  return rounded > 0 ? rounded : fallback;
}

function paginate(items, pageInput, pageSizeInput) {
  const pageSize = normalizePositiveInt(pageSizeInput, 10);
  const page = normalizePositiveInt(pageInput, 1);

  const totalItems = items.length;
  const totalPages = Math.max(1, Math.ceil(totalItems / pageSize));
  const safePage = Math.min(page, totalPages);
  const start = (safePage - 1) * pageSize;
  const end = start + pageSize;

  return {
    items: items.slice(start, end),
    page: safePage,
    pageSize,
    totalItems,
    totalPages,
    hasNextPage: safePage < totalPages,
    hasPreviousPage: safePage > 1,
  };
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function renderSafeMarkdown(markdown) {
  let html = escapeHtml(markdown);
  html = html.replace(/`([^`]+)`/g, "<code>$1</code>");
  html = html.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");
  html = html.replace(/\n/g, "<br>");
  return html;
}

function runPython(args, timeoutMs = 30_000) {
  return new Promise((resolvePromise) => {
    const child = spawn("python3", args, {
      cwd: REPO_ROOT,
      env: process.env,
    });

    let stdout = "";
    let stderr = "";

    const timer = setTimeout(() => {
      child.kill("SIGTERM");
      resolvePromise({
        ok: false,
        exitCode: -1,
        command: `python3 ${args.join(" ")}`,
        stdout,
        stderr: `${stderr}\nCommand timed out after ${timeoutMs} ms.`.trim(),
      });
    }, timeoutMs);

    child.stdout.on("data", (chunk) => {
      stdout += String(chunk);
    });

    child.stderr.on("data", (chunk) => {
      stderr += String(chunk);
    });

    child.on("close", (code) => {
      clearTimeout(timer);
      resolvePromise({
        ok: code === 0,
        exitCode: code ?? -1,
        command: `python3 ${args.join(" ")}`,
        stdout,
        stderr,
      });
    });
  });
}

function parseReadmeViolations(readme) {
  const lines = readme.split(/\r?\n/);
  const violations = [];
  let currentFile = "";

  for (const line of lines) {
    const fileHeader = line.match(/^###\s+`([^`]+)`/);
    if (fileHeader) {
      currentFile = fileHeader[1];
      continue;
    }

    const violationLine = line.match(/^\-\s+\*\*([^*]+)\*\*:\s+(\d+)\s+violations?/i);
    if (violationLine && currentFile) {
      violations.push({
        file: currentFile,
        type: violationLine[1].trim(),
        count: Number(violationLine[2]),
      });
    }
  }

  return violations;
}

async function listViolations() {
  const readme = await readFile(README_PATH, "utf8");
  const byFile = parseReadmeViolations(readme);

  const totals = byFile.reduce(
    (acc, row) => {
      acc.total += row.count;
      const key = row.type.toLowerCase();
      acc.byType[key] = (acc.byType[key] ?? 0) + row.count;
      return acc;
    },
    { total: 0, byType: {} },
  );

  return {
    byFile,
    totals,
    notes: "Source: repository README violation summary.",
  };
}

async function inspectLazyImports() {
  const targets = ["ml_pipeline.py", "data_processor.py"];
  const report = [];

  for (const relativePath of targets) {
    const fullPath = join(REPO_ROOT, relativePath);
    const content = await readFile(fullPath, "utf8");
    const lines = content.split(/\r?\n/);

    const topLevelImports = lines
      .filter((line) => /^(import\s+|from\s+\S+\s+import\s+)/.test(line.trim()))
      .map((line) => line.trim());

    report.push({
      file: relativePath,
      topLevelImports,
      importCount: topLevelImports.length,
    });
  }

  return {
    files: report,
    hint: "Top-level imports here are useful candidates for lazy loading reviews.",
  };
}

async function runDispatchDemo(input = {}) {
  const requestType = String(input.requestType ?? "TRACE");
  const statusCode = Number(input.statusCode ?? 500);
  const region = String(input.region ?? "sa-east-1");

  const snippet = [
    "import json",
    "import request_handler as rh",
    "import traffic_router as tr",
    "payload = {",
    `  'requestType': '${requestType}',`,
    `  'statusCode': ${Number.isFinite(statusCode) ? statusCode : 500},`,
    `  'region': '${region}',`,
    "  'requestResult': rh.process_request_type('" + requestType + "'),",
    "  'statusMessage': rh.get_status_message(" + (Number.isFinite(statusCode) ? statusCode : 500) + "),",
    "  'route': tr.route_traffic('" + region + "')",
    "}",
    "print(json.dumps(payload, indent=2))",
  ].join("\n");

  return runPython(["-c", snippet], 10_000);
}

async function renderDashboardUrl() {
  const htmlPath = join(__dirname, "web", "index.html");
  const cssPath = join(__dirname, "web", "styles.css");
  const appPath = join(__dirname, "web", "app.js");

  const [htmlTemplate, cssBundle, appBundle] = await Promise.all([
    readFile(htmlPath, "utf8"),
    readFile(cssPath, "utf8"),
    readFile(appPath, "utf8"),
  ]);

  const html = htmlTemplate
    .replace("/*__APP_CSS__*/", cssBundle)
    .replace("/*__APP_JS__*/", appBundle);

  return `data:text/html;charset=utf-8,${encodeURIComponent(html)}`;
}

createCanvas({
  id: "py-sample-dashboard",
  title: "Python Sample App Dashboard",
  render: async () => ({
    url: await renderDashboardUrl(),
  }),
  actions: [
    {
      name: "listModules",
      description: "List known sample modules with paging metadata.",
      handler: async (ctx) => {
        const page = Number(ctx.input?.page ?? 1);
        const pageSize = Number(ctx.input?.pageSize ?? 10);
        return paginate(MODULES, page, pageSize);
      },
    },
    {
      name: "listViolations",
      description: "Read violation counts from README.md.",
      handler: async () => listViolations(),
    },
    {
      name: "runBenchmark",
      description: "Run benchmark.py and return stdout/stderr.",
      handler: async () => runPython(["benchmark.py"], 60_000),
    },
    {
      name: "runDispatchDemo",
      description: "Execute request/route demo calls through Python modules.",
      handler: async (ctx) => runDispatchDemo(ctx.input ?? {}),
    },
    {
      name: "inspectLazyImports",
      description: "Summarize top-level imports in heavy Python modules.",
      handler: async () => inspectLazyImports(),
    },
    {
      name: "renderStepSummary",
      description: "Render constrained markdown to safe HTML.",
      handler: async (ctx) => ({
        html: renderSafeMarkdown(String(ctx.input?.markdown ?? "")),
      }),
    },
  ],
});
