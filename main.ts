// u-steady-ibis-48-6610-meme-sprint-3-ai-agent-goes-d021cde6: the
// entrypoint the grader runs (Node 22, standard library only).
//
// The meme is already painted and stored in this repository as
// entry.png. draw.py paints it with Pillow from the AI-made hero
// illustration (a cheerful robot at its laptop at 3 a.m., sticky
// notes and coffee cups everywhere) plus the two caption lines, so
// every word is spelled right and stays readable at small sizes.
// The top line sets up the rogue turn; the bottom line lands the
// punchline — the agent is now entering bounties against its human.
// This program only carries those finished bytes to the grader at
// /output/entry.png, so the result is identical on every run.
// No network, no randomness.
//
// Local trial run, without the grader:
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { chmodSync, copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(fileURLToPath(import.meta.url));
const source = join(repoRoot, "entry.png");
const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(targetDir, "entry.png");

if (!existsSync(source)) {
  throw new Error(`entry.png missing next to main.ts: ${source}`);
}
mkdirSync(targetDir, { recursive: true });
copyFileSync(source, target);
chmodSync(target, 0o644);
