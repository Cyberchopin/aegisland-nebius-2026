# License verification

The owner requested license selection. **MIT** is selected for this repository's
original integration code, synthetic fixtures and documentation. The root
[LICENSE](../../LICENSE) uses the standard MIT grant, notice condition and
warranty/liability disclaimer, with a copyright notice naming the
AegisLand contributors, not NVIDIA or Nebius. Its text was
checked against the [OSI MIT reference](https://opensource.org/license/mit).
SPDX identifier: `MIT`; OSI approved.

This permissive license suits a small reusable standard-library integration.
Adding it locally does not publish the project. License text cannot establish
contribution ownership; the owner must confirm distribution rights before release.
See [THIRD_PARTY_NOTICES.md](../../THIRD_PARTY_NOTICES.md).

| Material | Verification | Boundary |
| --- | --- | --- |
| Integration source/tests/docs/synthetic fixtures | Standard MIT license added; standard-library imports | Applies to original repository material, subject to any file notices |
| NVIDIA model | Model card identifies NVIDIA Nemotron Open Model License; official license page dated December 15, 2025 | No weights/model code bundled; MIT does not relicense the model |
| AegisLand core | Baseline `eda23d3` referenced; no core modules imported/copied | Pinned upstream license not established here; do not redistribute its assets without checking |
| Nebius | Hosted API and sanitized owner-run evidence | Service/account terms are separate |
| CI actions | Versioned references, no action implementations bundled | No third-party action code is relicensed |
| Video/screenshots | Runbook produces project-authored HTML and synthetic evidence displays | Use these screens and no unlicensed music or logo assets |

[NVIDIA's license](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-nemotron-open-model-license/)
allows use/distribution subject to its conditions and does not grant general
trademark rights. The [model card](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-BF16)
is a family reference, not proof of the serving checkpoint selected by Nebius.
The live response establishes the hosted API model ID only.

Before release: confirm rights in the contributions; retain MIT notices; review
applicable service/model terms and any assets added later; approve final media.
After an authorized push, verify GitHub detects MIT and judges can access the
complete source. Public license detection cannot be verified from unpushed files.
