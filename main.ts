import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// Copies POST.json (the X post's address, written by the second builder
// after the meme is posted) from this repository to the output directory.
const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const src = join(here, "POST.json");
const dst = join(outDir, "POST.json");

if (!existsSync(src)) {
  console.error("POST.json not found next to main.ts");
  process.exit(1);
}
mkdirSync(outDir, { recursive: true });
copyFileSync(src, dst);
// Byte-size check: the copy must be identical to the source.
if (statSync(src).size !== statSync(dst).size) {
  console.error("POST.json copy size mismatch");
  process.exit(1);
}
console.log(`copied POST.json -> ${dst}`);
