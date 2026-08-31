# TuinBooks v60.8.3 Stability Staging — Agent QA Gate

**Target:** staging/test business only. Do not test destructive workflows in a live customer business.

## Release identification
- `app/VERSION-STAGING.txt` must read `60.8.3-stability-staging-agent-test`.
- Browser console: `window.__TUINBOOKS_STAGING_RELEASE__` should contain `60.8.3`.
- `document.documentElement.dataset.scheduleRenderer` should be `schedule-v2-60.8.3-staging` after opening Schedule.
- Run `window.__tuinbooksStagingDiagnosticsV6083.getReport()` and retain the output with the test report.

## P0 — startup / data authority
1. Cold login opens the correct business without showing a misleading empty workspace.
2. Reload three times. Client/team/schedule counts must not oscillate.
3. Navigate Schedule → Work → Clients → Billing → Schedule three times; no blank view and no unexpected jump back to Work.
4. Console must contain no `currentMonday is not defined`, `scheduleCell is not defined`, unhandled promise rejection, or startup ReferenceError.

## P0 — backup and import/export
5. **Export current business workbook** downloads a real file.
6. **Export business data** downloads a real file or shows a clear blocking error; silent no-op is FAIL.
7. In QA only, perform an Eden-sized replacement import. Verify preview counts before import.
8. Reload and log out/in. Imported clients, teams and visits must persist.
9. Export again after import and compare core counts with the pre-import/expected dataset.

## P0 — Schedule V2
10. Schedule opens directly with correct teams and correct selected-week counts.
11. Previous → Today → Next works and dates/counts change coherently.
12. Basket button opens/closes reliably in normal mode.
13. Rearrange mode shows the high-density Basket on the left (desktop) and at least ~20 names should be visible without excessive card height when enough items exist.
14. Rearrange selection count stays correct while selecting/deselecting multiple visits.
15. Drag a visit within the same day; save must persist after reload.
16. Drag between teams; save must persist after reload.
17. Drag calendar → Basket; item disappears from calendar and appears in Basket; reload must preserve.
18. Drag Basket → calendar; item returns with the selected team/date; reload must preserve.
19. Move multiple selected visits to Basket; all and only selected visits move.
20. For a recurring visit choose **This visit only**; future occurrences remain unchanged.
21. For a recurring visit choose **This & future visits**; past/completed visits remain unchanged and future dates/team follow the new pattern.
22. A failed network/cloud save must restore the previous schedule rather than leaving local/cloud disagreement.
23. Completed/cancelled/resolved visits must not become draggable mutable live appointments.

## P0 — Work/mobile consistency
24. Work today totals must agree with the same day's active Schedule jobs by team.
25. Team progress meter numerator/denominator and percentage must agree; specifically test a team with partial completion.
26. Mobile owner/field workflow: login/pair → route → job detail → note → photo → complete → refresh.
27. Test missed/not-serviced outcome and confirm office Work/Schedule sees the result.
28. Capture an opportunity/extra on mobile and confirm office can see it.
29. Mobile must not expose office-only Schedule editing controls.

## P1 — Billing / Clients / communications
30. Billing contains no `Invalid Date` in visible rows, document preview or due-date display.
31. Client search finds known clients quickly.
32. Edit a populated client text field; reload preserves it.
33. Clear an optional client text field; reload must keep it blank rather than restoring the previous value.
34. Quote/invoice preview opens. Use an internal QA recipient only for actual send tests.
35. WhatsApp reaches the final prepared-send handoff without sending automatically.
36. Email send (QA recipient only) succeeds or gives an explicit actionable error.

## P1 — visual/stability checks
37. TuinBooks logo is visible after cold load, reload and navigation.
38. No giant blank Schedule gutter, overlapping Basket, or top-clipping sticky Basket.
39. Desktop widths: 1366, 1536, 1920. Mobile widths: 390 and 430.
40. No horizontal page-level scrollbar in normal desktop Schedule; board-local scroll is acceptable on narrower screens.

## Final gate
Run **three complete loops**:
`Login → Schedule move → Work → Client edit → Billing → reload → logout/login → verify persistence`.

**PASS requires:**
- zero Critical/P0 failures;
- no unexplained console exceptions;
- persistence after reload and logout/login;
- no live customer communication/data changed;
- all temporary QA mutations restored or deliberately retained in the QA business.

Record every item as PASS / FAIL / NOT TESTED and attach console screenshots/details for any FAIL.
