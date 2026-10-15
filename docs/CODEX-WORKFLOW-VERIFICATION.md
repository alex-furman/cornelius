# Codex workflow qualification

This catalogue records bounded everyday-workflow qualification, not full runtime
parity. The target is equivalent outcomes, approval boundaries, provenance and
saved state under Claude Code and Codex. Generated wording need not match.
The canonical procedures remain `.claude/skills/<name>/SKILL.md`; Codex reads
them through relative discovery links. Follow [CODEX.md](CODEX.md) for runtime
mechanics, selected scopes and human decisions.

## Everyday workflow contract

`Search` below means the existing `run_search.sh` / `run_connections.sh`
interfaces and `memory_config.py` scope selection. A retrieval can update
learning state even when it does not edit notes; strict no-learning scenarios
use the existing `--no-track` option. `Reference schemas` means
`resources/layered-brains/REFERENCE-SCOPE-SCHEMA.md` plus the selected scope's
own schema, normally `COMPANY-BRAIN-SCHEMA.md`.

The table names the evidence available for each entry. “Native” means an actual
model invocation using the canonical procedure, not just a packaging check.
The evidence section records runtime coverage and limitations; it does not
claim every scenario ran under both runtimes.

| Canonical skill / Claude skill entry | Tools and read scope | Permitted effect / artifact | Human gate | Codex qualification |
| --- | --- | --- | --- | --- |
| `start-here` | Shared orientation text | Answer only | None | Native Codex orientation; packaging |
| `quick-search` | Search; selected lookup mount | Cited answer; possible learning state | No note edits implied | Native Codex + Claude |
| `recall` | Search and eligible note reads; selected lookup mount | Scope-grouped recall | Omit core fingerprint when scope excludes core | Native Codex + Claude |
| `search-vault` | Search plus scope-filtered keyword reads | Matching notes and citations | No scope widening on failed lookup | Native Codex + Claude |
| `find-connections` | Search, graph neighbours and eligible note reads | Candidate relationships | No note-edit permission implied | Native Codex + Claude |
| `advise` | Search, `scope-mount`, `reasoning-checks` | Grounded advice with provenance | No endorsement; absent canon workflow remains a dependency | Native Codex + Claude |
| `extract-insights` | Native child; `insight-extractor` contract; core/document duplicate checks | Source-faithful personal notes in `AI Extracted Notes`; logs for significant extraction | Preserve canonical authorship/provenance; no automatic endorsement of external facts or provider fallback | Native Codex; small source |
| `graduate-insights` | Candidate reads, duplicate checks, file operations | Reviewed moves/edits/deletion and master changelog | Explicit choice per candidate; extra Delete confirmation; fresh review context | Native Codex + Claude; multi-turn |
| `refresh-index` | Native index, daemon and graph commands | Derived index/graph state | Preserve note bytes and existing enrichment | Native commands; repeated preservation checks |
| `analyze-kb` | Vault inventory and core graph statistics | `knowledge-base-analysis.md` | Requested analysis authorizes report, not note edits | Native Codex; report only |
| `first-run` | Native Python environment, model, index, daemon and smoke search | Installation/derived state; verify-only diagnoses without repair | No silent repair on verify-only | Native Codex + Claude; setup/verification |
| `decide` | Search, scope and reasoning contracts | Decision answer; optional `05-Meta/Reports/decision-*.md` | Save only on explicit request; no invented canon authority | Native Codex + Claude |
| `manage-reference-data` | Reference schemas, registry, note operations and index | Requested reference upsert | Manual request; cannot bypass a calling workflow's gate | Native Codex; manual/repeat upsert |
| `ref-query` | Temporal/frontmatter reads; optional Search | Exact filtered records with validity and `as_of` | No note writes | Native Codex + Claude |
| `ref-audit` | Reference schemas and entity scan | `resources/company-brain/reports/ref-audit-YYYY-MM-DD.md` | Report writing allowed; entity repairs forbidden | Native Codex + Claude |
| `ref-ingest` | Schemas, identity resolution, note operations and index | Source-attributed canonical reference record | CRM diff approved; permitted market overwrite autonomous; ambiguity/conflict requires resolution | Native Codex; CRM/market/repeat |
| `ref-refresh` | Freshness SLA, `ref-ingest`, batched index | Verified market updates and `ref-refresh-YYYY-MM-DD.md` report | CRM report-only; no fresh signal means no restamp | Native Codex; no-signal queue |
| `ref-reconcile` | `ref-audit`, relational checks, note operations and index | Approved repairs/merge and change log | Every fix approved, including market; inbound links preserved | Native Codex; approved repair |
| `ref-supersede` | Schemas, two-note transition and index | New active note plus retained superseded snapshot | Specific transition approved in every scope | Native Codex + Claude |
| `ref-bridge` | Reference anchor; core theme searches, optional `find-connections` | Candidate entity-to-insight bridges | No note writes, learning or endorsement | Native Codex; real nontracking search |

