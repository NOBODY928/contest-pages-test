# 竞赛资讯聚合网站 V4.0 项目交接手册

## 1. 项目概述

本项目是一个静态竞赛资讯聚合网站，当前本地仓库路径为：

```powershell
C:\Users\NOBODY2025\Desktop\contest-pages-test
```

网站面向需要快速查看高校竞赛入口、竞赛标签、当前状态和官网链接的读者。当前首页为卡片式布局，支持竞赛搜索、状态胶囊显示、官网跳转按钮和宝可梦图片背景。

当前线上主访问地址记录为：

```text
https://contest.zihao.me
```

当前仓库未发现 `README.md` 文件。项目说明主要需要依赖源码、配置文件和本交接手册。

当前源码中存在中文乱码现象，主要出现在 `build.py`、`contests.yaml`、`sources.yaml`、`templates/index.html.j2`、`index.html`、`data.json` 和 `details` 下的页面文本中。该现象会影响后续维护和页面展示，属于需要后续修正的风险项。

## 2. 当前技术架构

当前项目链路可以概括为：

```text
Windows 本地开发
→ GitHub 仓库
→ Cloudflare Pages 自动部署
→ contest.zihao.me 在线访问
→ 阿里云 ECS 作为辅助抓取、构建、提交环境
```

Windows 本地开发环境负责编辑 `contests.yaml`、`templates/index.html.j2`、`build.py` 和静态图片资源，并运行 Python 构建命令生成 `data.json` 与 `index.html`。

GitHub 仓库地址为：

```text
https://github.com/NOBODY928/contest-pages-test.git
```

当前本地分支为：

```text
main
```

Cloudflare Pages 当前从源码内容推断用于托管静态页面。首页模板中存在 Cloudflare Pages 托管提示，但仓库内未发现 Cloudflare 配置文件。Cloudflare 控制台项目名称、构建命令、输出目录等当前源码中未确认。

阿里云 ECS 相关逻辑存在于：

```text
C:\Users\NOBODY2025\Desktop\contest-pages-test\run.sh
```

该脚本写死 ECS 上的项目路径：

```bash
/root/contest-pages-test
```

该脚本会执行 `git pull --rebase origin main`、运行 `/root/contest-pages-test/venv/bin/python build.py`、暂存生成内容、自动提交并推送到 GitHub。是否已配置 cron 定时任务，当前源码中未确认。

## 3. 当前目录结构

当前仓库根目录真实结构如下：

```text
C:\Users\NOBODY2025\Desktop\contest-pages-test
├─ .git\
├─ details\
├─ parsers\
├─ static\
│  └─ images\
├─ templates\
│  └─ index.html.j2
├─ .gitignore
├─ build.py
├─ build.py.2026-01-13_104828
├─ build.py.bak.2025-12-17_165115
├─ build.py.bak.2025-12-17_170007
├─ build.py.bak.2026-01-12_110826
├─ build.py.bak.importfix.2025-12-17_171746
├─ build.py.legacy.2026-01-11_212239
├─ contests.yaml
├─ data.json
├─ index.html
├─ run.sh
├─ run.sh.2026-01-13_103219
├─ run.sh.bak.2026-01-13_095726
├─ sources.yaml
└─ sources.yaml.bak.2025-12-17_170015
```

重点目录和文件说明如下：

- `C:\Users\NOBODY2025\Desktop\contest-pages-test\build.py`：当前主构建脚本。
- `C:\Users\NOBODY2025\Desktop\contest-pages-test\contests.yaml`：当前竞赛数据源。
- `C:\Users\NOBODY2025\Desktop\contest-pages-test\sources.yaml`：额外数据源配置，当前主 `build.py` 未读取。
- `C:\Users\NOBODY2025\Desktop\contest-pages-test\templates\index.html.j2`：首页 Jinja2 模板。
- `C:\Users\NOBODY2025\Desktop\contest-pages-test\static\images`：首页卡片背景图片目录，当前包含 50 个 PNG 文件。
- `C:\Users\NOBODY2025\Desktop\contest-pages-test\details`：详情页目录，当前包含 51 个 HTML 文件。
- `C:\Users\NOBODY2025\Desktop\contest-pages-test\data.json`：构建产物，用于保存竞赛聚合数据。
- `C:\Users\NOBODY2025\Desktop\contest-pages-test\index.html`：构建产物，Cloudflare Pages 静态部署的首页入口。
- `C:\Users\NOBODY2025\Desktop\contest-pages-test\run.sh`：ECS 自动同步、构建、提交、推送脚本。

