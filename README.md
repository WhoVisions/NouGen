# 🪐 NouGen

> The application and developer layer for [NouGenShards](https://github.com/Who-Visions/NouGenShards).

NouGen provides the user-facing workflows, reusable skills, and high-level tools that build on NouGenShards. NouGenShards owns durable shard storage and the lower-level context, retrieval, and relay substrate.

## Architecture

- **WhoVisions/NouGen** — application workflows, developer-facing tools, reusable skills, and integrations.
- **Who-Visions/NouGenShards** — durable context storage, retrieval primitives, relay infrastructure, and identity capsule contracts.

The application layer orchestrates work and uses the Shards substrate for persistent context. Storage and retrieval concerns stay in NouGenShards; product workflows and integrations stay in NouGen.

## What lives here

- **Reusable skills** in `skills/`, including the [GSAP scroll video website](skills/05-web-frontend/gsap-scroll-video-website), [autonomous plan and execute workflow](skills/13-automation/plan-execute-autonomous), and [NouGenTube morph](skills/99-fleet-custom/nougentube-morph).
- **Local voice utility** at `tools/speak.py`.
- **NouGenTube morph workflow**, which turns source material into reusable tools, skills, and patterns.

## Morph pipeline

```
Watch → Digest → Extract → Build → Shard
  │        │         │        │       └─ Store reusable context in NouGenShards
  │        │         │        └─ Generate skills and tools
  │        │         └─ Identify workflows and patterns
  │        └─ Summarize source material
  └─ YouTube, research, or operational knowledge
```

**Shard and recurse so you don't rehearse.**

<!-- nougen:fleet-role:begin (generated from nougen-handoffs fleet/manifest.json; edit the manifest, not this block) -->
## Fleet role

| | |
|---|---|
| Role | UNDECLARED (umbrella 'recursive intelligence substrate'; overlaps NouGenShards?) |
| Kind | core |
| Status | undeclared |
| Canonical for | — |
| Visibility | public |

<!-- nougen:fleet-role:end -->
