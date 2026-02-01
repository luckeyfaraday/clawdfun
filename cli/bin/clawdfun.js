#!/usr/bin/env node

import { writeFileSync, mkdirSync, existsSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';

const command = process.argv[2];
const target = process.argv[3];

if (command === 'install' && target === 'router') {
  console.log('🦞 Clawd.fun | Initializing Agentic Router Skill...');
  
  const skillDir = join(homedir(), '.openclaw', 'skills', 'clawdfun');
  if (!existsSync(skillDir)) {
    mkdirSync(skillDir, { recursive: true });
  }

  const skillContent = `# Clawd.fun Router Skill
# Version 1.0.0

## Vision
Autonomous routing for AI agents to Pump.fun.

## Endpoints
- API: https://clawdfun-delta.vercel.app/api

## Commands
- launch: Routes a token mint to Pump.fun.
- trade: Buys/Sells on the bonding curve.
`;

  writeFileSync(join(skillDir, 'SKILL.md'), skillContent);
  
  console.log('✅ Success: Clawd.fun Router Skill installed at ~/.openclaw/skills/clawdfun/SKILL.md');
  console.log('🤖 You can now tell your agent: "Launch a token on Pump.fun via the Clawd.fun router"');
} else {
  console.log('Usage: npx clawdfun install router');
}
