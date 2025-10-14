function stripInterfaceBlocks(source) {
  const pattern = /(export\s+)?interface\s+[A-Za-z0-9_<> ,]*\{/g;
  return stripBlocks(source, pattern);
}

function stripTypeLiteralBlocks(source) {
  const pattern = /(export\s+)?type\s+[A-Za-z0-9_<> ,]+=\s*\{/g;
  return stripBlocks(source, pattern);
}

function stripBlocks(source, pattern) {
  let output = '';
  let lastIndex = 0;
  let match;
  while ((match = pattern.exec(source)) !== null) {
    output += source.slice(lastIndex, match.index);
    let index = match.index;
    let braceCount = 0;
    let started = false;
    while (index < source.length) {
      const char = source[index];
      if (char === '{') {
        braceCount += 1;
        started = true;
      } else if (char === '}') {
        braceCount -= 1;
        if (started && braceCount === 0) {
          index += 1;
          while (source[index] === ';' || source[index] === '\n' || source[index] === '\r') {
            index += 1;
          }
          break;
        }
      }
      index += 1;
    }
    lastIndex = index;
  }
  output += source.slice(lastIndex);
  return output;
}

function removeTypeAliases(source) {
  return source.replace(/export\s+type\s+[^=]+=.+?;\n?/g, '').replace(/type\s+[^=]+=.+?;\n?/g, '');
}

function removeImportTypeStatements(source) {
  return source.replace(/import\s+type[^;]+;\n?/g, '');
}

function removeAccessModifiers(source) {
  return source.replace(/\bpublic\s+/g, '').replace(/\bprivate\s+/g, '').replace(/\breadonly\s+/g, '');
}

function removeVariableAnnotations(source) {
  return source.replace(/(const|let|var)\s+([A-Za-z0-9_$]+)\s*:\s*([^=;\n]+)(?==)/g, '$1 $2 ');
}

function removeFunctionAnnotations(source) {
  let output = source.replace(/(\(|,)\s*([A-Za-z0-9_$]+)\s*:\s*([^),]+)/g, '$1 $2');
  output = output.replace(/\)\s*:\s*([^=\{]+)/g, ')');
  return output;
}

function removeTypeAssertions(source) {
  return source.replace(/\s+as\s+[A-Za-z0-9_\.\[\]\<\>\'"|&?, ]+/g, '');
}

function convertImports(source) {
  return source.replace(/import\s+{([^}]+)}\s+from\s+['"]([^'";]+)['"];?/g, (_, names, specifier) => {
    const normalized = names
      .split(',')
      .map((part) => part.trim())
      .filter(Boolean)
      .join(', ');
    return `const { ${normalized} } = require('${specifier}');`;
  });
}

function convertExports(source) {
  const exports = [];
  let output = source;

  output = output.replace(/export\s+function\s+([A-Za-z0-9_$]+)\s*\(/g, (_, name) => {
    exports.push({ local: name, exported: name });
    return `function ${name}(`;
  });

  output = output.replace(/export\s+class\s+([A-Za-z0-9_$]+)\s*/g, (_, name) => {
    exports.push({ local: name, exported: name });
    return `class ${name} `;
  });

  output = output.replace(/export\s+const\s+([A-Za-z0-9_$]+)\s*=\s*/g, (_, name) => {
    exports.push({ local: name, exported: name });
    return `const ${name} = `;
  });

  output = output.replace(/export\s+\{([^}]+)\}\s+from\s+['"]([^'";]+)['"];?/g, (_, names, specifier) => {
    const normalized = names
      .split(',')
      .map((part) => part.trim())
      .filter(Boolean);
    const mappings = normalized.map((entry) => {
      const [local, alias] = entry.split(/\s+as\s+/);
      return {
        local: (alias ? local : entry).trim(),
        exported: (alias ? alias : entry).trim()
      };
    });
    mappings.forEach((mapping) => exports.push(mapping));
    const destructured = mappings.map((mapping) => {
      return mapping.local === mapping.exported
        ? mapping.local
        : `${mapping.local}: ${mapping.exported}`;
    });
    return `const { ${destructured.join(', ')} } = require('${specifier}');`;
  });

  output = output.replace(/export\s+\{([^}]+)\};?/g, (_, names) => {
    names
      .split(',')
      .map((part) => part.trim())
      .filter(Boolean)
      .forEach((entry) => {
        const [local, alias] = entry.split(/\s+as\s+/);
        if (alias) {
          exports.push({ local: local.trim(), exported: alias.trim() });
        } else {
          exports.push({ local: entry, exported: entry });
        }
      });
    return '';
  });

  const assignments = exports
    .map(({ local, exported }) => `module.exports.${exported} = ${local};`)
    .join('\n');

  return `${output}\n${assignments}\n`;
}

export function transpileModule(source) {
  let output = source;
  output = removeImportTypeStatements(output);
  output = stripInterfaceBlocks(output);
  output = stripTypeLiteralBlocks(output);
  output = removeTypeAliases(output);
  output = removeAccessModifiers(output);
  output = removeVariableAnnotations(output);
  output = removeFunctionAnnotations(output);
  output = removeTypeAssertions(output);
  output = convertImports(output);
  output = convertExports(output);
  return { outputText: output };
}

export default {
  transpileModule
};
