# 🌐 BRICK Network Geofeed 仓库使用说明

欢迎使用 BRICK Network Geofeed 管理仓库。请在提交和维护数据时严格遵守以下说明：

---

### 1️⃣ 准入原则
* 本仓库**仅限受信用户**使用与维护。

### 2️⃣ 提交方式 (PR 流程)
本仓库不接受直接推送主分支，所有数据更新必须通过 **Pull Request (PR)** 提交：
1. 先点击右上角 **Fork** 本仓库到个人账号。
2. 在本地完成修改并 `git push` 到你的远程仓库。
3. 在 GitHub 页面上发起 **Pull Request**，等待管理员审核并入。

### 3️⃣ 数据提交规范
* 提交 Geofeed 数据时，**必须在 `/data/` 目录下创建新的 `.csv` 文件**（例如 `data/hk-ips.csv`）。
* 将你需要提交的 Geofeed 信息写入该文件中。

> 💡 **温馨提示**：
> 系统后台会自动扫描并合并 `/data/` 目录下的所有文件。请确保数据格式正确。根据网络规划，**`44.32.191.0/28` 范围内的 IP 请保持原样，不要进行聚合。**

---

### 4️⃣ 公开地址
合并后的标准 Geofeed 文件将自动发布到以下公开地址，供全球 GeoIP 厂商及解析器抓取：

🔗 **[https://geofeed.nia.ink/geofeed.csv](https://geofeed.nia.ink/geofeed.csv)**
