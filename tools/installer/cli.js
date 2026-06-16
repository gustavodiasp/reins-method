#!/usr/bin/env node

// REINS Method installer — `npx reins-method install`
//
// Clones/updates ~/.reins, runs an interactive setup wizard (arrow-key
// selectable menus via @clack/prompts), then hands the collected answers to
// `bin/reins install --non-interactive` to do the actual file work. Day-to-day
// commands (`reins update`, `reins sync`, ...) remain a plain bash CLI with no
// runtime dependencies — Node is only needed for this installer.

const path = require('node:path');
const os = require('node:os');
const fs = require('node:fs');
const { execFileSync } = require('node:child_process');
const { Command } = require('commander');

const REINS_HOME = process.env.REINS_HOME || path.join(os.homedir(), '.reins');
const PKG_ROOT   = path.join(__dirname, '../..');
const LOCAL_BIN  = path.join(PKG_ROOT, 'bin', 'reins');
const REINS_BIN  = fs.existsSync(path.join(REINS_HOME, 'bin', 'reins'))
  ? path.join(REINS_HOME, 'bin', 'reins')
  : LOCAL_BIN;

async function getClack() {
  return import('@clack/prompts');
}

async function getColors() {
  return (await import('picocolors')).default;
}

async function printBanner() {
  const c = await getColors();
  const lines = [
    ['      ,~~_              ', '____  ___________   _______'],
    ['      |/\\ =_ _ ~       ', '/ __ \\/ ____/  _/ | / / ___/'],
    ['       _( )_( )\\~~    ', '/ /_/ / __/  / //  |/ /\\__ \\'],
    ['       \\,\\  _|\\ \\~~~ ', '/ _, _/ /____/ // /|  /___/ /'],
    ['          \\`   \\    ', '/_/ |_/_____/___/_/ |_//____/'],
    ['          `    `', ''],
  ];
  for (const [horse, reins] of lines) {
    console.log(c.green(horse) + c.greenBright(reins));
  }
  console.log('');
  console.log(c.dim(c.green('  Structured AI pair programming method')));
  console.log(c.dim(c.green('  ──────────────────────────────────────────────────')));
  console.log('  Agent-agnostic · stack-agnostic · globally installed');
  console.log('');
}


function readCurrentAgents() {
  const configPath = path.join(REINS_HOME, 'user', 'config.yaml');
  if (!fs.existsSync(configPath)) return [];
  const content = fs.readFileSync(configPath, 'utf8');
  const agentsBlock = content.match(/^agents:\n((?:[^\S\n]*- .+\n?)*)/m);
  if (agentsBlock) {
    return (agentsBlock[1].match(/- (.+)/g) || []).map(s => s.replace(/^- /, '').trim());
  }
  const agentScalar = content.match(/^agent:\s*(.+)/m);
  return agentScalar ? [agentScalar[1].trim()] : [];
}

const AGENT_OPTIONS = [
  { value: 'claude-code', label: 'Claude Code' },
  { value: 'copilot', label: 'GitHub Copilot CLI' },
  { value: 'codex', label: 'Codex CLI' },
  { value: 'gemini', label: 'Gemini CLI' },
  { value: 'aider', label: 'Aider' },
  { value: 'other', label: 'OpenCode / Cursor / Other' },
];

