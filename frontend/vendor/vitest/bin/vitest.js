#!/usr/bin/env node
import path from 'node:path';
import process from 'node:process';
import { pathToFileURL } from 'node:url';
import { readdir } from 'node:fs/promises';
import { __getSuites, __reset } from '../index.js';

async function collectTestFiles(rootDir) {
  const entries = await readdir(rootDir, { withFileTypes: true }).catch((error) => {
    if (error && error.code === 'ENOENT') {
      return [];
    }
    throw error;
  });
  const files = [];
  for (const entry of entries) {
    const entryPath = path.join(rootDir, entry.name);
    if (entry.isDirectory()) {
      const nested = await collectTestFiles(entryPath);
      files.push(...nested);
    } else if (entry.isFile() && entry.name.endsWith('.test.js')) {
      files.push(entryPath);
    }
  }
  return files;
}

async function runTestFile(filePath) {
  __reset();
  await import(pathToFileURL(filePath).href);
  const suites = __getSuites();
  const results = [];
  for (const suite of suites) {
    for (const test of suite.tests) {
      try {
        await test.fn();
        results.push({ suite: suite.name, name: test.name, status: 'passed' });
      } catch (error) {
        results.push({ suite: suite.name, name: test.name, status: 'failed', error });
      }
    }
  }
  return results;
}

async function main(argv) {
  const [command, ...rest] = argv;
  if (!command || command === '--help' || command === '-h') {
    console.log('Usage: vitest run [--reporter <name>]');
    return 0;
  }
  if (command !== 'run') {
    console.error(`Unsupported command: ${command}`);
    return 1;
  }
  const filteredArgs = [];
  for (let index = 0; index < rest.length; index += 1) {
    const value = rest[index];
    if (value === '--reporter') {
      index += 1; // skip reporter name
      continue;
    }
    if (value.startsWith('--reporter=')) {
      continue;
    }
    filteredArgs.push(value);
  }
  if (filteredArgs.length > 0) {
    console.warn(`Ignoring unsupported arguments: ${filteredArgs.join(', ')}`);
  }

  const cwd = process.cwd();
  const testsDir = path.join(cwd, 'tests');
  const files = await collectTestFiles(testsDir);
  if (files.length === 0) {
    console.warn('No test files found.');
    return 0;
  }
  let failures = 0;
  for (const file of files) {
    const relativePath = path.relative(cwd, file);
    const results = await runTestFile(file);
    for (const result of results) {
      if (result.status === 'passed') {
        process.stdout.write('.');
      } else {
        failures += 1;
        process.stdout.write('F');
        console.error(`\n${relativePath} :: ${result.suite} :: ${result.name}`);
        if (result.error && result.error.stack) {
          console.error(result.error.stack);
        } else if (result.error && result.error.message) {
          console.error(result.error.message);
        }
      }
    }
  }
  process.stdout.write('\n');
  if (failures > 0) {
    console.error(`${failures} test(s) failed.`);
    return 1;
  }
  return 0;
}

const exitCode = await main(process.argv.slice(2));
process.exit(exitCode);
