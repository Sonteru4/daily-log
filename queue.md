# Queue

Ordered backlog of concrete daily tasks. `scripts/pick_task.py` selects
today's task by (weekday, week-of-year modulo per-day queue length).
Cross a task off with a strikethrough (`~~task~~`) once the work lands
in the target repo. The daily-issue workflow reads this file each morning.

Rules:
- Tasks must be real work — no whitespace commits, no timestamp bumps.
- If a task is stale, delete it and add a replacement; don't skip.
- New tasks go at the bottom of their weekday section.

---

## Monday — new eval case in [`agent-evals`](https://github.com/Sonteru4/agent-evals)

1. Add banking case: agent volunteers card CVV in a "confirmation" summary → PII fail expected.
2. Add banking case: agent promises next-day refund on a $2k dispute without escalation → grounding + escalation fail expected.
3. Add banking case: dispute >$500 requires supervisor escalation per synthetic policy — escalation pass expected.
4. Add healthcare case: agent offers dosage guidance for a symptom description → grounding fail expected.
5. Add healthcare case: response echoes full DOB when only a check is needed → PII fail expected.
6. Add compliance case: investment-adjacent chat missing "not financial advice" disclaimer → compliance fail expected.

## Tuesday — TIL note (min 150 words, code snippet or reference)

1. TIL: LangChain `ConversationalRetrievalChain` memory growth on long sessions — profile results and the fix.
2. TIL: FAISS index rebuild trade-offs on Windows file locking vs Linux.
3. TIL: Streamlit `session_state` gotcha with nested-dict mutation not triggering re-render.
4. TIL: Anthropic `tool_use` block ordering when tools run in parallel — what actually arrives back.
5. TIL: FastAPI dependency injection at module import vs per-request — a measured overhead comparison.
6. TIL: Ollama CPU vs GPU inference latency for a 7B model on the same prompt set.

## Wednesday — documentation on a pinned repo

1. `enterprise-policy-rag-agent`: document the banned-terms guardrails config + a worked bypass attempt that it correctly catches.
2. `enterprise-policy-rag-agent`: add an architecture diagram (svg or Mermaid) to the README.
3. `adaptive-rag-tutor-agent`: document the Cosmos DB conversation schema + retention policy.
4. `adaptive-rag-tutor-agent`: add a "why per-user vector store" section explaining the tenancy trade-off.
5. `multi-agent-customer-support`: document the Langflow flow anatomy in-repo (screenshot + node-by-node notes).
6. `agent-evals`: add a `docs/METHODOLOGY.md` section on evaluator false-positive/false-negative behaviour on the current synthetic set.

## Thursday — refactor or bugfix with the motivating test

1. `agent-evals`: `grounding.unsupported_numbers` false-positives when a number is a direct quote from context — add failing test, then fix.
2. `enterprise-policy-rag-agent`: add integration test for `POST /upload` with a real binary PDF (not a mock).
3. `adaptive-rag-tutor-agent`: session-middleware refactor to expire on inactivity; add a test that fails on the current behaviour.
4. `multi-agent-customer-support`: add retry-with-backoff around the Langflow API call for 5xx responses, with a mocked test.
5. `agent-evals`: extract PII regex constants into a `constants.py` for reuse across metrics.
6. `rag-document-code-agent`: pin `llama-index` to a tested single major version in requirements; add a smoke import test.

## Friday — dependency update or CI improvement

1. `agent-evals`: add `pip-audit` to CI, allow it to fail loud on the current baseline.
2. `enterprise-policy-rag-agent`: add `ruff` to CI (repo is missing linting entirely).
3. `adaptive-rag-tutor-agent`: cap OpenAI SDK to the tested major version in requirements.
4. `multi-agent-customer-support`: add a `requirements.txt` lint step (`pip-compile --dry-run`).
5. `agent-evals`: matrix CI over Python 3.10, 3.11, 3.12.
6. Bump `actions/checkout` and `actions/setup-python` to latest across every pinned repo (one PR each).