async function runInstall() {
  const clack = await getClack();

  await printBanner();

  const configPath = path.join(REINS_HOME, 'user', 'config.yaml');

  clack.intro('REINS Method setup');
  clack.note(
    'Arrow keys to navigate · Space to select/deselect · Enter to confirm · Esc or Ctrl+C to cancel',
    'How to use this menu',
  );

  if (fs.existsSync(configPath)) {
    const again = await clack.confirm({
      message: `REINS is already configured at ${REINS_HOME}. Re-run the wizard?`,
      initialValue: false,
    });
    if (clack.isCancel(again) || !again) {
      clack.outro('Nothing to do.');
      return;
    }
  }

  const agents = await clack.multiselect({
    message: 'Which AI coding agents do you use?',
    options: AGENT_OPTIONS,
    required: true,
  });
  if (clack.isCancel(agents)) {
    clack.cancel('Install cancelled.');
    process.exit(0);
  }

  const wantsStandards = await clack.confirm({
    message: 'Do you have company code standards to configure?',
    initialValue: false,
  });
  if (clack.isCancel(wantsStandards)) {
    clack.cancel('Install cancelled.');
    process.exit(0);
  }

  const wantsHistoric = await clack.confirm({
    message: 'Enable Historic Mode (performance tracking)?',
    initialValue: false,
  });
  if (clack.isCancel(wantsHistoric)) {
    clack.cancel('Install cancelled.');
    process.exit(0);
  }

  const adapterPath = await clack.text({
    message: 'Install an adapter pack now? Path to local pack (leave empty to skip):',
    placeholder: '(skip)',
    defaultValue: '',
  });
  if (clack.isCancel(adapterPath)) {
    clack.cancel('Install cancelled.');
    process.exit(0);
  }

  const language = await clack.text({
    message: 'Language to interact in (agent replies, skill/persona output)?',
    placeholder: 'English',
    defaultValue: 'English',
  });
  if (clack.isCancel(language)) {
    clack.cancel('Install cancelled.');
    process.exit(0);
  }

  const docLanguage = await clack.text({
    message: 'Language for documentation (code comments, docstrings, READMEs, etc.)?',
    placeholder: 'English',
    defaultValue: 'English',
  });
  if (clack.isCancel(docLanguage)) {
    clack.cancel('Install cancelled.');
    process.exit(0);
  }

  const args = [
    'install',
    '--non-interactive',
    `--from-package=${PKG_ROOT}`,
    ...agents.map(a => `--agent=${a}`),
    `--standards=${wantsStandards ? 'yes' : 'no'}`,
    `--historic=${wantsHistoric ? 'on' : 'off'}`,
    `--language=${language || 'English'}`,
    `--doc-language=${docLanguage || 'English'}`,
  ];
  if (adapterPath) args.push(`--adapter=${adapterPath}`);

  const spinner = clack.spinner();
  spinner.start('Configuring REINS Method');
  try {
    execFileSync(LOCAL_BIN, args, { stdio: 'pipe' });
    spinner.stop('Configured REINS Method');
  } catch (e) {
    spinner.stop('Configuration failed');
    process.stderr.write(e.stdout || '');
    process.stderr.write(e.stderr || '');
    process.exit(1);
  }

  if (wantsStandards) {
    const companyMd = path.join(REINS_HOME, 'user', 'standards', 'company.md');
    const editNow = await clack.confirm({
      message: `Open ${companyMd} in your editor now?`,
      initialValue: true,
    });
    if (!clack.isCancel(editNow) && editNow) {
      const editor = process.env.EDITOR || 'vi';
      try {
        execFileSync(editor, [companyMd], { stdio: 'inherit' });
      } catch {
        // non-fatal — user can edit it later
      }
    }
  }

  const c = await getColors();
  clack.note(
    [
      `REINS Method installed to ${REINS_HOME}`,
      'Restart your terminal/agent to activate the `reins` command,',
      'or reload your shell right now:',
      '',
      '  source ~/.zshrc     # zsh',
      '  source ~/.bashrc    # bash',
      '',
      'Then run:',
      '',
      '  reins status',
      '',
      'Optional companion tools (see README.md "Companion tools"):',
      `  ${c.bold('headroom')}   pip install "headroom-ai[all]"`,
      `  ${c.bold('graphify')}   pip install graphifyy`,
    ].join('\n'),
    'Done',
  );
  clack.outro('Getting started: reins status');
}

function runDelegated(cmd, args) {
  if (!fs.existsSync(path.join(REINS_HOME, 'bin', 'reins'))) {
    console.error(`Error: REINS Method is not installed at ${REINS_HOME}. Run "npx reins-method install" first.`);
    process.exit(1);
  }
  try {
    execFileSync(REINS_BIN, [cmd, ...args], { stdio: 'inherit' });
  } catch (e) {
    process.exit(e.status || 1);
  }
}

const program = new Command();
program
  .name('reins-method')
  .description('REINS Method installer — interactive setup for the agent-agnostic AI workflow')
  .version(require('../../package.json').version);

program
  .command('install', { isDefault: true })
  .description('Install or reconfigure REINS Method (interactive wizard)')
  .action(runInstall);

program
  .command('update')
  .description('Pull latest core and regenerate agent bridge files')
  .action(() => runDelegated('update', []));

program
  .command('uninstall')
  .description('Unhook REINS from your agent/shell, optionally delete ~/.reins')
  .action(() => runDelegated('uninstall', []));

program
  .command('agents')
  .description('Update which AI coding agents you use and re-wire')
  .action(runAgents);

program.parseAsync(process.argv);

async function runAgents() {
  const clack = await getClack();
  clack.intro('REINS — update agent selection');
  clack.note(
    'Arrow keys to navigate · Space to select/deselect · Enter to confirm · Esc or Ctrl+C to cancel',
    'How to use this menu',
  );

  const currentAgents = readCurrentAgents();
  const initialValues = currentAgents.filter(a => AGENT_OPTIONS.some(o => o.value === a));

  const agents = await clack.multiselect({
    message: 'Which AI coding agents do you use?',
    options: AGENT_OPTIONS,
    initialValues,
    required: true,
  });
  if (clack.isCancel(agents)) {
    clack.cancel('Cancelled.');
    process.exit(0);
  }

  const args = ['agents-set', ...agents.map(a => `--agent=${a}`)];
  try {
    execFileSync(REINS_BIN, args, { stdio: 'inherit' });
  } catch (e) {
    process.exit(e.status || 1);
  }
  clack.outro('Agent selection updated.');
}
