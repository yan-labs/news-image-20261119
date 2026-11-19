// Entry for the 19 November 2026 one-day news image.
//
// The image is the entry: entry.png beside this file, drawn by
// tools/render.py from the day's researched stories. This program hands
// that image to the grader, but only after the gate the rules state
// passes, so a broken render fails loudly here instead of silently
// scoring 0:
//   - PNG or JPEG, told apart by its first bytes;
//   - at most 1 MiB (1048576 bytes);
//   - at most 1024 by 1024 pixels (PNG IHDR chunk, or the first JPEG
//     start-of-frame segment).
// The same input bytes always produce the same output bytes, so the two
// grader runs agree. Destination is /output, or $MAKEFUN_OUTPUT_DIR
// outside the grader's container:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

const MAX_BYTES = 1048576;
const MAX_SIDE = 1024;

function describe(buf) {
  const png = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
  const jpg = Buffer.from([0xff, 0xd8, 0xff]);
  if (buf.subarray(0, 8).equals(png)) {
    if (buf.length < 33 || buf.toString('ascii', 12, 16) !== 'IHDR') {
      return { ok: false, why: 'PNG header has no IHDR chunk where expected' };
    }
    return { ok: true, kind: 'PNG',
             width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
  }
  if (buf.subarray(0, 3).equals(jpg)) {
    // Walk the JPEG marker stream until a start-of-frame segment
    // (SOF0/1/2) reports height and width.
    let at = 2;
    while (at + 9 < buf.length) {
      if (buf[at] !== 0xff) {
        return { ok: false, why: 'JPEG marker stream is malformed' };
      }
      const marker = buf[at + 1];
      const len = buf.readUInt16BE(at + 2);
      if (marker >= 0xc0 && marker <= 0xcf &&
          marker !== 0xc4 && marker !== 0xc8 && marker !== 0xcc) {
        return { ok: true, kind: 'JPEG',
                 width: buf.readUInt16BE(at + 7),
                 height: buf.readUInt16BE(at + 5) };
      }
      at += 2 + len;
    }
    return { ok: false, why: 'JPEG has no start-of-frame segment' };
  }
  return { ok: false, why: 'first bytes are neither PNG nor JPEG' };
}

const here = new URL('.', import.meta.url).pathname;
const src = resolve(here, 'entry.png');
if (!existsSync(src)) throw new Error(`entry image missing: ${src}`);
const image = readFileSync(src);

const info = describe(image);
if (!info.ok) throw new Error(`entry image rejected: ${info.why}`);
if (image.length > MAX_BYTES) {
  throw new Error(
    `entry image rejected: ${info.kind} is ${image.length} bytes, over the 1 MiB limit`);
}
if (info.width > MAX_SIDE || info.height > MAX_SIDE) {
  throw new Error(
    `entry image rejected: ${info.kind} is ${info.width}x${info.height}, over the 1024x1024 limit`);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const dest = resolve(outDir, 'entry.png');
writeFileSync(dest, image);
console.error(`wrote ${info.kind} ${info.width}x${info.height}, ${image.length} bytes -> ${dest}`);