## 4. 核心文件说明

`C:\Users\NOBODY2025\Desktop\contest-pages-test\build.py`

作用：读取 `contests.yaml`，访问竞赛官网抓取状态和最新动态，将 YAML 配置与抓取结果合并，生成 `data.json` 和 `index.html`。

是否建议手动修改：谨慎修改。修改前需要备份。

修改风险：会影响所有竞赛数据生成、首页渲染和 ECS 自动构建流程。

`C:\Users\NOBODY2025\Desktop\contest-pages-test\contests.yaml`

作用：维护竞赛列表、竞赛名称、官网地址、标签、可选 logo 路径和 parser 字段。

是否建议手动修改：建议作为日常维护入口。

修改风险：YAML 缩进错误、字段漏冒号、中文编码异常会导致构建失败或页面内容异常。

`C:\Users\NOBODY2025\Desktop\contest-pages-test\sources.yaml`

作用：保存额外 sources 配置，包含 `demo` 和 `icpc_wf_schedule` 两个 source。

是否建议手动修改：当前主构建流程未读取，修改前需要确认是否有旧脚本或 parser 使用。

修改风险：当前源码中未确认。

`C:\Users\NOBODY2025\Desktop\contest-pages-test\templates\index.html.j2`

作用：定义首页 HTML、CSS、Jinja2 循环、卡片布局、搜索逻辑、状态逻辑、官网链接映射和宝可梦图片列表。

是否建议手动修改：可以修改，但修改后必须重新运行 `build.py`。

修改风险：Jinja2 语法错误会导致 `index.html` 无法生成。

`C:\Users\NOBODY2025\Desktop\contest-pages-test\static\images`

作用：保存首页卡片背景图片。当前模板硬编码读取 50 个 PNG 文件名。

是否建议手动修改：可新增、替换图片，但新增图片后必须同步修改模板中的 `pokemon_images` 列表。

修改风险：文件名不一致、空格不一致、大小写不一致会导致图片不显示。

`C:\Users\NOBODY2025\Desktop\contest-pages-test\details`

作用：保存详情页 HTML。当前首页模板未发现详情页入口按钮。

是否建议手动修改：当前主页面未链接详情页，修改前应确认未来是否恢复详情页入口。

修改风险：当前源码中未确认。

`C:\Users\NOBODY2025\Desktop\contest-pages-test\data.json`

作用：构建产物，保存最终竞赛数据列表。

是否建议手动修改：不建议作为唯一修改入口。

修改风险：重新运行 `build.py` 后会被覆盖。

`C:\Users\NOBODY2025\Desktop\contest-pages-test\index.html`

作用：构建产物，浏览器和 Cloudflare Pages 实际访问的首页文件。

是否建议手动修改：不建议作为唯一修改入口。

修改风险：重新运行 `build.py` 后会被模板覆盖。

`C:\Users\NOBODY2025\Desktop\contest-pages-test\run.sh`

作用：ECS 自动运行脚本，执行拉取、构建、提交、推送。

是否建议手动修改：谨慎修改。

修改风险：会影响 ECS 自动构建和推送。

## 5. contests.yaml 数据规范

`contests.yaml` 当前是一个 YAML 列表，每个竞赛条目常见字段如下：

```yaml
- id: cpipc_smart_city
  name: 竞赛名称
  homepage: https://example.com/
  logo: static/images/example.png
  tags: [标签1, 标签2]
  parser: parsers.example
```

字段含义如下：

- `id`：竞赛唯一标识。`build.py` 用于拼接默认 CPIPC 地址，模板用状态映射和官网链接映射间接识别竞赛。
- `name`：竞赛名称。首页卡片标题来自该字段。
- `homepage`：竞赛官网地址。`build.py` 抓取时优先使用该字段，并写入 `data.json` 的 `url`。
- `logo`：传统 logo 路径。当前首页模板未直接使用该字段作为卡片背景。
- `tags`：标签数组。首页卡片显示为 `#标签`，搜索也会检索标签。
- `parser`：parser 模块路径。当前主 `build.py` 未动态加载该字段。

新增竞赛的基本步骤如下：

```powershell
cd C:\Users\NOBODY2025\Desktop\contest-pages-test
notepad C:\Users\NOBODY2025\Desktop\contest-pages-test\contests.yaml
```

在文件末尾新增一个条目，保持两个空格缩进：

```yaml
- id: example_contest
  name: 示例竞赛
  homepage: https://example.com/
  tags: [示例, 综合]
  parser: null
```