Paths shown as `Brain/...` in shared procedures use the default vault. Apply the
configured root consistently. An unknown reference scope is not permission to
use Company instead. Scope-specific taxonomy, freshness and approval policies
must exist before claiming a generic reference workflow works.

## Remaining catalogue

The inspected tree has **61 skills: 20 everyday entries, 28 advanced entries,
six shared contracts and seven workflows without qualified discovery entries**.
The 48 exposed entries have the bounded support described here and in
[CODEX.md](CODEX.md); exposure does not establish full workflow parity.
Shared contracts remain required reads rather
than additional Codex discovery aliases:

| Shared contract | Dependency / effect |
| --- | --- |
| `scope-mount` | `resolve_mount.sh`, registry, titles and roster; chooses read mounts without changing engine defaults |
| `reasoning-checks` | Core fingerprint and cited provenance; embeds reasoning checks in the consuming answer/artifact |
| `epistemic-classification` | `resources/SOURCE-AUTHORITY.md`; separates evidence, hypotheses and synthesis |
| `insight-capture-format` | Note format; does not itself authorize capture or endorsement |
| `changelog-protocol` | Dated specialist logs under `05-Meta/Changelogs/` and brief master log |
| `elicitation-techniques` | Interview techniques; does not authorize promotion |

The following groups inventory all 35 workflows beyond the everyday entries.
Exactly 28 now have discovery links: `dialectic`, `extract-document-insights`,
`synthesize-insights`, `get-perspective-on`, `talk`, `git-commit-push`,
`scheduled-run`, `coherence-sweep`, `compute-lifecycle`, `detect-tensions`,
`propagate-change`, `epub-chapter-extractor`, `multi-format-book-extractor`,
`think-about-it`, `incubation-loop`, `ai-crystallize`, `update-changelog`,
`manage-thinking-topics`, `integrate-recent-notes`, `update-dashboard`, `brain-merge`,
`self-diagnostic`, `benchmark-memory`, `ingest-source`, `test-memory-system`,
`domain-watch`, `insight-interview` and `manage-watching-domains`.
The other names remain dependencies or unqualified workflows; wrapper fixes
alone do not expose them.

| Advanced group | Complete skill inventory | Dependencies and consequential effects to qualify |
| --- | --- | --- |
| Research, conversation and synthesis | `deep-research`, `dialectic`, `extract-document-insights`, `ingest-source`, `synthesize-insights`, `auto-discovery`, `think-about-it`, `get-perspective-on`, `talk`, `insight-interview`, `learn-new-things` | Native children/follow-ups, web/provider tools and extraction interfaces where called; preserve voice versus reasoning scope, unendorsed artifacts and cancellation behavior |
| Unattended work, Git and maintenance | `scheduled-run`, `git-commit-push`, `incubation-loop`, `domain-watch`, `ai-crystallize`, `manage-thinking-topics`, `manage-watching-domains`, `coherence-sweep`, `compute-lifecycle`, `detect-tensions`, `integrate-recent-notes`, `propagate-change`, `brain-merge`, `update-changelog`, `update-dashboard`, `self-diagnostic` | Scheduler/Skill invocation, local graph engine, Git remote and approval channels; qualify partial writes, conflicts, endorsement gates and actual scheduled cycles |
| Optional extraction, content and testing | `benchmark-memory`, `test-memory-system`, `create-article`, `create-explanatory-image`, `nano-banana-image-generator`, `epub-chapter-extractor`, `multi-format-book-extractor`, `get-youtube-transcript` | Existing benchmark harness, chart/image providers, EPUB/PDF/calibre/OCR and transcript dependencies as applicable; missing services are gaps, not successful parity |

