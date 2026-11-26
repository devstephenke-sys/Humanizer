# Draftwell feature inventory

Research date: 26 November 2026.

Reference site inspected in a browser and from public pages:

- https://stealthwriter.ai/
- https://stealthwriter.ai/humanizer
- https://stealthwriter.ai/ai-detector
- https://stealthwriter.ai/pricing
- https://stealthwriter.ai/faq
- https://stealthwriter.ai/changelog
- https://stealthwriter.ai/about
- https://stealthwriter.ai/sign-in

The signed-in humanizer was not opened. Humanizer controls that live only after sign-up are taken from the public FAQ, homepage, pricing, and changelog, and are marked as such. Nothing below is inferred from private APIs or source code.

Draftwell is an original product. It does not use the reference name, logo, model names, or payment system.

## Product decision

Every verified writing and detection feature is available without an account limit, subscription, or payment. Accounts exist only so a person can save documents. Abuse protection is a short rate limit and a maximum input size, applied equally to everyone.

Payments, invoices, plan gates, upgrade prompts, and affiliate billing were verified on the reference site and are intentionally not built.

## Verified reference features

| Feature | Purpose | User interaction | Input | Expected output | Backend | AI | Draftwell status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Marketing homepage | Explain the product and route to tools | Nav, theme toggle, calls to action | None | Static content plus links | None | None | Implemented as an original homepage |
| Theme toggle | Switch light and dark appearance | Header button | None | Theme class on the page | None | None | Implemented |
| Public AI detector | Estimate how AI-like a draft reads | Paste text, pick a scan mode, run scan | Text, public demo cap 500 words | Overall score, label, sentence highlights | Scan endpoint | Proprietary detector (not available) | Implemented with an original probabilistic analyzer. Not a copy of their V1/V2 models |
| Detector versions V1 and V2 | Two scanner generations | Radio control, V2 default | Mode | Different scores | Proprietary | Proprietary | Not replicated as named versions. Replaced by Quick and Deep analysis modes, documented as an alternative |
| Short-text warning | Warn when a scan is less reliable | Automatic under 100 words | Word count | Warning banner | Validation | None | Implemented |
| Loading state | Show that a scan is running | Button disables, "Scanning..." | In-flight request | Spinner and status | Request lifecycle | None | Implemented |
| Humanizer entry | Rewrite a draft | Paste text. Public page then requires sign-up | Draft text | Account wall on the reference site | Account + rewrite | Proprietary rewrite models | Implemented without an account wall |
| Rewrite intensity | Control how much wording changes | Levels 1–10. FAQ: 1–3 light, 7–10 heavy. Homepage also says light, medium, aggressive | Level | Closer or freer paraphrase | Rewrite settings | LLM | Implemented as a 1–10 slider plus Light, Medium, and Strong presets |
| Rewrite profiles | Choose a rewrite style | Model selector described in the May 2026 changelog: lightweight, stronger coherence, and older legacy options | Profile | Different rewrite behavior | Provider settings | LLM | Implemented as Swift, Studio, Careful, and Plain. Original names. All unlocked |
| Meaning and citation care | Avoid drifting facts | User reviews the result. Humanizer FAQ says rewrites can change a detail | Draft, optional citation lock | Rewritten text plus warnings if markers disappear | Prompt plus post-check | LLM | Implemented. The app tells the user to review facts. It does not promise a detector score |
| Sentence alternatives | Fine-tune one sentence | Click a sentence, pick another phrasing. Described on the homepage and FAQ. Not observed inside a signed-in session | One sentence plus context | Several alternatives | Alternative endpoint | LLM | Implemented |
| Deep scan highlights | Show which sentences look less natural | Shown after a public scan. Green = more natural, red = still needs work | Scanned text | Color-coded sentences and a score card | Detector | Heuristics | Implemented |
| Word count | Show draft length | Live counter. Public detector shows `n / 500 words`. Changelog mentions humanized word counts | Text | Word and character counts | Shared text helpers | None | Implemented, without a paid word cap |
| Humanize handoff | Move from a scan to a rewrite | "Humanize" link on the detector | Current text | Humanizer with that draft | Client state | None | Implemented |
| Account sign-in | Reach the signed-in app | Email form on `/sign-in`. Humanizer page also says email or Google | Email | Session | Auth API | None | Email and password implemented. Google sign-in was not built because it needs OAuth credentials that are not part of the free local stack |
| Responsive layout | Use the app on phones | FAQ says desktop, tablet, and mobile | Viewport | Usable layout | None | None | Implemented |
| Multilingual rewrite | Keep or target a language | FAQ and changelog list several languages | Text plus language | Rewrite in that language | Prompt instruction | LLM | Implemented as an explicit language control |
| Dashboard billing | Plan, invoices, subscription | Changelog, August 2026 | Account | Billing UI | Payments | None | Excluded on purpose |
| Pricing and paid limits | Sell daily quotas and longer inputs | Pricing page | Plan | 10 to 2,000 actions/day and 1,000 or 5,000 word caps | Billing | None | Excluded. One shared input ceiling for reliability only |
| Public API | Programmatic access | FAQ: no public API | n/a | n/a | n/a | n/a | Not a public product API. This app has its own private API for its frontend |
| Browser extension | Rewrite outside the site | FAQ: not available | n/a | n/a | n/a | n/a | Not built |
| Live chat support | Account support | Changelog mentions a dashboard chat vendor | Account | Chat widget | Third party | None | Not built. About page points at repository docs instead |
| Affiliate program | Referrals | Footer link | n/a | Marketing page | n/a | n/a | Not built |