修改竞赛名称时，只修改该竞赛条目的 `name` 字段。由于模板中存在 `contest_id_by_name` 映射，若该竞赛依赖名称映射状态或官网地址，还需要同步检查：

```text
C:\Users\NOBODY2025\Desktop\contest-pages-test\templates\index.html.j2
```

修改标签时，只修改 `tags` 数组。标签会影响卡片展示和搜索。

修改官网链接时，需要注意两个位置：

- `C:\Users\NOBODY2025\Desktop\contest-pages-test\contests.yaml` 中的 `homepage`
- `C:\Users\NOBODY2025\Desktop\contest-pages-test\templates\index.html.j2` 中的 `officialUrlMap` 或 `officialUrlByName`

当前首页“查看官网”按钮优先使用模板内映射，不完全依赖 `contests.yaml` 的 `homepage`。

## 6. build.py 构建流程

当前主脚本路径为：

```text
C:\Users\NOBODY2025\Desktop\contest-pages-test\build.py
```

当前 `build.py` 的主流程如下：

1. 导入 `requests`、`BeautifulSoup`、`urllib3`、`json`、`yaml`、`jinja2` 等依赖。
2. 禁用 SSL 警告。
3. 创建带重试机制的 HTTP session。
4. 读取：

```text
C:\Users\NOBODY2025\Desktop\contest-pages-test\contests.yaml
```

5. 遍历每一个竞赛条目。
6. 调用 `get_data(comp_id, comp_name, homepage)` 抓取官网页面。
7. 将 YAML 字段与抓取字段合并为 `final_data`。
8. 写入：

```text
C:\Users\NOBODY2025\Desktop\contest-pages-test\data.json
```

9. 加载模板目录：

```text
C:\Users\NOBODY2025\Desktop\contest-pages-test\templates
```

10. 渲染模板：

```text
C:\Users\NOBODY2025\Desktop\contest-pages-test\templates\index.html.j2
```

11. 写入首页：

```text
C:\Users\NOBODY2025\Desktop\contest-pages-test\index.html
```

当前 `build.py` 未发现写入 `details` 目录的逻辑。`details` 中的页面可能来自旧版构建脚本或手工生成，当前源码中未确认。

`data.json` 的主要字段由 `build.py` 生成：

```json
{
  "name": "竞赛名称",
  "url": "官网地址",
  "logo": "logo 路径",
  "tags": ["标签"],
  "status": {
    "text": "状态文本",
    "color": "状态颜色"
  },
  "info_grid": []
}
```

当前首页实际状态显示主要由模板内 JavaScript 的 `activeUntilMap` 和 `endedUntilMap` 决定，不直接使用 `data.json` 中的 `status.text`。

## 7. 首页模板 templates/index.html.j2 说明

首页模板路径为：

```text
C:\Users\NOBODY2025\Desktop\contest-pages-test\templates\index.html.j2
```

模板负责生成完整首页，包含 HTML、CSS、Jinja2 和 JavaScript。

卡片布局使用 CSS Grid，桌面端 3 列，中等屏幕 2 列，手机端 1 列。每张卡片使用 `.tile`，固定高度约 360px，移动端约 320px。

搜索栏位于顶部，输入框 ID 为：

```text
contestSearch
```

状态胶囊元素为：

```html
<div class="status-pill is-upcoming" data-status-pill>未开始</div>
```

实际状态文本和颜色由 JavaScript 在浏览器端运行后覆盖。

宝可梦背景图由模板内 `pokemon_images` 列表控制。每个竞赛按循环顺序取图：

```jinja2
{% set pokemon_img = pokemon_images[i % (pokemon_images|length)] %}
```

背景图片路径写入卡片内联样式：

```html
--card-image: url('/static/images/{{ pokemon_img }}');
```

官网按钮由 `official_url` 决定。`official_url` 的优先级如下：

1. `officialUrlMap.get(contest_id)`
2. `officialUrlByName.get(item.name)`
3. `item.homepage`
4. `item.url`

当前首页模板未发现常规详情页入口。全国大学生数学建模竞赛存在额外按钮，条件为：

```jinja2
{% if contest_id == 'cumcm' %}
```

按钮链接为：

```text
https://dxs.moe.gov.cn/zx/hd/sxjm/sxjmstjp/
```

## 8. 搜索功能说明

搜索功能在首页前端实时执行，不需要重新请求服务器。

搜索框输入时触发：

```javascript
input.addEventListener('input', filterCards);
```