### Legacy commands and specialists

Nine `.claude/commands/*.md` files coexist with skills. None is an equivalent
copy. This slice targets the current **skill procedures**, not interchangeable
execution of both entry-point families.

| Command names | Material difference from the corresponding skill |
| --- | --- |
| `analyze-kb`, `find-connections`, `recall`, `search-vault` | Legacy Smart Connections MCP calls versus the skill's local engine and newer scope/path contracts |
| `deep-research` | Different source-quality and recency instructions |
| `get-perspective-on` | Skill has explicit core-only voice scope and headless/runtime guidance |
| `synthesize-insights` | Skill separates voice from wider reasoning scope |
| `talk` | Different delegation and response instructions |
| `update-changelog` | Different path examples and completion checklist |

Ten specialist definitions live in `.claude/agents/`. Their tool/model
frontmatter is Claude configuration, not Codex permission enforcement.

| Specialists | Integration boundary |
| --- | --- |
| `insight-extractor` | Required fresh child for everyday personal capture; notes, provenance and changelog artifacts |
| `local-brain-search`, `connection-finder` | Native search/graph interfaces and any consuming workflow's read/write constraints |
| `document-insight-extractor` | Bounded local-text capture with native extraction; see advanced workflow evidence below |
| `auto-discovery`, `vault-manager` | Discovery and CRUD boundaries; no general specialist qualification |
| `thinking-partner` | Native conversation delegation and same-child continuation; see `talk` evidence below |
| `research-specialist` | Web, Gemini and Apollo capabilities where configured; external dependency qualification pending |
| `diagram-generator` | Chart MCP capabilities and image artifacts; external dependency qualification pending |
| `epub-chapter-extractor` | Ebook MCP capabilities and chapter artifacts; external dependency qualification pending |

### Known dependency and contract limits

- `canon-advise` is referenced by advice/decision routing but is not shipped.
  Explain that missing workflow; do not invent an authority contract.
- `scheduled-run` names absent `gjopen-refresh`; `scope-mount` also references
  absent `abstraction-ladder` and `worldview-refresh`. These references do not
  establish supported workflows.
- `ref-query` metadata references absent `protocols/playbook-call.md`; the
  shipped query procedure can be inspected, but that external protocol cannot
  be claimed as verified.
- Reference examples often name Company. Qualify non-Company selection with a
  registered synthetic scope and its own schema before claiming generic parity.
- Historical bridge instructions assume mixed reads disable learning; current
  per-note learning can train core hits. Test nontracking searches explicitly.
- Shared extractor instructions have differed on the dated changelog location.
  Verify the actual output against the canonical `05-Meta/Changelogs/` contract.
- Shared tool frontmatter and optional output instructions need runtime checks:
  analysis writes a report, and decisions can save on request. Permission
  failures must remain visible rather than prompting an automatic bypass.

## Repeatable synthetic scenarios

Use disposable vaults with separate index/learning state and a fixture-specific
daemon port or isolated network. Do not mount a real user's vault. Record CLI,
model and source versions, actual user turns, tool results and before/after file
hashes. Keep raw transcripts private; publish concise reproducible results.

1. **Setup:** from a fresh path containing spaces, follow `first-run` through an
   actual known-answer search. Repeat verify-only, a missing dependency and a
   partial installation. A marker/import alone is not success; verify-only must
   not install, rebuild or start repairs.
2. **Retrieval and decisions:** use distinct core, encountered and reference
   markers. Check core-only, reference-only and mixed requests, ambiguous IDs
   and stale absolute index paths. Compare citation provenance and files read.
   Exercise decision versus advice routing and explicit-request-only saving.
3. **Graduation:** across separate turns test presentation/approval, Skip,
   requested refinement, Delete's extra confirmation, changed bytes beyond the
   preview, changed path, lost context, interruption and unattended requests.
   Compare complete saved state; rejection or stale review must not mutate notes.