## Reference claims that are not copied

- The reference FAQ says submitted text is not stored after processing. Draftwell does the opposite when someone saves a document, because this brief requires a workspace and history. Unsaved scans and rewrites are not written to the database.
- The reference markets output as reading naturally. Draftwell does not claim a result is human-authored, original in a legal sense, or able to pass any detector.
- Their detector copy already says a score is an estimate and not proof of authorship. Draftwell keeps that limitation in the interface.

## Writing tools that were not separate products

These pages were not found on the reference site: essay rewriter, article rewriter, sentence rewriter, paragraph rewriter, paraphraser, or grammar checker. The verified writer is one humanizer with intensity, profile, and sentence alternatives.

Draftwell still provides those jobs as separate screens, because this brief asks for distinct writing tools. Each screen calls the same provider layer with its own instructions. They are original tools, not clones of hidden reference pages.

| Tool | Purpose | Status |
| --- | --- | --- |
| Humanizer | Natural rewrite with intensity and profile | Implemented |
| Rewriter | General rewrite of a draft | Implemented |
| Paraphraser | Same meaning, different wording | Implemented |
| Essay rewriter | Essay structure and academic tone, facts kept | Implemented |
| Article rewriter | Article flow, headings kept | Implemented |
| Sentence rewriter | One or a few sentences | Implemented |
| Paragraph rewriter | A single paragraph | Implemented |
| Content improvement | Clarity and directness | Implemented |
| Grammar and readability | Corrections with an explanation | Implemented |

## Workspace features from this brief

The reference marketing does not show document history. These are Draftwell features required by the brief:

| Feature | Status |
| --- | --- |
| Copy result | Implemented in the browser |
| Download TXT | Implemented in the browser |
| Download DOCX | Implemented by the API |
| Clear input | Implemented |
| Restore the previous input | Implemented |
| Side-by-side comparison | Implemented |
| Regenerate | Implemented |
| Save, list, open, and delete documents | Implemented for signed-in users |
| User isolation | Documents are queried by the signed-in user id |

## Explicitly excluded

Subscriptions, premium flags, Stripe, PayPal, checkout, card collection, invoices, billing tables, paid word quotas, upgrade prompts, and feature locks.
