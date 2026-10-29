# 双语口播稿（英文录音，中文辅助）

录音只用英文。中文是给你理解意思、找停顿、知道该点哪里的。

**全程不能出现在画面里：** 终端历史、API key、`.env` 文件、GitHub/Devpost/Nebius 账户页、桌面通知、私人文件夹路径、工作台页面最底部的 "Integration status" 面板（那段旧文字还写着 live review unverified，和你的口播矛盾）。

---

## 段 1 · 0:00–0:15 · 问题

**英文口播：** A drone simulation is flying home on low battery. One frame later, it switches to an evasive hold. If you're the operator, you need to know why — and you need proof, not a guess.

**中文意思：** 一架仿真无人机低电量返航，下一帧突然改成规避悬停。操作员需要知道为什么，而且要有证据。

**停顿提示：** "low battery." 后停半拍；"why —" 后停顿，"proof, not a guess" 放慢、加重。

**鼠标：** 不动，停在页面标题上。

**画面：** 工作台首页，大标题 "See why the next action changed."

---

## 段 2 · 0:15–0:35 · 介绍

**英文口播：** This is AegisLand Evidence Review. It's a Physical AI review tool, not a flight controller. It takes saved simulation evidence from our OpenCV project and lets you trace every decision back to the exact record it came from. Nothing here can send a command to an aircraft.

**中文意思：** 这是一个物理 AI 审查工具，不是飞控。它拿我们 OpenCV 项目保存的仿真证据，让你把每个决策追溯到原始记录。这里任何东西都不能给飞机发指令。

**停顿提示：** "not a flight controller." 后停；最后一句慢一点。

**鼠标：** 慢慢在左侧三个场景卡片上移过。

**画面：** 三个场景卡片 + 右上角 "3 / 230 / 0"。

---

## 段 3 · 0:35–1:45 · 真实运行演示（这 70 秒画面必须一直是工作台，不能切走）

**3a 英文：** Here's the low-battery intrusion run. At sequence 37 the planner is returning home.
**中文：** 这是低电量 + 入侵场景，第 37 步时规划器还在返航。
**鼠标：** 点左侧 **Low battery + intrusion** → 点 **Sequence 37**。
**画面：** 视频跳帧，右侧动作显示 return home。

**3b 英文：** At sequence 38, the video jumps to the exact frame, and the action changes to evade and hold. On the right is the original record: source line 39, its evidence ID, approval not required, and an execution flag that's true — in simulation. The check says it plainly: a positive flag does not prove hardware moved.
**中文：** 第 38 步，视频跳到对应帧，动作变成规避悬停。右边是原始记录：第 39 行、证据 ID、不需要审批、执行标志为真——但只是仿真。检查结果明确说：标志为真不代表硬件动了。
**停顿：** "source line 39" 读清楚；"— in simulation." 前停顿。
**鼠标：** 点 **Sequence 38**；鼠标依次停在 "Approval required: false"、"Execution flag: true"、"Hardware command sent: false"。
**画面：** 右侧 "evade and hold"、"Execution reported in simulation"、底部 "Validated citation: line 39 / c71390b01d39"。

**3c 英文：** I can open the untouched source line and the hash of the full trace, so nothing here is a rewritten summary.
**中文：** 可以打开原始那一行和整份 trace 的哈希，这里没有任何改写过的摘要。
**鼠标：** 稍微往下滚，点开 **Inspect the exact source record**。**只滚到这个卡片为止，不要再往下滚。**
**画面：** 展开的原始字段 + SHA-256。

**3d 英文：** And I can export this review as JSON, with the citation attached.
**中文：** 还可以把这次审查导出成 JSON，带着引用。
**鼠标：** 滚回上方，点 **Export selected review JSON ↓**。
**画面：** 浏览器下载提示（如果弹出下载栏，里面只能有这个文件名，不要露出下载文件夹路径）。

**3e 英文：** Now GPS loss in low light. Return-to-home isn't available, so the planner asks a human for approval — and it's still pending. At sequence 30, the system takes an enhanced second look. The approval state stays visible — never mistaken for permission.
**中文：** GPS 丢失 + 低光场景。返航不可用，所以规划器请求人工审批，而且还在等待中。第 30 步系统做了增强重新观测。审批状态一直显示着，绝不会被误当成已批准。
**鼠标：** 点 **GPS loss + low light** → **Sequence 22** → **Sequence 30**。
**画面：** "request human approval"、"Recorded approval: pending"、"Active re-observation: true"。

---

## 段 4 · 1:45–2:15 · Nebius Token Factory + NVIDIA Nemotron

**英文口播：** Where does AI come in? We send a small, bounded window of these records to NVIDIA Nemotron on Nebius Token Factory. Nemotron has one job: pick which record to review, and which check to run. In our recorded live review, it returned HTTP 200, finished cleanly, and cited line 39 — the same moment we just looked at. Our local code verified that citation against the real file.

**中文意思：** AI 在哪里？我们把一小段有边界的记录发给 Nebius Token Factory 上的 NVIDIA Nemotron。它只做一件事：选哪条记录、跑哪种检查。在我们记录的那次真实审查里，它返回 HTTP 200、正常结束、引用了第 39 行——正是刚才看的那一刻。本地代码对照真实文件验证了这个引用。

**停顿：** "Nebius Token Factory"、"NVIDIA Nemotron" 两个名字一定读清楚；"line 39 —" 后停顿。

**鼠标：** 切到浏览器另一个标签：GitHub 上的 `verification/attempt004_public_summary.json`，鼠标依次指 `http_status`、`model`、`finish_reason`、`"line": 39`、`citation_validation`。

**画面：** 只显示这个公开 JSON。**不能显示**：任何 receipt、request ID、API key、Nebius 控制台、账户邮箱。

---

## 段 5 · 2:15–2:40 · 意义

**英文口播：** The model points; our code checks. Malformed or uncited answers are rejected, and the model never gets a command channel. The OpenCV simulation is our earlier work; this hackathon, we built the review loop around it. For safety engineers and operators, that means fast answers they can verify.

**中文意思：** 模型负责指，代码负责查。格式错误或没引用的回答一律拒绝，模型永远拿不到指令通道。OpenCV 仿真是我们之前的工作，这次黑客松做的是外面这一圈审查闭环。对安全工程师和操作员来说，这意味着又快又能验证的答案。

**停顿：** "The model points; our code checks." 两半句之间停顿，这是金句。

**鼠标：** 切到 GitHub README，滚到 Architecture 图。

**画面：** 架构图。

---

## 段 6 · 2:40–2:50 · 收尾

**英文口播：** AegisLand: see why the next action changed. The code is on GitHub at Cyberchopin slash aegisland-nebius-2026. Thanks for watching.

**中文意思：** AegisLand：看清下一步为什么变了。代码在 GitHub 上。谢谢观看。

**鼠标：** 滚回 README 顶部。

**画面：** README 标题 + 徽章 + 仓库地址栏（地址栏只显示 github.com 链接）。
