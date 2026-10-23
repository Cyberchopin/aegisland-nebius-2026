# Scope and external references

The root MIT license covers the original code, synthetic fixtures and documents
in this competition integration repository, subject to any explicit file notices.
It does not grant rights in external projects, services, trademarks or model weights.

| Reference | Use in this repository | License boundary |
| --- | --- | --- |
| AegisLand core, baseline `eda23d3` | Referenced architecture/provenance; no core module imported or copied | Its license and distribution rights are separate; do not add core assets without checking them |
| NVIDIA Nemotron 3 Super | Hosted text inference via Nebius; no model weights or model code distributed | NVIDIA Nemotron Open Model License, separate from this repository's MIT license |
| Nebius Token Factory | HTTP API and retained sanitized owner-run results | Account/service terms still apply |
| Python | Standard-library imports | Python runtime license is separate; no runtime bundled |
| GitHub Actions | `actions/checkout@v4`, `actions/setup-python@v5`, `actions/upload-artifact@v4` references | Actions are fetched by CI; no action implementation bundled |

[NVIDIA's model license](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-nemotron-open-model-license/)
was reviewed as the December 15, 2025 version. This project does not relicense
the model. Names identify technologies used; no endorsement is claimed. The
submission uses plain text and project-authored visuals, without stock music or
third-party logo assets. Any later distributed third-party assets need their own
rights/notice review.
