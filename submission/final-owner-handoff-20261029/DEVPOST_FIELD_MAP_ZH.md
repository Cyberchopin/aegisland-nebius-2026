# Devpost 填写手册

英文内容全部来自 `DEVPOST_FINAL_EN.md`，直接复制对应段落。Devpost 上的所有内容必须是英文。

你已经有一个条目：https://devpost.com/software/aegisland-evidence-review-for-physical-ai ，在原条目上点 **Edit** 修改，不要新建。

## 字段对照

| Devpost 字段 | 复制哪一段 |
| --- | --- |
| Project name | `## Project name` |
| Elevator pitch / Tagline | `## One-line tagline` |
| About the project（故事正文） | 依次粘贴：Inspiration → What it does → How we built it → How Nebius Token Factory is used → How NVIDIA Nemotron is used → How OpenCV evidence is used → Challenges we ran into → Accomplishments → What we learned → What's next → Existing work and significant updates → Honest limitations。每段保留 `##` 标题，Devpost 支持 Markdown。 |
| Built with（标签） | `## Built With` 里的词，一个一个输入成标签：python, html, javascript, jsonl, sha-256, unittest, github-actions, nebius-token-factory, nvidia-nemotron, opencv |
| "Try it out" links | 只填 `https://github.com/Cyberchopin/aegisland-nebius-2026` |
| Video demo link | `【在这里粘贴你的 YouTube 链接】`（必须是公开或不公开列出，不能是私享） |
| Image gallery | 可以上传 `docs/assets/readme/workbench-intrusion-seq38.png` 和 `architecture-nebius-review.svg`（Devpost 不收 SVG 的话，用仓库里的截图或自己截一张架构图 PNG） |
| Track / Category | **Physical AI** |
| Repository URL | `https://github.com/Cyberchopin/aegisland-nebius-2026` |
| Testing instructions / How to test | `## Testing instructions` 整段 |
| Significant updates during the hackathon（如果有单独的框） | `## Existing work and significant updates during the hackathon` |
| Nebius / NVIDIA feedback（如果有单独的框） | `## Nebius / NVIDIA feedback` |

## Working demo / test build 怎么填

本项目**没有**长期在线的公共网址，这是事实，照实写。如果表单要求 demo 链接或 test build，填仓库地址，并在说明里粘贴：

> The demo is a local test build. Clone the repository and run `python -B scripts/serve_review_workbench.py --directory demo --port 8090`, then open http://127.0.0.1:8090/ on the same machine. Python 3.11+, standard library only, no API key. There is no always-on public endpoint.

**不要**把 `http://127.0.0.1:8090/` 单独填成"评委可访问链接"，评委打不开。

## 必须你本人确认的内容（我不能替你填）

- 参赛资格：年龄、所在国家/地区、学生身份等是否符合规则。
- 团队成员：名单是否完整、每个人是否都接受了邀请。
- 所有权声明：OpenCV 仿真视频、trace 和概念图是你本人或团队的作品，你有权提交。
- 如果表单问是否使用了 AI 辅助，按实际情况如实勾选。
- 你的姓名、邮箱、学校等个人信息。

## 最后确认提交状态

1. 全部填完后，滚到页面底部点 **Submit**（或 **Save & Submit**）。
2. 回到你的项目页，确认状态写的是 **Submitted**，而不是 **Draft**。
3. 在比赛的 **Project Gallery** 里能搜到你的项目。
4. 截图保存"Submitted"状态页面，并把项目网址存下来。
5. 截止时间是 **2026 年 10 月 30 日上午 10:00 PDT**，至少提前 1 小时提交完。