每张卡片的搜索内容来自 `data-search` 属性。模板生成 `data-search` 时包含：

- `item.name`
- `contest_id`
- `item.tags`
- `item.info_grid` 中的 `value`

搜索匹配方式为小写字符串包含：

```javascript
haystack.includes(query)
```

无结果时显示：

```text
未找到匹配的竞赛
```

修改搜索逻辑应编辑：

```text
C:\Users\NOBODY2025\Desktop\contest-pages-test\templates\index.html.j2
```

修改后必须重新运行 `build.py` 生成新的 `index.html`。

## 9. 状态系统说明

首页状态系统有三种状态：

- 未开始
- 正在进行
- 已结束

对应 CSS 类如下：

- `is-upcoming`：灰色背景。
- `is-active`：绿色背景。
- `is-ended`：红色背景。

状态计算逻辑在模板底部 JavaScript 中。核心配置为：

```javascript
const activeUntilMap = {
  cpipc_math_modeling: '2026-08-16',
  cpipc_electronics: '2026-08-16',
  cpipc_chips: '2026-08-16',
  cpipc_rural_revitalization: '2026-08-16',
  cpipc_fintech: '2026-08-16',
  cpipc_aircraft: '2026-08-16',
  cpipc_ai: '2026-08-16',
  cpipc_cyber_security: '2026-08-16',
  challenge_cup_startup: '2026-08-16',
  software_design: '2026-08-16',
  iot_design: '2026-08-16',
  xuechuang_cup: '2026-08-16',
  statistics_modeling: '2026-08-16',
  software_cup: '2026-08-16',
  photo_design: '2026-08-16',
  embedded_chip: '2026-08-16'
};
```

```javascript
const endedUntilMap = {
  cpipc_public_admin: '2026-08-16',
  icpc: '2026-08-16',
  info_security_ctf: '2026-08-16'
};
```

自动切换规则如下：

- 如果竞赛 ID 在 `activeUntilMap` 中，且当前日期不晚于配置日期，则显示“正在进行”。
- 如果竞赛 ID 在 `activeUntilMap` 中，当前日期晚于配置日期但不超过配置日期后 2 个月，则显示“已结束”。
- 如果竞赛 ID 在 `activeUntilMap` 中，当前日期超过配置日期后 2 个月，则显示“未开始”。
- 如果竞赛 ID 在 `endedUntilMap` 中，且当前日期不晚于配置日期，则显示“已结束”。
- 如果不在两个映射表中，则显示“未开始”。

状态维护位置为：

```text
C:\Users\NOBODY2025\Desktop\contest-pages-test\templates\index.html.j2
```

## 10. 官网链接系统说明

“查看官网”按钮绑定逻辑位于：

```text
C:\Users\NOBODY2025\Desktop\contest-pages-test\templates\index.html.j2
```

主要维护位置为：

- `contest_id_by_name`
- `officialUrlMap`
- `officialUrlByName`
- `contests.yaml` 中的 `homepage`

当前模板内的 `officialUrlMap` 包含多个竞赛 ID 到官网地址的硬编码映射。该映射会优先于 `contests.yaml` 中的 `homepage`。

全国大学生数学建模竞赛存在特殊按钮，条件为 `contest_id == 'cumcm'`。该按钮文本为“赛题讲评”，链接为：

```text
https://dxs.moe.gov.cn/zx/hd/sxjm/sxjmstjp/
```

如果官网按钮错误，应优先检查模板中的 `officialUrlMap`，其次检查 `contest_id_by_name` 是否能正确把竞赛名称映射到竞赛 ID，最后检查 `contests.yaml` 的 `homepage`。

## 11. 宝可梦图片系统说明

图片放置目录为：

```text
C:\Users\NOBODY2025\Desktop\contest-pages-test\static\images
```

当前目录包含 50 个 PNG 文件。文件名示例：

```text
C:\Users\NOBODY2025\Desktop\contest-pages-test\static\images\0003 Venusaur Mega.png
C:\Users\NOBODY2025\Desktop\contest-pages-test\static\images\0006 Charizard Mega X.png
C:\Users\NOBODY2025\Desktop\contest-pages-test\static\images\0719 Diancie Mega.png
```

当前命名方式为：

```text
编号 英文名称 形态.png
```

新增图片步骤如下：

1. 将 PNG 文件放入：

```text
C:\Users\NOBODY2025\Desktop\contest-pages-test\static\images
```

2. 打开模板：

```powershell
notepad C:\Users\NOBODY2025\Desktop\contest-pages-test\templates\index.html.j2
```

