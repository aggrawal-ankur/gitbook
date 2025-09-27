---
title: Why I Moved from GitBook to GitHub Pages (Hugo + Hextra)
sidebar:
  exclude: false
---

***September 27, 2025***

I had been using GitBook for about three months, mainly because it made writing effortless:

1. Great UI — Modern GitBook looks clean and professional. No static site generator (SSG) theme came close.
2. Ease of use — Simple workflow, no setup headaches.
3. WYSIWYG editor — What you see is what you get.
4. Fast sync — Changes showed up almost instantly.
5. Markdown storage — Notes were plain .md files, making migration possible.
6. Clean repo — My GitHub repo wasn’t polluted with config or build artifacts, just Markdown.

The trade-offs were acceptable at first:

1. Limited customization/extensibility — I once wanted to experiment with a knowledge graph (like Obsidian), but GitBook had no way to integrate such features.
2. No cancel option for edit requests — Annoying, but tolerable.

Over time, GitBook began failing at the very things it was good at:

1. Slow updates — Sometimes changes didn’t show up for 12+ hours, even after clearing caches and testing across devices.
2. Broken CSS — Pages often loaded without styles until refreshed.
3. Random reloads — The editor would refresh mid-flow, breaking focus.
4. Critical failures — On September 26, 2025, I tried creating a simple table. Every attempt resulted in errors and forced reloads. That was the breaking point.

Since I had already explored alternatives, I switched immediately:

1. Picked Hugo with the Hextra theme for its balance of speed, flexibility, and polish. Learned them and started migration.
2. Migration took 8h 14m total (6h 44m on Sept 26, plus 1h 30m on Sept 2 for prep work).

Now my site is stable, extensible, and independent of a hosted editor.

The advantages are immediately noticeable.
1. Performance and reliability — No more waiting hours for updates to show up. GitHub Pages does it instantly.
2. Offline-friendly — With Asia's recent internet issues (the Red Sea cable cuts), I can now work without relying on GitBook’s cloud.
3. Customization — Hugo + Hextra lets me extend and modify the site however I want. All it takes is learning the framework, which is in my control.

My guiding principle is to build a setup I can control as much as possible. That way, I can spend time working instead of being blocked by unreliable tools. With Hugo + Hextra on GitHub Pages, I’ve reclaimed that control — and I’m much happier for it.