
from __future__ import annotations
from collections import Counter

class RepositoryContextAgent:
    name = "repository_context"

    def analyze(self, artifact):
        imports = Counter()
        for source in artifact.files.values():
            for line in source.splitlines():
                line = line.strip()
                if line.startswith("import ") or line.startswith("from "):
                    imports[line.split()[1].split(".")[0]] += 1
        return {
            "repository": artifact.name,
            "test_count": len(artifact.tests),
            "file_count": len(artifact.files),
            "top_imports": imports.most_common(8),
            "github_metadata": artifact.github_metadata,
        }
