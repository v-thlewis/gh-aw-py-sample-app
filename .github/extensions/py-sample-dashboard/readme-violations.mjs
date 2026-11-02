export function parseReadmeViolations(readme) {
  const lines = readme.split(/\r?\n/);
  const violations = [];
  let currentFile = "";

  for (const line of lines) {
    const fileHeader = line.match(/^###\s+`([^`]+)`/);
    if (fileHeader) {
      currentFile = fileHeader[1];
      continue;
    }

    if (/^#{1,3}\s/.test(line)) {
      currentFile = "";
      continue;
    }

    const violationLine = line.match(/^\-\s+\*\*([^*]+)\*\*:\s+(\d+)\s+violations?/i);
    if (violationLine && currentFile) {
      violations.push({
        file: currentFile,
        type: violationLine[1].trim(),
        count: Number(violationLine[2]),
      });
    }
  }

  return violations;
}
