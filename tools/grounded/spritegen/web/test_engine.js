const fs = require('fs'), zlib = require('zlib'), E = require('./engine.js');
const t0 = Date.now();
const r = E.generate({}, {}, {}, []);
console.log('ms', Date.now() - t0, JSON.stringify(E.check(r.key, r.pal)), 'maat', r.po.w, r.po.h);
const N = 64, raw = Buffer.alloc(N * (N * 4 + 1));
for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) { const k = r.key[y * N + x], o = y * (N * 4 + 1) + 1 + x * 4; if (k) { const c = r.pal[k] || [255, 0, 255]; raw[o] = c[0]; raw[o + 1] = c[1]; raw[o + 2] = c[2]; raw[o + 3] = 255; } }
const crc = b => { let c, t = []; for (let n = 0; n < 256; n++) { c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } c = 0xffffffff; for (const v of b) c = t[(c ^ v) & 255] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; };
const chunk = (type, data) => { const l = Buffer.alloc(4); l.writeUInt32BE(data.length); const td = Buffer.concat([Buffer.from(type), data]); const c = Buffer.alloc(4); c.writeUInt32BE(crc(td)); return Buffer.concat([l, td, c]); };
const ih = Buffer.alloc(13); ih.writeUInt32BE(N, 0); ih.writeUInt32BE(N, 4); ih[8] = 8; ih[9] = 6;
fs.writeFileSync(process.argv[2], Buffer.concat([Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]), chunk('IHDR', ih), chunk('IDAT', zlib.deflateSync(raw)), chunk('IEND', Buffer.alloc(0))]));
