#!/usr/bin/env python3
"""
Estimate the energy (Wh) and carbon (gCO2e) footprint of LLM inference from
token counts, following an SCI-style (ISO/IEC 21031) marginal-attribution model.

Feed it the token counts the Copilot CLI shows in `/usage` (cumulative billed
tokens already include the per-turn "re-billed context" compounding) or `/context`
(a single snapshot -- will undercount).

All factors are order-of-magnitude estimates and highly hardware/model dependent.
Results are reported as a low/mid/high RANGE on purpose. Do not present the mid
value as a precise figure.

Examples
--------
# From /usage cumulative counts:
python estimate_llm_carbon.py --input-tokens 9000 --output-tokens 50

# Attribute a single web_search (results linger 5 extra turns), clean grid:
python estimate_llm_carbon.py --input-tokens 1500 --output-tokens 50 \
    --persist-turns 5 --searches 1 --grid 50

# Model a cached context path (re-processed input billed at 0.2x):
python estimate_llm_carbon.py --input-tokens 1500 --persist-turns 5 --cache-factor 0.2
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass

# --- Per-token energy factors (Wh/token), compute-only. ---------------------
# Input (prefill) is batched/compute-bound -> cheap. Output (decode) does one
# forward pass per token -> ~10x costlier. Ranges span ~an order of magnitude.
INPUT_WH = {"low": 0.00005, "mid": 0.00015, "high": 0.0003}
OUTPUT_WH = {"low": 0.0005, "mid": 0.0015, "high": 0.003}

# Datacenter overhead (chip -> facility energy).
DEFAULT_PUE = 1.15

# External retrieval energy per web_search query (Wh). NOT captured by tokens:
# search-backend index serving + ranking. Wide uncertainty; network transfer of
# the ~tens-of-KB payload is negligible (<0.001 Wh) and folded in here.
RETRIEVAL_WH = {"low": 0.1, "mid": 0.2, "high": 0.3}

LEVELS = ("low", "mid", "high")


@dataclass
class Result:
    energy_wh: dict          # per level, facility-level Wh (incl. PUE + retrieval)
    inference_wh: dict       # per level, facility-level Wh (LLM only, incl. PUE)
    retrieval_wh: dict       # per level, external retrieval Wh
    carbon_g: dict           # per level, gCO2e


def estimate(
    input_tokens: float,
    output_tokens: float,
    persist_turns: int,
    searches: int,
    grid_gco2e_per_kwh: float,
    pue: float,
    cache_factor: float,
) -> Result:
    """Compute low/mid/high energy and carbon.

    persist_turns: extra turns the input tokens are re-processed while lingering
        in context (0 = first pass only). Re-processed tokens are weighted by
        cache_factor to model prompt/KV caching.
    """
    # Effective input tokens: first ingest (1x) + re-processed tail (cache_factor each).
    effective_input = input_tokens * (1.0 + persist_turns * cache_factor)

    inference_wh, retrieval_wh, energy_wh, carbon_g = {}, {}, {}, {}
    g_per_wh = grid_gco2e_per_kwh / 1000.0  # gCO2e per Wh

    for lvl in LEVELS:
        infer = (effective_input * INPUT_WH[lvl] + output_tokens * OUTPUT_WH[lvl]) * pue
        retr = searches * RETRIEVAL_WH[lvl]
        total = infer + retr
        inference_wh[lvl] = infer
        retrieval_wh[lvl] = retr
        energy_wh[lvl] = total
        carbon_g[lvl] = total * g_per_wh

    return Result(energy_wh, inference_wh, retrieval_wh, carbon_g)


def _fmt(v: float, unit: str) -> str:
    if v < 0.01:
        return f"{v:.4f} {unit}"
    if v < 1:
        return f"{v:.3f} {unit}"
    return f"{v:.2f} {unit}"


def main() -> None:
    p = argparse.ArgumentParser(
        description="Estimate LLM energy/carbon from token counts (SCI-style, ranged).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    p.add_argument("--input-tokens", type=float, required=True,
                   help="Input/prefill tokens (first ingest). From /usage or /context.")
    p.add_argument("--output-tokens", type=float, default=0.0,
                   help="Output/decode tokens the model generated.")
    p.add_argument("--persist-turns", type=int, default=0,
                   help="Extra turns input tokens are re-processed in context (0=first pass only).")
    p.add_argument("--cache-factor", type=float, default=1.0,
                   help="Weight for re-processed input tokens (1.0=no cache, ~0.1-0.3 if KV/prompt cached).")
    p.add_argument("--searches", type=int, default=0,
                   help="Number of external web_search queries to add retrieval energy for.")
    p.add_argument("--grid", type=float, default=480.0,
                   help="Grid carbon intensity in gCO2e/kWh (e.g. 480 global avg, 50 low-carbon).")
    p.add_argument("--pue", type=float, default=DEFAULT_PUE,
                   help="Datacenter Power Usage Effectiveness (chip->facility).")
    args = p.parse_args()

    r = estimate(
        input_tokens=args.input_tokens,
        output_tokens=args.output_tokens,
        persist_turns=args.persist_turns,
        searches=args.searches,
        grid_gco2e_per_kwh=args.grid,
        pue=args.pue,
        cache_factor=args.cache_factor,
    )

    eff_in = args.input_tokens * (1.0 + args.persist_turns * args.cache_factor)

    print("=" * 62)
    print("LLM inference energy/carbon estimate (SCI-style, order-of-mag)")
    print("=" * 62)
    print(f"Input tokens (first ingest) : {args.input_tokens:,.0f}")
    print(f"Persist turns / cache factor: {args.persist_turns} / {args.cache_factor}")
    print(f"Effective input tokens      : {eff_in:,.0f}")
    print(f"Output tokens               : {args.output_tokens:,.0f}")
    print(f"Web searches (retrieval)    : {args.searches}")
    print(f"Grid intensity              : {args.grid:g} gCO2e/kWh")
    print(f"PUE                         : {args.pue:g}")
    print("-" * 62)
    print(f"{'':14}{'low':>14}{'mid':>14}{'high':>14}")
    print(f"{'Inference Wh':14}" + "".join(f"{_fmt(r.inference_wh[l], 'Wh'):>14}" for l in LEVELS))
    if args.searches:
        print(f"{'Retrieval Wh':14}" + "".join(f"{_fmt(r.retrieval_wh[l], 'Wh'):>14}" for l in LEVELS))
    print(f"{'Total Wh':14}" + "".join(f"{_fmt(r.energy_wh[l], 'Wh'):>14}" for l in LEVELS))
    print(f"{'Carbon gCO2e':14}" + "".join(f"{_fmt(r.carbon_g[l], 'g'):>14}" for l in LEVELS))
    print("-" * 62)
    print(f"Headline: ~{_fmt(r.carbon_g['low'], 'gCO2e')} - "
          f"{_fmt(r.carbon_g['high'], 'gCO2e')} "
          f"(mid ~{_fmt(r.carbon_g['mid'], 'gCO2e')})")
    print("Note: factors are estimates spanning ~an order of magnitude.")
    print("      Retrieval energy is a separate, token-invisible boundary.")
    print("      Grid choice is the largest lever (global 480 vs clean ~50).")


if __name__ == "__main__":
    main()
