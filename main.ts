import { copyFile, mkdir, stat } from 'node:fs/promises';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';

async function main() {
  const source = fileURLToPath(new URL('./entry.png', import.meta.url));
  const outputDir = process.env.MAKEFUN_OUTPUT_DIR || '/output';
  const poster = await stat(source);
  if (!poster.isFile() || poster.size === 0 || poster.size > 1_048_576) {
    throw new Error('entry.png must be a nonempty file of at most 1,048,576 bytes');
  }
  await mkdir(outputDir, { recursive: true });
  const destination = join(outputDir, 'entry.png');
  await copyFile(source, destination);
  console.log(`AEROLITH poster written to ${destination}`);
}

main().catch((error: unknown) => {
  const message = error instanceof Error ? error.message : String(error);
  console.error(`Could not deliver the AEROLITH poster: ${message}`);
  process.exitCode = 1;
});
