# NNAGA Plugin Repository

Standalone catalog and payload repository for NNAGA. `index.toml` is the
schema-2 listing; package manifests and payloads are fetched lazily by the
application. Run `maintenance/generate_index.py` after adding or changing a
manifest.

The catalog metadata and maintenance script are licensed under the GNU
General Public License, version 3 or later. Payload licenses belong to their
respective authors and are recorded in each manifest. The included REAPER
stock JSFX files are redistributed only where the source contains an explicit
GPL grant (IXix, GPL-marked Liteon, and LOSER MGA JS Limiter files); their
source notices are preserved verbatim.