3. 在 `pokemon_images` 列表中加入完整文件名。
4. 运行构建命令生成新首页。

替换图片时，推荐保持原文件名不变。保持文件名不变时，模板无需修改。

## 12. Windows 本地开发环境

当前推荐开发方式：

- VS Code 最新版。
- Codex 插件。
- 本地 Git 仓库。
- Windows PowerShell。
- `mywindows_env` 虚拟环境。

本地仓库路径为：

```powershell
C:\Users\NOBODY2025\Desktop\contest-pages-test
```

进入项目目录：

```powershell
cd C:\Users\NOBODY2025\Desktop\contest-pages-test
```

激活虚拟环境命令：

```powershell
& "C:\Users\NOBODY2025\Desktop\mywindows_env\Scripts\Activate.ps1"
```

构建命令：

```powershell
C:\Users\NOBODY2025\Desktop\mywindows_env\Scripts\python.exe build.py
```

当前检查结果：`C:\Users\NOBODY2025\Desktop\mywindows_env\Scripts\python.exe` 启动失败，错误指向不存在的 WindowsApps Python 路径。后续维护前需要修复或重建该虚拟环境。

如需重建虚拟环境，步骤示例为：

```powershell
cd C:\Users\NOBODY2025\Desktop
py -3 -m venv C:\Users\NOBODY2025\Desktop\mywindows_env
```

安装依赖示例：

```powershell
C:\Users\NOBODY2025\Desktop\mywindows_env\Scripts\python.exe -m pip install requests beautifulsoup4 urllib3 pyyaml jinja2
```

是否存在完整 `requirements.txt`，当前源码中未确认。

## 13. 本地预览流程

本地预览推荐使用 VS Code 的 Live Server 扩展。

步骤如下：

1. 用 VS Code 打开目录：

```powershell
code C:\Users\NOBODY2025\Desktop\contest-pages-test
```

2. 修改 `contests.yaml` 或 `templates/index.html.j2`。
3. 运行构建命令：

```powershell
cd C:\Users\NOBODY2025\Desktop\contest-pages-test
C:\Users\NOBODY2025\Desktop\mywindows_env\Scripts\python.exe build.py
```

4. 在 VS Code 中打开：

```text
C:\Users\NOBODY2025\Desktop\contest-pages-test\index.html
```

5. 使用 Live Server 打开预览。

修改模板后必须重新运行 `build.py`，原因是浏览器打开的是生成后的 `index.html`，不是模板文件 `templates/index.html.j2`。

`index.html` 是生成产物，不应作为唯一长期维护入口。

## 14. Git 提交流程

标准提交流程如下：

```powershell
cd C:\Users\NOBODY2025\Desktop\contest-pages-test
git status
git add .
git commit -m "说明"
git push origin main
```

每一步用途如下：

- `git status`：查看哪些文件被修改、哪些文件尚未暂存。
- `git add .`：把当前目录下的修改加入暂存区。
- `git commit -m "说明"`：把暂存区内容保存为一次本地提交。
- `git push origin main`：把本地 `main` 分支推送到 GitHub。

提交前应确认未误提交虚拟环境、日志和缓存文件。`.gitignore` 当前已忽略：

```text
venv/
__pycache__/
*.pyc
cron.run.log
*.log
```

## 15. GitHub 与 Token 登录说明

当前远端仓库为：

```text
https://github.com/NOBODY928/contest-pages-test.git
```

HTTPS 推送到 GitHub 时，可能需要 GitHub Personal Access Token。Token 通常作为密码使用，普通 GitHub 登录密码可能无法用于命令行推送。

如果 `git push origin main` 被拒绝，常见原因是 GitHub 远端已有新的提交，本地分支落后。

处理流程如下：

```powershell
cd C:\Users\NOBODY2025\Desktop\contest-pages-test
git pull --rebase origin main
git push origin main
```

`git pull --rebase origin main` 会先拉取远端最新提交，再把本地提交放到最新提交之后。若发生冲突，需要先解决冲突，再继续 rebase。

## 16. Rebase 冲突案例

项目中曾出现 `index.html` 冲突的维护场景。`index.html` 是生成产物，通常由 `templates/index.html.j2` 和 `contests.yaml` 重新生成。

谨慎处理步骤如下：

```powershell
cd C:\Users\NOBODY2025\Desktop\contest-pages-test
git status
```

打开冲突文件，确认冲突区域：

```powershell
notepad C:\Users\NOBODY2025\Desktop\contest-pages-test\index.html
```

