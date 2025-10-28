# astrbot_plugin_minecraftskin

查询正版我的世界玩家皮肤，返回链接与渲染图（精炼输出）。

- 作者: BvzRays
- 版本: v1.0.0

## 安装
- 将本文件夹置于 AstrBot `data/plugins/` 并重启，或在 WebUI 上传 zip。
- 依赖按 `requirements.txt` 自动安装（`aiohttp`）。

## 用法
- 指令：`/mcskin <用户名>`（例：`/mcskin BvzRays`）

## 返回格式
1) 纯文本：
```
Minecraft玩家名：【BvzRays】
```
2) 单个“转发消息”内展示各项：每条为“链接 → 对应图片 → 空行”，例如：
```
皮肤：https://...
[皮肤图片]

披风：https://...
[披风图片]

全身：https://...
[全身渲染图片]

头像头：https://...
[头像头图片]

头像：https://...
[头像图片]

UUID：32ae3a44ea084b0f93c79b8131c480b9
```
3) 单独一条消息发送“全身图”（可在配置关闭）。

## 配置（_conf_schema.json）
- WebUI 可视化，实体配置位于 `data/config/astrbot_plugin_minecraftskin_config.json`。
- 主要开关：`send_skin_url`、`send_cape_url`、`send_body_url`、`send_head_url`、`send_avatar_url`、`send_uuid`、`send_body_image`、`request_timeout_seconds`。

## 接口
- 演示：`http://xiaoxun.my/api/v1/mc_skin/?name=BvzRays`
