# README visual assets

These files illustrate the README. None of them is new simulation, model or flight evidence.

| File | Bytes | SHA-256 | Meaning |
| --- | ---: | --- | --- |
| [aegisland-concept.png](aegisland-concept.png) | 2,307,796 | `fe649b9d6377c11c0a6ed88f8992e78655393ffbdd913f66eb73ebc47f06840a` | Owner-supplied AI concept artwork, copied byte for byte from [aegisland-opencv-2026](https://github.com/Cyberchopin/aegisland-opencv-2026/blob/main/docs/assets/readme/ASSETS.md). Illustration only; not flight footage, model output or evaluation evidence. |
| [workbench-intrusion-seq38.png](workbench-intrusion-seq38.png) | 528,451 | `7dc0312462ce5019cc50d3c8d469a4d56a86eb13063fa069f960683cb03035d6` | Headless-browser capture of the bundled offline workbench (`demo/`) at source line 39 / sequence 38 of the low-battery intrusion replay. The verdict shown is the deterministic check, not model output. |
| [workbench-gps-lowlight-seq30.png](workbench-gps-lowlight-seq30.png) | 521,778 | `c2a1f3b426a9c4a3df4e842c3edaf29a8f3c3045f13e09647264dc2530e34a5b` | Same workbench at source line 31 / sequence 30 of the GPS-loss + low-light replay (pending approval, active re-observation). Deterministic check, not model output. |
| [architecture-nebius-review.svg](architecture-nebius-review.svg) | 4,344 | `218454075f3534f5c21530b6ac7010544f6f8d3c5951c0996ffa322349621f0f` | Hand-drawn architecture diagram in the visual style of the OpenCV submission. Figures match `verification/attempt004_public_summary.json`. |
| [verification-summary.svg](verification-summary.svg) | 3,313 | `12f5669472cb4ae7aac388fb79d8f6aca58ebc8845b730ce41b042f15877ab85` | Presentation of existing records from `verification/attempt004_public_summary.json` and the retained Attempt 001–003 results. No test, inference or API call was run to draw it. |

The screenshots were taken from the local preview (`scripts/serve_review_workbench.py --directory demo`) and cropped to the three main panels. They show saved synthetic simulation only. The earlier capture `docs/assets/workbench-preview.jpg` is unchanged.