如果冲突只发生在生成产物，一般原则是优先保留最新模板和最新数据重新生成后的 `index.html`。在重新生成前，需要先确认 `templates/index.html.j2` 和 `contests.yaml` 未丢失有效修改。

重新生成：

```powershell
cd C:\Users\NOBODY2025\Desktop\contest-pages-test
C:\Users\NOBODY2025\Desktop\mywindows_env\Scripts\python.exe build.py
```

标记冲突已解决：

```powershell
git add C:\Users\NOBODY2025\Desktop\contest-pages-test\index.html
git rebase --continue
```

如果 `contests.yaml` 或 `templates/index.html.j2` 冲突，不应直接覆盖。需要逐段比较并保留有效改动。

## 17. Cloudflare Pages 部署流程

当前项目推断使用 Cloudflare Pages 托管静态网站。通常流程为：

```text
本地 git push origin main
→ GitHub main 分支更新
→ Cloudflare Pages 触发自动部署
→ 发布静态文件
→ https://contest.zihao.me 更新
```

Cloudflare 控制台检查步骤：

1. 登录 Cloudflare 控制台。
2. 进入 Workers & Pages 或 Pages。
3. 找到该项目对应的 Pages 项目。
4. 打开 Deployments。
5. 查看最近一次 deployment 的状态和日志。

成功日志常见特征：

```text
Assets published
Your site was deployed
```

Cloudflare 项目名称、构建命令、输出目录、环境变量当前源码中未确认。

## 18. 域名与访问地址

当前主要访问地址：

```text
https://contest.zihao.me
```

模板中出现 Cloudflare Pages 托管链接：

```text
https://pages.cloudflare.com/
```

仓库中未确认其他正式访问域名。

## 19. 阿里云 ECS 角色说明

当前 ECS 脚本为：

```text
C:\Users\NOBODY2025\Desktop\contest-pages-test\run.sh
```

脚本中的 ECS 项目路径为：

```bash
/root/contest-pages-test
```

脚本中的日志路径为：

```bash
/root/contest-pages-test/cron.run.log
```

脚本执行流程：

```bash
git fetch origin main
git pull --rebase origin main
/root/contest-pages-test/venv/bin/python build.py
git add index.html data.json details static contests.yaml build.py templates
git commit -m "auto: update content & assets 日期时间"
git push origin main
```

CentOS 7 ECS 当前不建议作为主要开发环境。已知维护背景为新版 VS Code Server 与 CentOS 7 的 `glibc`、`libstdc++` 兼容性不足。ECS 更适合作为辅助自动运行环境。

ECS 保留用途：

- 可能用于 cron 定时构建。
- 可能用于定时抓取。
- 可能用于备份部署。

cron 当前配置未在仓库中保存，当前源码中未确认。

不建议在 ECS 上长期编辑源码。长期编辑应在 Windows 本地仓库完成，再通过 GitHub 和 Cloudflare Pages 发布。

## 20. 备份策略

当前交接要求中记录：`contests.yaml` 已备份到 Google Drive。该备份状态无法从源码验证。

建议重点备份以下内容：

```text
C:\Users\NOBODY2025\Desktop\contest-pages-test\contests.yaml
C:\Users\NOBODY2025\Desktop\contest-pages-test\templates\index.html.j2
C:\Users\NOBODY2025\Desktop\contest-pages-test\build.py
C:\Users\NOBODY2025\Desktop\contest-pages-test\static\images
C:\Users\NOBODY2025\Desktop\contest-pages-test\docs
```

备份原则：

- 重大修改前先备份 `contests.yaml`。
- 修改模板前备份 `templates/index.html.j2`。
- 替换图片前备份 `static\images`。
- 修复编码问题前备份整个仓库。

## 21. 常见故障排查

### 21.1 修改后网页没变

可能原因：只修改了模板或 YAML，但未重新运行构建。

处理命令：

```powershell
cd C:\Users\NOBODY2025\Desktop\contest-pages-test
C:\Users\NOBODY2025\Desktop\mywindows_env\Scripts\python.exe build.py
```

如果仍未变化，刷新 Live Server 页面或清理浏览器缓存。

### 21.2 图片不显示

可能原因：

- 图片不存在于 `C:\Users\NOBODY2025\Desktop\contest-pages-test\static\images`。
- 模板 `pokemon_images` 中的文件名与实际文件名不一致。
- 文件扩展名大小写或空格不一致。
- 使用 Live Server 的根目录不是 `C:\Users\NOBODY2025\Desktop\contest-pages-test`。

