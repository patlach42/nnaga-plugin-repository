# NNAGA Plugin Repository

Standalone catalog and payload repository for NNAGA. `index.toml` is the
schema-2 listing; package manifests and payloads are fetched lazily by the
application. Run `maintenance/generate_index.py` after adding or changing a
manifest.

Every package manifest records a canonical upstream `source` URL and a
purpose-focused description. The generated schema-2 index mirrors both fields
so clients can show provenance without downloading full manifests.

The catalog metadata and maintenance script are licensed under the GNU
General Public License, version 3 or later. Payload licenses belong to their
respective authors and are recorded in each manifest. The included REAPER 7.77
stock JSFX files come from the official REAPER distribution and are
redistributed only where the source contains an explicit GPL grant (IXix,
GPL-marked Liteon, and LOSER MGA JS Limiter files); their source notices are
preserved verbatim.
