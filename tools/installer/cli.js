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
const REPO_URL =
  process.env.REINS_REPO_URL || 'https://github.com/gustavodiasp/reins-method.git';

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

function ensureGit() {
  try {
    execFileSync('git', ['--version'], { stdio: 'ignore' });
  } catch {
    console.error('Error: git is required.');
    process.exit(1);
  }
}

function cloneOrPull() {
  if (fs.existsSync(path.join(REINS_HOME, '.git'))) {
    console.log(`REINS Method already installed at ${REINS_HOME} — pulling latest core...`);
    execFileSync('git', ['-C', REINS_HOME, 'pull', '--ff-only'], { stdio: 'inherit' });
  } else if (fs.existsSync(REINS_HOME)) {
    console.error(`Error: ${REINS_HOME} exists and is not a REINS git checkout. Move it aside first.`);
    process.exit(1);
  } else {
    console.log(`Cloning REINS Method to ${REINS_HOME}...`);
    execFileSync('git', ['clone', '--depth', '1', REPO_URL, REINS_HOME], { stdio: 'inherit' });
  }
  fs.chmodSync(path.join(REINS_HOME, 'bin', 'reins'), 0o755);
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
  ensureGit();
  cloneOrPull();

  const configPath = path.join(REINS_HOME, 'user', 'config.yaml');

  clack.intro('REINS Method setup');

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

  const agent = await clack.select({
    message: "What's your primary AI Coding Agent?",
    options: AGENT_OPTIONS,
  });
  if (clack.isCancel(agent)) {
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
    placeholder: 'english',
    defaultValue: 'english',
  });
  if (clack.isCancel(language)) {
    clack.cancel('Install cancelled.');
    process.exit(0);
  }

  const docLanguage = await clack.text({
    message: 'Language for documentation (code comments, docstrings, READMEs, etc.)?',
    placeholder: 'english',
    defaultValue: 'english',
  });
  if (clack.isCancel(docLanguage)) {
    clack.cancel('Install cancelled.');
    process.exit(0);
  }

  const args = [
    'install',
    '--non-interactive',
    `--agent=${agent}`,
    `--standards=${wantsStandards ? 'yes' : 'no'}`,
    `--historic=${wantsHistoric ? 'on' : 'off'}`,
    `--language=${language || 'english'}`,
    `--doc-language=${docLanguage || 'english'}`,
  ];
  if (adapterPath) args.push(`--adapter=${adapterPath}`);

  const spinner = clack.spinner();
  spinner.start('Configuring REINS Method');
  try {
    execFileSync(path.join(REINS_HOME, 'bin', 'reins'), args, { stdio: 'pipe' });
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

  clack.note(
    [
      `REINS Method installed to ${REINS_HOME}`,
      'Restart your terminal/agent to activate the `reins` command, then run:',
      '',
      '  reins status',
      '',
      'Optional companion tools (see README.md "Companion tools"):',
      '  - headroom: pip install "headroom-ai[all]"',
      '  - graphify: pip install graphifyy',
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
    execFileSync(path.join(REINS_HOME, 'bin', 'reins'), [cmd, ...args], { stdio: 'inherit' });
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

program.parseAsync(process.argv);
