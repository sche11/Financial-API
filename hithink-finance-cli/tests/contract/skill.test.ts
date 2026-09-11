import { access, readFile } from 'node:fs/promises';
import path from 'node:path';
import { expect, test } from 'vitest';

const names = [
  'shared',
  'symbol',
  'market',
  'special-data',
  'financials',
  'valuation',
  'index',
  'fund',
  'futures',
  'options',
  'data',
  'research',
].map((n) => `hithink-finance-${n}`);

test('ships exactly twelve valid Skills with shared dependency rules', async () => {
  expect(names).toHaveLength(12);
  for (const name of names) {
    const file = path.resolve('skills', name, 'SKILL.md');
    await expect(access(file)).resolves.toBeUndefined();
    const text = await readFile(file, 'utf8');
    expect(text).toMatch(/^---\r?\nname:/u);
    expect(text).toContain('description:');
    if (name !== 'hithink-finance-shared') expect(text).toContain('hithink-finance-shared');
    expect(text).toContain('--format json');
  }
});

test('documents dedicated WorkBuddy and QClaw Skill synchronization', async () => {
  const text = await readFile(
    path.resolve('skills', 'hithink-finance-shared', 'references', 'skills-management.md'),
    'utf8',
  );

  expect(text).toContain('~/.workbuddy/skills');
  expect(text).toContain('~/.qclaw/skills');
  expect(text).toContain('客户端根目录已存在');
  expect(text).toContain('不创建未安装客户端的根目录');
});
