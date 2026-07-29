(function () {
  const state = {
    modules: null,
    violations: null,
    benchmark: null,
    dispatch: null,
  };

  async function invokeAction(name, input) {
    if (globalThis.github?.copilot?.invokeAction) {
      return globalThis.github.copilot.invokeAction(name, input ?? {});
    }

    return {
      warning: "Canvas host action bridge not detected in this runtime.",
      action: name,
      input: input ?? {},
    };
  }

  function setActiveTab(tabName) {
    document.querySelectorAll(".tab").forEach((tab) => {
      tab.classList.toggle("is-active", tab.dataset.tab === tabName);
    });

    document.querySelectorAll(".panel").forEach((panel) => {
      panel.classList.toggle("is-hidden", panel.dataset.panel !== tabName);
    });
  }

  function renderModules() {
    const panel = document.querySelector('[data-panel="modules"]');
    const items = state.modules?.items ?? [];

    panel.innerHTML = `
      <div class="muted">${state.modules ? `${state.modules.totalItems} module entries` : "Loading modules..."}</div>
      <div class="grid">
        ${items
          .map(
            (module) => `
              <article class="card">
                <h3>${module.name}</h3>
                <p>${module.purpose}</p>
                <p class="muted">${(module.highlights ?? []).join(" | ")}</p>
              </article>
            `,
          )
          .join("")}
      </div>
    `;
  }

  function renderViolations() {
    const panel = document.querySelector('[data-panel="violations"]');
    const byFile = state.violations?.byFile ?? [];
    const total = state.violations?.totals?.total ?? 0;

    panel.innerHTML = `
      <p><strong>Total violations:</strong> ${total}</p>
      <div class="grid">
        ${byFile
          .map(
            (row) => `
              <article class="card">
                <h3>${row.file}</h3>
                <p>${row.type}</p>
                <p class="muted">Count: ${row.count}</p>
              </article>
            `,
          )
          .join("")}
      </div>
      <p class="muted">${state.violations?.notes ?? ""}</p>
    `;
  }

  function renderBenchmark() {
    const panel = document.querySelector('[data-panel="benchmark"]');

    panel.innerHTML = `
      <div class="controls">
        <button class="primary" id="run-benchmark">Run benchmark.py</button>
      </div>
      <pre>${escapeHtml(state.benchmark ? `${state.benchmark.stdout || ""}\n${state.benchmark.stderr || ""}` : "Run benchmark to view output.")}</pre>
    `;

    panel.querySelector("#run-benchmark")?.addEventListener("click", async () => {
      panel.querySelector("pre").textContent = "Running benchmark...";
      state.benchmark = await invokeAction("runBenchmark", {});
      renderBenchmark();
    });
  }

  function renderDispatch() {
    const panel = document.querySelector('[data-panel="dispatch"]');

    panel.innerHTML = `
      <div class="controls">
        <input id="requestType" value="TRACE" placeholder="requestType" />
        <input id="statusCode" value="500" placeholder="statusCode" />
        <input id="region" value="sa-east-1" placeholder="region" />
        <button class="primary" id="run-dispatch">Run dispatch demo</button>
      </div>
      <pre>${escapeHtml(state.dispatch ? `${state.dispatch.stdout || ""}\n${state.dispatch.stderr || ""}` : "Run dispatch demo to view output.")}</pre>
    `;

    panel.querySelector("#run-dispatch")?.addEventListener("click", async () => {
      const requestType = panel.querySelector("#requestType")?.value || "TRACE";
      const statusCode = Number(panel.querySelector("#statusCode")?.value || 500);
      const region = panel.querySelector("#region")?.value || "sa-east-1";

      panel.querySelector("pre").textContent = "Running dispatch demo...";
      state.dispatch = await invokeAction("runDispatchDemo", {
        requestType,
        statusCode,
        region,
      });
      renderDispatch();
    });
  }

  function escapeHtml(value) {
    return String(value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  async function loadInitialData() {
    state.modules = await invokeAction("listModules", { page: 1, pageSize: 10 });
    state.violations = await invokeAction("listViolations", {});

    renderModules();
    renderViolations();
    renderBenchmark();
    renderDispatch();
  }

  function wireTabs() {
    document.querySelectorAll(".tab").forEach((tab) => {
      tab.addEventListener("click", () => {
        setActiveTab(tab.dataset.tab);
      });
    });
  }

  function init() {
    wireTabs();
    setActiveTab("modules");
    loadInitialData().catch((error) => {
      const panel = document.querySelector('[data-panel="modules"]');
      if (panel) {
        panel.innerHTML = `<pre>${escapeHtml(String(error))}</pre>`;
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
})();