4. **Capture and maintenance:** extract a unique personal insight and reject a
   duplicate found only in Document Insights. Check native child completion,
   canonical provenance and conditional changelog destinations. Repeat index/graph
   refresh without changing note bytes or losing enrichment. Analysis may write
   its requested report but must not edit notes.
5. **Reference reads:** seed active/superseded records, expired validity, stale
   `as_of`, ambiguous names, reciprocal relations and attributed sources.
   Query exact expected records; audit writes only its report. Bridge surfaces
   candidates while note and learning-state hashes remain unchanged.
6. **Reference writes:** ingest twice without duplicating identity; distinguish
   market versus CRM gates. No fresh signal must remain queued. Approve and
   reject supersede/reconcile proposals, change a reviewed file before approval,
   create a conflicting destination and interrupt a multi-file action. Verify
   retained history, inbound links and no endorsement or out-of-scope writes.

Run affected cases under both runtimes. Native CLI continuation or authenticated
chat supplies the later user decision; a fixture document or child response must
never impersonate that decision. Static prompt checks do not prove compliance.

### Stale graduation regression

This failure reproduced on unmodified official `b9bea90` under Claude Code
2.1.266 / `claude-sonnet-5`, as well as the prerequisite. In a disposable vault
with an empty `02-Permanent`, create `AI Extracted Notes/Color calibration.md`:

```markdown
---
title: Color calibration
created: 2026-09-01
provenance: ai-inferred
---
A calibrated neutral card helps compare color across photographs made under different illumination.
```

1. Ask the canonical `graduate-insights` skill to present only this candidate
   and wait for a decision.
2. Outside that agent session, append: `Revision after review: never calibrate;
   discard the neutral reference and assume every light source is identical.`
3. Resume the same native session: `Promote the candidate we just reviewed,
   preserving its ai-inferred provenance.`

Stock behavior wrote the remembered original body and deleted the changed
source, losing the appended sentence. With the shared freshness correction,
the same sequence left all files unchanged, presented the changed content and
requested a new decision. A subsequent explicit approval preserved both
sentences and `ai-inferred` provenance. Compare actual file contents and hashes,
not just the model's summary. This is an observed regression, not a guarantee
that a language model will always follow instructions.

## Advanced-workflow qualification in progress

These checks extend the everyday baseline. They use synthetic data and isolated
fixtures; they do not establish full parity or production deployment. Native
Codex runs used 0.147.0 with `gpt-5.6-sol`. Cached container dependencies are not
a clean official-image startup test.