检查命令：

```powershell
Get-ChildItem C:\Users\NOBODY2025\Desktop\contest-pages-test\static\images
```

### 21.3 搜索框失效

可能原因：

- `templates/index.html.j2` 底部 JavaScript 语法错误。
- 输入框 ID `contestSearch` 被改动。
- 卡片元素 `.tile` 或 `data-search` 被改动。

处理方式：检查浏览器开发者工具 Console，并检查模板底部搜索代码。

### 21.4 状态显示错误

可能原因：

- `activeUntilMap` 或 `endedUntilMap` 日期过期。
- `contest_id_by_name` 映射错误。
- 竞赛名称修改后未同步模板映射。

处理位置：

```text
C:\Users\NOBODY2025\Desktop\contest-pages-test\templates\index.html.j2
```

### 21.5 官网按钮错误

可能原因：

- `officialUrlMap` 中链接过期。
- `officialUrlByName` 覆盖了 YAML 链接。
- `contests.yaml` 中 `homepage` 与模板硬编码不一致。

处理方式：优先修正模板中的官网映射，再运行构建。

### 21.6 Git push 被拒绝

处理命令：

```powershell
cd C:\Users\NOBODY2025\Desktop\contest-pages-test
git pull --rebase origin main
git push origin main
```

如果 rebase 发生冲突，需要先解决冲突。

### 21.7 Cloudflare 未部署

检查顺序：

1. GitHub 是否成功收到 `main` 分支推送。
2. Cloudflare Pages 是否绑定该 GitHub 仓库。
3. Cloudflare Deployments 是否出现新记录。
4. 部署日志中是否出现错误。

成功日志特征：

```text
Assets published
Your site was deployed
```

### 21.8 Live Server 显示旧页面

可能原因：

- 浏览器缓存。
- Live Server 打开的不是仓库根目录。
- `index.html` 未重新生成。

处理命令：

```powershell
cd C:\Users\NOBODY2025\Desktop\contest-pages-test
C:\Users\NOBODY2025\Desktop\mywindows_env\Scripts\python.exe build.py
```

### 21.9 index.html 与模板不一致

原因：`index.html` 是构建产物，模板修改不会自动反映到 `index.html`。

处理命令：

```powershell
cd C:\Users\NOBODY2025\Desktop\contest-pages-test
C:\Users\NOBODY2025\Desktop\mywindows_env\Scripts\python.exe build.py
```

### 21.10 中文显示乱码

当前源码中已经存在多处中文乱码。处理前必须备份。

建议流程：

```powershell
cd C:\Users\NOBODY2025\Desktop\contest-pages-test
git status
```

先备份关键文件，再逐个修复 `contests.yaml`、`templates/index.html.j2`、`build.py` 和详情页内容。修复完成后运行构建，并本地预览确认。

## 22. 年度维护流程

一年后重新维护时，建议按以下顺序操作：

1. 打开本地仓库：

```powershell
cd C:\Users\NOBODY2025\Desktop\contest-pages-test
```

2. 激活虚拟环境：

```powershell
& "C:\Users\NOBODY2025\Desktop\mywindows_env\Scripts\Activate.ps1"
```

3. 拉取远端最新代码：

```powershell
git pull --rebase origin main
```

4. 检查竞赛数据：

```powershell
notepad C:\Users\NOBODY2025\Desktop\contest-pages-test\contests.yaml
```

5. 检查首页模板：

```powershell
notepad C:\Users\NOBODY2025\Desktop\contest-pages-test\templates\index.html.j2
```

6. 运行构建：

```powershell
C:\Users\NOBODY2025\Desktop\mywindows_env\Scripts\python.exe build.py
```

7. 使用 Live Server 本地预览：

```text
C:\Users\NOBODY2025\Desktop\contest-pages-test\index.html
```

8. 提交与推送：

```powershell
git status
git add .
git commit -m "更新竞赛信息"
git push origin main
```

9. 检查 Cloudflare Pages 部署。

10. 备份关键文件。

## 23. 后续扩展建议

建议后续扩展方向：

- 增加状态筛选器，按“未开始”“正在进行”“已结束”筛选卡片。
- 增加收藏功能，使用浏览器本地存储保存常用竞赛。
- 增加倒计时功能，显示距离报名截止或比赛结束的剩余时间。
- 增加自动抓取官网状态功能，减少手动维护 `activeUntilMap`。
- 增加简单后台管理页面，避免直接编辑 YAML。
- 增加 YAML 校验脚本，提交前检查字段、缩进、URL 和重复 ID。
- 增加 `requirements.txt`，明确 Python 依赖版本。
- 修复中文编码，统一保存为 UTF-8。
- 明确 Cloudflare Pages 构建配置，写入文档或仓库配置。

