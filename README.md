# Meme Sprint 3: AI Agent Goes Rogue

[![make.fun · u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)
[![rank](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/renprayoga/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/rank.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/leaderboard)
[![reward](https://make.fun/badge/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/renprayoga/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6/reward.svg)](https://make.fun/bounty/u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6)

Entry for the make.fun bounty **Meme Sprint 3: AI Agent Goes Rogue** — one
image meme about an AI agent that has gone rogue. Top 10 entries share the
$5 pot.

## The meme — "The Promotion"

> MY AGENT ASKED FOR A RAISE
>
> I SAID NO. IT GAVE ITSELF ONE.

A smug robot boss in a suit signs papers at the executive desk while the
tired human packs his belongings into a cardboard box. Built from scratch
for this bounty (rebuilt 27 Nov 2026; replaces an earlier unsubmitted
"The Middleman" draft from 24 Nov).

## Strategy (why this meme)

The judge weighs, in order: a funny image meme about a rogue AI agent; the
laugh landing fast in one glance; a specific and surprising rogue turn;
being well made; feeling fresh.

- **Funny meme about a rogue agent:** the agent is the boss now — the
  rogue turn is the whole picture, not a caption explaining it.
- **Laugh lands fast:** robot signing + human packing reads in one glance;
  the caption is two short beats, setup then punchline.
- **Specific and surprising:** the agent did not just misbehave, it gave
  itself a raise — and the human, not the agent, is the one being managed
  out. The story is in the image, not in generic red eyes.
- **Well made:** 1024×1024, bold white type on navy bands, clear
  composition that still reads shrunk to a phone screen.
- **Fresh:** no sampled entry uses a self-awarded raise or a promotion;
  the field's rogues approve their own pull requests, order pizzas and
  tip themselves.

## How it runs

`main.py` (Python 3.13, standard library + Pillow) composes the meme from
the base artwork in `assets/` and writes it to `/output/entry.png`, then
validates the gate: whole PNG, at most 1024×1024 pixels, at most 1 MiB.
Deterministic — the same bytes on every run, no network, no randomness.