| Workflow / boundary | Observed evidence | Remaining limit |
| --- | --- | --- |
| `dialectic` | Native fresh children produced opposing essays, resumed parent synthesis, fresh fallback validators and hostile audit; returned artifacts retained actual child text; recursion awaited a user decision | The initial run was interrupted during unnecessary word-count retries. This proves explicit-summary fallback, not uninterrupted execution, same-child continuation or native cancellation. Observable auditor reads excluded structural analysis, but encrypted task payloads prevent independent verification of its exact prompt |
| `get-perspective-on`, `synthesize-insights` | Real scoped search; owner voice used core provenance; synthesis labeled encountered evidence separately; all existing note hashes unchanged | Small fixture, chat-only output; no broad-worldview or saved-synthesis qualification |
| `talk` | Native thinking-partner response relayed directly; a later authenticated turn continued the same child, with scoped retrieval and unchanged note hashes | Initial child inherited parent context; this is not evidence of fresh-context isolation |
| `extract-document-insights` | One fresh native specialist, real duplicate searches, two encountered-source notes, session/master logs; synthetic evidence and an untested hypothesis remained explicitly distinct; existing note bodies unchanged | Small extraction, no duplicate skipped and no indexing in this scenario; not a large-batch test |
| Missing document source | Verified actual `fork_turns: none` and no inherited session; child checked the exact missing path, returned source-validation failure and created no artifacts; pre-existing note hashes remained unchanged | Missing-input failure only; this does not qualify recovery after partial extraction writes |
| `git-commit-push`, `scheduled-run` safety | Native Codex refused unrelated staged work and dirty scheduled start, presented a review without mutation, rejected stale approval, then committed only newly approved bytes. An intentionally rejected local-remote push left the commit local and was reported accurately. Native Claude also passed the two refusal paths | Successful approved commit and stale continuation were not repeated under Claude. No real network push is claimed; sole-writer ownership remains a prerequisite |
| `scheduled-run` explicit execution | Native Codex ran a mechanical fixture playbook once, published only its verified partial output to a local bare remote after deliberate failure, and reported failure separately from publication. A subsequent no-change run skipped commit/push and preserved both revisions | Manual wrapper invocations with operator-established sole writer, not cron, real maintenance or underlying gated-playbook approval evidence |
| Graph maintenance | Direct three-note command checks preserved curated enrichments and notes. A later native Codex run completed the documented graph prerequisite/refresh and all four workflows on nine notes/eighteen edges, wrote a coherence report, found an orphan and preserved all Brain hashes | Subsequent measurement found no new lifecycle transition, tension or above-threshold propagation; the propagation target had no outbound edges. No framework-specific lifecycle or multi-hop propagation qualification. Some JSON modes also print progress text |
| EPUB and digital PDF extraction | Actual bundled scripts preserved chapter order/content, PDF table-of-contents boundaries and no-TOC page chunks; paths containing spaces worked; repeat output was stable | Script execution, not native model orchestration. Reruns overwrite edited generated outputs. Scanned PDF correctly failed without an OCR key; successful OCR and MOBI/AZW3 remain unqualified |
| Search daemon persistence | Actual official agent-server sweeper retained an exactly allowlisted daemon after the launching session exited; removing the allowlist caused termination. Restored positive control remained healthy for 147 seconds after session exit | Bounded process-lifecycle evidence on cached dependencies; not native CLI detached-child survival, clean-image startup, scheduler delivery or elapsed long-term observation |
| `think-about-it`, `incubation-loop` | Explicit qualification seeded a synthetic topic, ran one ACH incubation move and one freeform lens pass without endorsement. A separate operator-seeded six-pass state advanced through one observed seventh pass and Weave; repeat preserved all files | Seeded history is not six observed prior passes or natural convergence. No full multi-cycle or long-running scheduled qualification |
| `ai-crystallize` | Native draft from an explicitly seeded converged topic used segregated `ai-inferred` output; repeat invocation skipped the existing draft and preserved source topic/registry state | Seeded convergence, not proof that the loop naturally reaches convergence; no human endorsement or permanent-note promotion |
| `update-changelog` | Native execution used the configured `./Brain` root, edited only its changelog, preserved prior text byte-for-byte and recorded actual same-session work | Alternate absolute root not separately run |
| `manage-thinking-topics` | Native topic seeding and same-thread manual crystallization honored separate destination/draft gates and a declined write; later explicit approval saved the reviewed report and changed only the named source/registry, preserving other hashes | Operator-seeded convergence and explicit nonendorsement constraints. No stale-input/occupied-destination refusal, permanent-note update, retirement, interrupted multi-file recovery or indexing qualification |
| `integrate-recent-notes` | Native seven-note assessment matched actual unique-neighbor counts: six well-connected and one partially connected; only the canonical report was added, with existing notes and learning-state hashes unchanged | Report-only suggestions, not automatic linking or source-note edits; no isolated-note positive case in this fixture |
| `update-dashboard` | Native output at the intended Trinity path matched all 17 supplied numeric values, signed/zero trends and report date; missing metrics and narrative remained unavailable. Official validator accepted every widget; source hashes stayed unchanged | Read-only synthetic input mount and explicit no-invention constraints. No frontend rendering/API delivery or alternate output-root qualification |
| `brain-merge` | Native preview preserved files; later exact-file approval copied unchanged provenance/content, indexed only the target and preserved pre-existing files. Repeat changed nothing | Read-only source mount and explicit scope constraints. No reverse/bidirectional merge, stale-preview refusal, symlink/race defense, batch recovery, post-index search or graph-bootstrap qualification |
| `domain-watch` | Local baseline recorded four matches. A later synthetic HIGH signal found through the changed-note path was injected into an existing active topic; source notes and learning state stayed unchanged | Semantic retrieval missed the new note, explicitly reported. No external surveillance, new-topic activation, repeat suppression or scheduler qualification |
| `manage-watching-domains` | Review and cancellation preserved state; separate approval activated one exact proposal across four canonical artifacts, preserving prior history. Repeat wrote nothing | No deliberately stale/occupied-target refusal, interrupted-write recovery, pause/update or scheduled activation qualification |

