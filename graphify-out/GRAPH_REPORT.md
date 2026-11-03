# Graph Report - local-whisper  (2026-11-03)

## Corpus Check
- Corpus is ~803 words - fits in a single context window. You may not need a graph.

## Summary
- 30 nodes · 53 edges · 6 communities (2 shown, 4 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- CLI & File Discovery
- Transcription Engine
- SRT Output & Flow
- Model Loading & CUDA
- CUDA Error Handling
- Package Root

## God Nodes (most connected - your core abstractions)
1. `main()` - 9 edges
2. `transcribe_file()` - 7 edges
3. `load_model()` - 5 edges
4. `collect_videos()` - 4 edges
5. `existing_subtitle()` - 4 edges
6. `segments_to_srt()` - 4 edges
7. `_is_cuda_error()` - 4 edges
8. `_try_cuda()` - 4 edges
9. `format_timestamp()` - 2 edges
10. `_add_cuda12_to_path()` - 2 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `_is_cuda_error()`  [EXTRACTED]
  local_whisper/cli.py → local_whisper/transcriber.py
- `main()` --calls--> `load_model()`  [EXTRACTED]
  local_whisper/cli.py → local_whisper/transcriber.py
- `main()` --calls--> `transcribe_file()`  [EXTRACTED]
  local_whisper/cli.py → local_whisper/transcriber.py
- `main()` --calls--> `collect_videos()`  [EXTRACTED]
  local_whisper/cli.py → local_whisper/files.py
- `main()` --calls--> `existing_subtitle()`  [EXTRACTED]
  local_whisper/cli.py → local_whisper/files.py

## Import Cycles
- None detected.

## Communities (6 total, 4 thin omitted)

### Community 0 - "CLI & File Discovery"
Cohesion: 0.40
Nodes (3): main(), collect_videos(), existing_subtitle()

### Community 2 - "SRT Output & Flow"
Cohesion: 0.40
Nodes (3): format_timestamp(), segments_to_srt(), transcribe_file()

## Knowledge Gaps
- **1 isolated node(s):** `local-whisper`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 8 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `transcribe_file()` connect `SRT Output & Flow` to `CLI & File Discovery`, `Transcription Engine`, `Model Loading & CUDA`?**
  _High betweenness centrality (0.137) - this node is a cross-community bridge._
- **What connects `local-whisper` to the rest of the system?**
  _1 weakly-connected nodes found - possible missing edges._
- **Why does `main()` connect `CLI & File Discovery` to `SRT Output & Flow`, `Model Loading & CUDA`, `CUDA Error Handling`?**
  _High betweenness centrality (0.080) - this node is a cross-community bridge._
- **Why does `_is_cuda_error()` connect `CUDA Error Handling` to `CLI & File Discovery`, `Transcription Engine`?**
  _High betweenness centrality (0.071) - this node is a cross-community bridge._