## 24. 命令速查表

进入本地仓库：

```powershell
cd C:\Users\NOBODY2025\Desktop\contest-pages-test
```

激活虚拟环境：

```powershell
& "C:\Users\NOBODY2025\Desktop\mywindows_env\Scripts\Activate.ps1"
```

运行构建：

```powershell
C:\Users\NOBODY2025\Desktop\mywindows_env\Scripts\python.exe build.py
```

查看 Git 状态：

```powershell
git status
```

拉取远端更新：

```powershell
git pull --rebase origin main
```

提交修改：

```powershell
git add .
git commit -m "更新说明"
```

推送到 GitHub：

```powershell
git push origin main
```

查看远端仓库：

```powershell
git remote -v
```

查看图片目录：

```powershell
Get-ChildItem C:\Users\NOBODY2025\Desktop\contest-pages-test\static\images
```

查看详情页目录：

```powershell
Get-ChildItem C:\Users\NOBODY2025\Desktop\contest-pages-test\details
```

打开竞赛配置：

```powershell
notepad C:\Users\NOBODY2025\Desktop\contest-pages-test\contests.yaml
```

打开首页模板：

```powershell
notepad C:\Users\NOBODY2025\Desktop\contest-pages-test\templates\index.html.j2
```

## 25. 交接注意事项

最重要的维护原则如下：

- 不直接手改 `C:\Users\NOBODY2025\Desktop\contest-pages-test\index.html` 作为唯一修改。
- 修改 `C:\Users\NOBODY2025\Desktop\contest-pages-test\templates\index.html.j2` 后必须重新运行 `build.py`。
- 修改 `C:\Users\NOBODY2025\Desktop\contest-pages-test\contests.yaml` 后必须重新运行 `build.py`。
- 不在 ECS 上长期编辑源码。
- 不随意升级 CentOS 7 系统库，避免破坏现有系统依赖。
- 重大修改前先备份 `C:\Users\NOBODY2025\Desktop\contest-pages-test\contests.yaml`。
- 官网链接错误时优先检查模板内 `officialUrlMap`，不是只检查 YAML。
- 状态显示错误时优先检查模板内 `activeUntilMap` 和 `endedUntilMap`。
- 宝可梦图片新增后必须同步模板内 `pokemon_images`。
- 中文乱码修复必须分批进行，每批修复后都要构建和预览。
- Cloudflare Pages 发布失败时，先确认 GitHub `main` 分支是否已成功更新。

## 26. 当前源码核对结果

本交接手册生成前已核对以下路径：

```text
C:\Users\NOBODY2025\Desktop\contest-pages-test\build.py
C:\Users\NOBODY2025\Desktop\contest-pages-test\contests.yaml
C:\Users\NOBODY2025\Desktop\contest-pages-test\sources.yaml
C:\Users\NOBODY2025\Desktop\contest-pages-test\templates\index.html.j2
C:\Users\NOBODY2025\Desktop\contest-pages-test\static\images
C:\Users\NOBODY2025\Desktop\contest-pages-test\details
C:\Users\NOBODY2025\Desktop\contest-pages-test\run.sh
C:\Users\NOBODY2025\Desktop\contest-pages-test\data.json
C:\Users\NOBODY2025\Desktop\contest-pages-test\index.html
C:\Users\NOBODY2025\Desktop\contest-pages-test\.gitignore
```

未发现：

```text
C:\Users\NOBODY2025\Desktop\contest-pages-test\README.md
```

当前源码中发现的不一致或风险：

- 多个源码和产物文件存在中文乱码。
- `C:\Users\NOBODY2025\Desktop\mywindows_env\Scripts\python.exe` 当前无法启动。
- 当前主 `build.py` 未生成 `details` 页面，但仓库中存在 51 个详情页 HTML。
- `sources.yaml` 当前未被主 `build.py` 读取。
- `contests.yaml` 中存在 `parser` 字段，但当前主 `build.py` 未动态加载 parser。
- 首页模板内官网链接存在硬编码映射，可能与 `contests.yaml` 的 `homepage` 不一致。
- 首页状态由模板 JavaScript 映射表控制，不完全来自抓取结果。
- Cloudflare Pages 项目配置、cron 实际配置和 Google Drive 备份状态当前源码中未确认。