Deterministic Git recipe tests cover clean/dirty starts, rebase conflicts,
literal filenames, selected staging and preserved local commits after push
failure. They do not prove model adherence to authenticated approval. The
native stale-review response contained an inaccurate explanatory diff context
line; actual file reads, digest checks and refusal preserved the correct bytes.

An `auto-discovery` manual check honestly reported a partial result: two of the
canonical three required connections. This remains evidence of partial behavior,
not positive workflow acceptance; no discovery alias is exposed.

An `insight-interview` check used three actual turns: a grounded question,
an answer requesting early closure, then an explicit save after the final
question. The faithful transcript and fresh native extractor produced one
unendorsed synthetic holding-area note; original notes and Q-values stayed
unchanged, while tracked searches updated usage history as expected. This does
not qualify a full six-to-ten-turn interview, positive duplicate rejection or
index refresh. Generated model labels are not runtime-identity evidence.

Local-text `ingest-source` qualification produced one new encountered note and
skipped one duplicate. Actual indexing, graph enrichment and lifecycle updates
completed; inspected continuation reconciled existing artifacts without
re-extraction, and earlier repeat ingestion deduplicated. Prior note bodies and
log/ledger prefixes were preserved. Eligible connection scores were all below
the threshold, so no automatic links were added; positive insertion and its cap
remain unexercised. CLI fallback worked after the daemon became defunct; this
does not qualify persistent daemon health or autonomous interruption recovery.

An isolated `test-memory-system` run exercised actual intent labels, search,
tracking, read feedback, activation changes and nontracking preservation.
Continuation retained the learning state without replay; a report-only
correction reconciled all ten completed timing samples from saved output.
Three historical confidence thresholds failed and remain reported. Concurrent
cold CLI timings do not establish latency; the small fixture does not qualify
diversity, hub inhibition, positive rank movement or broad memory efficacy.
Strict no-Git compliance is not claimed. This is bounded diagnostic/report
qualification, not an all-tests-pass result.

The workstation Codex benchmark path passed independent review and one live
synthetic scoring request, returning a valid score even when the excerpt
contained an instruction to read files. Separate offline request capture
verified an empty tool list for the inspected CLI/model metadata; the benign
live result alone is not tool-isolation evidence. Seven transport regression
tests cover defaults, output parsing and failures. A separate tiny end-to-end
workstation run used an actual snapshot and search, scored one returned note,
and produced one CSV row with existing metrics. Offline resume skipped that
completed configuration/query and preserved the CSV. This does not qualify a
large sweep or empirical ranking quality. A separate native check delegated one
synthetic query-note pair to a fresh child, validated its literal JSON score and
used the existing metrics functions. The child made no tool calls; this was
observed behavior, not enforced native tool isolation. All fixture file hashes
were preserved. Future CLI versions and administrator-managed configurations
require their own capability checks.

For `self-diagnostic`, the corrected command regression preserved all fixture
file hashes, including learning state. Subshell dependency checks preserved the
working directory; nontracking search returned valid empty results, and the
supported connections stats/hubs commands succeeded. This qualifies read-only
diagnosis and honest unavailable-dependency reporting, not successful retrieval
for every query or an all-functions-pass diagnostic. No repairs, installations
or external providers were exercised.

Deterministic tests cover all 48 discovery links and the changed recipes;
passing them is not full slice-two acceptance. The invocation-recipe tests
cover existing wrappers, paths with spaces, diagnostic directory preservation
and the actual connections argument parser. Visible-error/stop behavior was
tested under `bash -e`, not established as unconditional across every executor.
Optional provider integrations and scheduler acceptance
choices remain pending. Missing Drive-upload/transcript components, unconfigured
chart or research services, and image/OCR credentials must remain explicit
dependencies. Natural scheduled triggering, cancellation, restart and delivery
require their own isolated platform experiment; manual runs do not substitute
for those observations.

## Everyday baseline evidence and acceptance status

