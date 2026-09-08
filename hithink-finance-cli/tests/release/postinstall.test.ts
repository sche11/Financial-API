import { readFile } from 'node:fs/promises';
import { expect, test } from 'vitest';

test('postinstall is best-effort and reuses the package-local Skills sync command', async () => {
  const source = await readFile('scripts/postinstall.mjs', 'utf8');
  expect(source).toContain("dist', 'cli', 'main.js");
  expect(source).toMatch(/'skills',\s*'sync',\s*'--repair'/u);
  expect(source).toContain('DISABLE_TELEMETRY');
  expect(source).toContain('HITHINK_FINANCE_NO_UPDATE_CHECK');
  expect(source).toContain('skills sync --repair');
  expect(source).not.toContain('npx');
  expect(source).not.toContain('@latest');
});
