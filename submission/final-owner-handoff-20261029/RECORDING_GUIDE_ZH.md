# 录制操作手册（零 Linux 基础版）

照着一步一步做就行。整个过程不会调用 Nebius，不需要 API key。

## 准备：先把 README 的 PR 合并

视频第 5、6 段要在 GitHub 上展示新的 README 和架构图。先打开 PR 并点 **Merge**，然后刷新仓库首页，确认能看到新的架构图，再开始录。

## 1. 打开 WSL

按 Windows 键，输入 `Ubuntu`（或 `WSL`），回车。出现一个黑色窗口，里面有 `$` 提示符，就说明打开了。

## 2. 进入仓库

如果你已经有一份干净的最新检出：

```bash
cd /home/shiyue1128/aegisland-nebius-submission-final-20261029
git status
```

`git status` 显示 `nothing to commit, working tree clean` 就可以继续。

如果这个文件夹不存在，就新拉一份（不会影响你原来的工作区）：

```bash
git clone https://github.com/Cyberchopin/aegisland-nebius-2026 /home/shiyue1128/aegisland-nebius-submission-final-20261029
cd /home/shiyue1128/aegisland-nebius-submission-final-20261029
```

## 3. 启动演示

```bash
python3 -B scripts/serve_review_workbench.py --directory demo --port 8090
```

窗口会停住不动，这是正常的，说明服务在运行。**录制期间不要关这个窗口。**

## 4. 打开浏览器

在 Windows 的 Chrome 或 Edge 里打开：

```
http://127.0.0.1:8090/
```

能看到 "See why the next action changed." 就成功了。

## 5. 端口被占用怎么办

如果第 3 步报错 `Address already in use`，先看看是谁占着：

```bash
curl -s http://127.0.0.1:8090/ | head -5
ss -ltnp | grep 8090
```

- 如果 `curl` 输出里有 AegisLand，说明工作台已经在跑了，直接用浏览器打开就行。
- 如果是别的东西，**不要随便杀进程**，换一个端口：把命令里的 `8090` 改成 `8091`，浏览器也改成 `http://127.0.0.1:8091/`。

## 6. 浏览器设置

- 缩放：按 `Ctrl` + `+`，调到 **110%–125%**，让字在视频里看得清。
- 隐藏书签栏：`Ctrl` + `Shift` + `B`。
- 关掉多余标签页，只留两个：工作台，和 GitHub 上的 `verification/attempt004_public_summary.json`。
- Windows 通知：右下角通知中心 → 打开 **请勿打扰**。
- 关掉微信、QQ、邮箱等会弹窗的软件。

## 7. 按时间表点击

完全按 `VIDEO_SHOT_LIST.md` 来点。重点：

1. 左侧点 **Low battery + intrusion**，再点 **Sequence 37**，然后点 **Sequence 38**。
2. 往下滚一点，点开 **Inspect the exact source record**。**只滚到这里，不要继续往下**，下面的 "Integration status" 面板是旧文字。
3. 滚回上面，点 **Export selected review JSON ↓**。
4. 左侧点 **GPS loss + low light**，再点 **Sequence 22**，然后点 **Sequence 30**。

## 8. 展示 Attempt 004 公开摘要

在第二个标签页打开：

```
https://github.com/Cyberchopin/aegisland-nebius-2026/blob/main/verification/attempt004_public_summary.json
```

用鼠标依次指：`"http_status": 200` → `"model"` → `"finish_reason": "stop"` → `"line": 39` → `"citation_validation": "PASS"`。

## 9. 不能出现在画面里的东西

- WSL 终端窗口（里面可能有你的用户名路径和历史命令）。录屏时只录浏览器窗口。
- 任何 API key、`.env` 文件、Nebius 控制台、GitHub 设置页、邮箱。
- 下载栏里的文件夹路径。
- 桌面和任务栏上的私人文件名。

## 10. 用 Windows 自带工具录屏

**方法 A：Xbox Game Bar（推荐）**
1. 先点一下浏览器窗口，让它在最前面。
2. 按 `Win` + `Alt` + `R` 开始录制，再按一次停止。这样只录当前窗口，不会录到终端。
3. 麦克风：按 `Win` + `G`，在"捕获"小窗里打开麦克风。
4. 视频保存在 `此电脑 → 视频 → 捕获`。

**方法 B：截图工具录屏**
按 `Win` + `Shift` + `R`，框选浏览器区域，点"开始"。

录音建议：用耳机麦克风，关掉风扇和空调，先试录 10 秒听一下效果。

## 11. 录完检查

- 时长**小于 3:00**（右键视频 → 属性 → 详细信息）。
- 0:35–1:45 这一整段都是工作台在运行，没有切走。
- 声音清楚，没有爆音。
- 全屏播放时，"line 39"、"c71390b01d39" 这些小字能看清。
- 从头到尾看一遍第 9 条列的东西，确认都没出现。

## 12. 上传 YouTube

1. 打开 https://studio.youtube.com → **创建** → **上传视频**。
2. 标题、描述直接复制 `YOUTUBE_COPY_EN.md`。
3. "是否为儿童内容"选 **否**。
4. 可见性选 **公开（Public）**。比赛允许的话可以用 **不公开列出（Unlisted）**，**绝对不能选私享（Private）**。
5. 等处理完，复制视频链接。
6. 打开浏览器**无痕窗口**（`Ctrl` + `Shift` + `N`），在没登录的状态下打开链接，确认能播放。

## 13. 关于 localhost

`http://127.0.0.1:8090/` 只能在你自己电脑上用来录屏。**不能**填进 Devpost 当作评委链接，评委打不开。Devpost 上给评委的是 GitHub 仓库链接和 YouTube 视频链接。

录完后，回到 WSL 窗口按 `Ctrl` + `C` 停止服务。