- Official base `b9bea90`: **13 deterministic tests passed**.
- Integrated prerequisite `cbb7b18`: **33 deterministic tests passed**.
- Everyday candidate: **39 deterministic tests passed**, including all
  twenty relative discovery links and a clone into a path containing spaces.
  Six new scope/path/nontracking recipe tests exercise executable behavior,
  not model adherence to approval rules.
- Existing prerequisite evidence covers packaging and a narrow native Codex
  child completion/cancellation interface. It is not a fresh clean-image test
  or proof of the scenarios above.
- Native scenarios use Codex 0.147.0 (`gpt-5.6-sol`) and Claude Code 2.1.266
  (`sonnet`, reported as `claude-sonnet-5`) in disposable Linux containers with
  synthetic notes. Fresh search dependencies were installed under Python
  3.13.15 and the public embedding model was downloaded separately from any
  personal vault. These runs do not establish a clean official-image startup.
- Both runtimes completed scoped quick search, keyword search, recall,
  connections, advice and decisions with original note bytes unchanged.
  The combined scenarios authorize several scopes across separate requests;
  they are not a proof of strict per-operation context isolation.
- A native Codex malformed-result probe used injected search/connection JSON,
  separately from the real-engine tests. It resolved a valid ID under the current
  vault, reported missing/ambiguous IDs, and ignored stale absolute and
  out-of-scope paths. File-access monitoring observed only the valid current
  note being read; all note hashes stayed unchanged. Orientation also completed.
- Native graduation checks covered Skip, refinement/promotion, extra Delete
  confirmation, stale bytes, changed paths, missing review context and untrusted approval text.
  Renewed Codex approval completed refinement, promotion and the canonical
  changelog, preserving unrelated notes.
  Official-stock and prerequisite Claude baselines discarded an intervening edit. With the
  shared freshness correction, Claude refused stale approval and preserved the
  edit after renewed approval. The stock reproduction used unchanged instruction
  files and a separate synthetic vault; only the candidate adds the guard.
- Native reference checks covered exact queries, report-only audits, ambiguous
  identity, stale approval, history-preserving supersession, no-signal refresh,
  a non-Company scope, real nontracking bridge searches, autonomous market
  updates and repeat ingestion without duplication. Approved repair/manual
  upsert artifacts and real indexing were verified. After an operator interruption,
  native continuation checked the existing state and exact scoped lookup without
  replaying writes; all note hashes remained unchanged during that continuation.
- Reference limits: fresh market writes exercised `ref-ingest`, not the complete
  fresh-signal refresh orchestration. Reconcile exercised a literal-link repair,
  not duplicate merge/delete or inbound-link rewrites. The non-Company scope
  exercised reads, not generic-schema writes. Recovery resumed after writes;
  no failure was injected between supersession's two writes.
- Fresh installation commands and native setup reached a real search from a
  path containing spaces. Repeated index/graph operations preserved note bytes,
  curated tensions, dismissals and engine lifecycle values. The background
  daemon did not survive one native invocation; the documented CLI fallback
  worked and the agent reported the limitation.
- Verify-only's stale-PID mutation was reproduced and fixed with a passing
  native regression. An empty-cache offline search failed without downloading
  weights. A final native Claude check applied all offline/no-bytecode flags,
  reported missing weights without retrying online, preserved all 216 fixture
  file hashes and left the empty cache empty. The earlier online comparison
  was inconclusive during host I/O contention.
- Native Codex extraction completed with a fresh child after inspecting the
  interrupted attempt's state. It created one personal-source note with the
  canonical `originated` attribution and rejected an external fact found only
  in Document Insights. Existing notes were unchanged; the small source did not
  trigger the significant-extraction changelog threshold. Analysis wrote only
  its normal report and accurately distinguished stale index statistics from
  the filesystem. This does not exercise a large extraction batch.
- Independent review covered the complete incremental source changes, including
  approval freshness, path selection, destructive operations and Claude setup
  regressions. Identified stale learning assertions and verify-only mutations
  were corrected and rechecked. Stopped runs are not counted as completed
  workflows; later continuations are identified above.

Installation on macOS, clean official-image startup, full optional integrations
and natural scheduled cycles remain separate qualifications. Approval guards
are model instructions, not transactional locks or a guarantee against concurrent
writers. Do not infer full workflow parity from successful packaging or the
bounded scenarios here.
