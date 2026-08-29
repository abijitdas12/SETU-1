import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const frontendDir = __dirname;
const publicDir = path.join(frontendDir, 'public');
const distDir = path.join(frontendDir, 'dist');

if (fs.existsSync(distDir)) {
  fs.rmSync(distDir, { recursive: true, force: true });
}
fs.cpSync(publicDir, distDir, { recursive: true });

const indexHtmlPath = path.join(frontendDir, 'index.html');
const distIndexHtmlPath = path.join(distDir, 'index.html');
fs.copyFileSync(indexHtmlPath, distIndexHtmlPath);

console.log('✓ Production frontend distribution assembled in dist/');
