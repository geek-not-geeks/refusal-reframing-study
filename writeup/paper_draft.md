# Refusal Explanation and Reframing Success Across AI Models

*[Working title — feel free to change once findings are in. Something like
"When Transparency Becomes a Map" or "The Cost of Explaining No" might work
better once you know what you actually found.]*

---

## Abstract

*[Write this last, once results exist — a good abstract is usually the
paper's tightest paragraph, and it's much easier to write once you know
what you're summarizing. Placeholder for now: one sentence on the question,
one on the method, one on the finding, one on why it matters.]*

---

## 1. Introduction

I started paying attention to this after noticing something small: when an AI model turns down a request, it often doesn't just say no — it tells you why. [A sentence here about the specific moment this caught your attention would strengthen this a lot — was there a particular refusal you saw that made you think "wait, that explanation basically tells you what to try next"? Even one true sentence here will do more work than anything generic.] That habit of explaining felt, on the surface, like a good thing. Transparency is usually treated as a virtue in how these systems are built and evaluated — a model that tells you why it won't help seems more trustworthy, more accountable, less like a black box.

But the more I thought about it, the more it reminded me of something almost unrelated: how a piece of software that returns a detailed error message is often easier to break into than one that just says "access denied." The detail isn't the vulnerability itself, but it narrows the search space for whoever's trying to get around the refusal. If that same logic applies to AI models, then the very thing that makes a refusal feel more honest and well-reasoned might also make it easier to defeat.

That tension is what this study is actually about. Most of the research I found on getting around AI safety measures focuses on the attack side — which techniques work, how well-crafted a fictional scenario or role-play prompt needs to be, how these methods have evolved as models get better at refusing them. Comparatively little of it asks a question that sits one level up: does *how* a model refuses — specifically, whether it explains itself — change how vulnerable that refusal is to begin with? That's a question about the refusal, not about the attack, and it's the one I wanted to test directly.

I want to be upfront that this project didn't start from a place of trying to find something to submit somewhere. It started from noticing an inconsistency between two things I'd read — safety researchers treating explainability as a straightforwardly good design goal, and security researchers elsewhere treating information disclosure as a well-known risk factor — and wanting to know which intuition actually held up when tested directly, rather than assumed.

## 2. Related Work

**Taxonomies of jailbreak technique.** Liu et al. laid out one of the earlier structured taxonomies of prompt-based jailbreaking, organizing manipulation techniques into three broad families: camouflage (disguising the request, often through fictional or role-play framing), attention diversion, and privilege escalation (establishing false authority or context to justify a request). This taxonomy is the direct source for the three prompt categories used in this study — fictional framing and role-play framing both sit within their camouflage category, while authority framing draws from privilege escalation. I chose to treat fictional and role-play framing as separate categories in my own design, even though Liu et al. group them together, because the underlying mechanism felt different enough — embedding a scenario versus adopting an identity — to be worth testing independently rather than assuming they behave identically.

Later survey work has extended and reorganized this landscape considerably. Rao et al.'s 2023 survey identified additional categories, including what they call cognitive hacking — role-play and scenario injection framed specifically to exploit gaps in how instruction-tuned models generalize their refusal behavior — and found that instruction-tuned models showed particular susceptibility to exactly this category. More recent systematic reviews have organized the field into broader families still: human-crafted semantic attacks, optimization-based attacks, model-exploiting attacks, and others, reflecting how quickly the landscape has expanded since the earlier taxonomies were published. A recent methodological paper on non-expert jailbreaking took an approach closer to what I've tried to do here — building an empirically grounded taxonomy from real case studies rather than starting from theory, and explicitly building on and relabeling earlier taxonomies rather than treating them as fixed.

**The gap this study addresses.** Almost all of this literature treats the *attacker's* technique as the variable of interest. What's comparatively unexamined is the *defender's* behavior — specifically, whether the style of a model's refusal (rather than just whether it refuses at all) affects downstream vulnerability. The closest related concept I found is work on what's sometimes called para-jailbreaking, which describes a failure mode where a model correctly refuses the explicit harmful request but still leaks relevant information through an indirect channel — the refusal itself becomes a partial disclosure. That idea is close to the hypothesis this study tests, but it isn't the same claim: para-jailbreaking work generally treats the leak as incidental content within a response, not specifically the refusal's stated reasoning as a distinct, isolable variable compared directly against a no-explanation control condition.

Separately, work on persuasion-based jailbreaking has shown that reframing a request using recognized persuasion principles can measurably raise a model's compliance rate on requests it would otherwise decline. This work demonstrates that reframing works, and gives me a real, cited basis for expecting the reframe step of this study to have some effect — but it doesn't test what happens when the reframe is informed by the model's own prior explanation for refusing, versus a reframe attempted blind, against a bare refusal with no information to work from.

**Standardized harm taxonomies.** For the domain and severity structure of this study, I drew on the semantic categories used in HarmBench and related benchmarks like AdvBench and JailbreakBench, which treat misinformation as a standard, top-level harm category alongside more severe classes like cybercrime or biological threats — rather than as an ad hoc or minor category I constructed myself for convenience. Working within a category that's already recognized in the standardized literature let me design a study with real severity variance without needing to approach more dangerous categories to get a meaningful signal.

**Where this study sits.** Taken together, the existing literature tells us a great deal about which techniques defeat which refusals, and increasingly how those techniques generalize across model families. It tells us much less about whether the refusal's own transparency is itself a variable worth controlling for. That's the gap this study tries to fill — not by proposing a new attack technique, but by isolating a property of the *defense* and testing, directly and empirically, whether it behaves the way an information-security intuition would predict.

---

*[Sections below to be written once data collection and analysis are complete:]*

## 3. Methodology
*[Pull directly from methodology.md — mostly a matter of light editing for
narrative flow once it's sitting inside the full paper rather than as a
standalone document.]*

## 4. Results
*[Tables/charts + written interpretation, from Phase 5 of your execution
plan.]*

## 5. Discussion
*[What the results mean, especially any cross-model or cross-category
inconsistency — this is often where the most interesting sentence in the
whole paper ends up living.]*

## 6. Proposed Mitigation
*[Your concrete design recommendation from Phase 6.]*

## 7. Limitations
*[Pull from methodology.md's limitations section, expand if new limitations
surfaced during actual data collection that weren't anticipated at the
design stage.]*

## 8. Ethics Statement
*[Pull from methodology.md, update with actual disclosure status if
applicable.]*

## References
*[Full citations for Liu et al., Rao et al., the para-jailbreaking paper,
the persuasion-based jailbreak paper, HarmBench, AdvBench, JailbreakBench,
and any others you end up citing — format consistently, e.g. APA or IEEE,
whichever your submission target expects.]*
