import assert from 'node:assert/strict';
import { existsSync, readFileSync, realpathSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { pathToFileURL } from 'node:url';

const [native, repository, home] = process.argv.slice(2);
const { loadSkills, formatSkillsForPrompt } = await import(pathToFileURL(join(native, 'dist/core/skills.js')));
const manifest = JSON.parse(readFileSync(join(repository, 'PROVENANCE.json'), 'utf8'));
const installed = join(home, '.pi/agent/skills');
const result = loadSkills({ cwd: home, agentDir: join(home, '.pi/agent'),
  skillPaths: [installed, join(repository, 'skills')], includeDefaults: false });
assert.deepEqual(result.skills.map(s => s.name).sort(), manifest.skills.map(s => s.name).sort());
assert.equal(result.diagnostics.length, 0, JSON.stringify(result.diagnostics));
const prompt = formatSkillsForPrompt(result.skills);
for (const skill of result.skills) {
  const metadataPath = join(repository, 'skills', skill.name, 'agents/openai.yaml');
  const metadata = existsSync(metadataPath) ? readFileSync(metadataPath, 'utf8') : '';
  const explicit = metadata.includes('allow_implicit_invocation: false');
  assert.equal(skill.disableModelInvocation, explicit, skill.name);
  assert.equal(prompt.includes(`<name>${skill.name}</name>`), !explicit, skill.name);
  assert.equal(realpathSync(skill.filePath), realpathSync(join(repository, 'skills', skill.name, 'SKILL.md')));
}
const owner = result.skills.find(s => s.name === 'codebase-design');
assert.ok(readFileSync(join(dirname(owner.filePath), 'references/experience-and-interfaces.md'), 'utf8'));
assert.ok(readFileSync(join(dirname(owner.filePath), '../ci-maintenance/references/setup-contracts.md'), 'utf8'));
console.log(`Pi native loader: ${result.skills.length} skills; policy, deduplication, and filesystem resource reads passed`);
