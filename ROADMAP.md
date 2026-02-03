# ROADMAP

Backlog for features, improvements, research, fixes, etc. 

### Documentation

- Add some of the documentation currently in the readme to the spreadsheet as well. The spreadsheet should, in general, be self-contained.

### Features

- Charts dashboard (cross‑platform‑safe)
     - Summary: Add a small dashboard with line/column charts that work in Excel, Numbers, and Google Sheets. Focus on balance over time, contributions vs expenses, and percent_funded trend using simple chart types and fixed ranges.
    - Effort: medium
    - Impact: high
    - Rationale: Big visual payoff without sacrificing compatibility.
- Cash‑flow warnings (liquidity risk flags)
    - Summary: Flags years where beginning balance + contributions + interest are less than scheduled expenses. It uses existing Forecast data and highlights
    near‑term cash shortfalls.
    - Effort: low
    - Impact: high
    - Rationale: Quick to implement and immediately actionable for boards.
- Scenario comparison sheet
    - Summary: A side‑by‑side view of multiple contribution scenarios (min balance, ending balance, percent funded, worst coverage). It speeds up
    decision‑making.
    - Effort: low‑medium
    - Impact: high
    - Rationale: High value for planning with modest development complexity.
- Component grouping + category subtotals
    - Summary: Adds category roll‑ups to show where costs concentrate and how funding targets break down by category. Helps non‑technical readers.
    - Effort: medium
    - Impact: high
    - Rationale: Improves clarity without changing core math.
- Reserve deficit planning (required contribution)
    - Summary: Solves for an annual contribution level to reach a target funding level by a specified year. Useful for dues planning.
    - Effort: medium
    - Impact: medium‑high
    - Rationale: High value but requires iterative calculation.
- Sensitivity toggles (stress rates)
    - Summary: Lets users apply alternate inflation/interest assumptions to see downside risk without new scenarios.
    - Effort: medium‑high
    - Impact: medium
    - Rationale: Good risk insight, more complexity in inputs and outputs.
- Export summary report (PDF/CSV)
    - Summary: Generates a concise shareable report with key metrics and top expenses.
    - Effort: medium
    - Impact: medium
    - Rationale: Improves communication but doesn’t affect planning math.

### Research

* Test with Excel on Windows (don't currently have access to this platform)

### Bugs

* In the spreadsheet, the contributions column is in a different color. It probably shouldn't be.  Or maybe it should.



