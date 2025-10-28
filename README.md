# astrbot_plugin_minecraftskin

一个简单好用的 AstrBot 插件：查询正版我的世界玩家皮肤并展示渲染图。

- 作者: BvzRays
- 版本: v1.0.0

## 安装
- 将本文件夹放入 AstrBot 的 `data/plugins/` 后重启；或在 WebUI 直接上传 zip。
- 依赖通过 `requirements.txt` 自动安装（使用 `aiohttp`）。

## 用法
- 指令：`/mcskin <用户名>`
- 示例：`/mcskin BvzRays`

返回（按配置开关展示，图片与文本同一条消息）：
```
--------------------
[ BvzRays ]
· 皮肤：http://textures.minecraft.net/texture/...
· 披风：https://skins.legacyminecraft.com/capes/...
· 全身：https://skins.legacyminecraft.com/renders/body/...
· 头像头：https://skins.legacyminecraft.com/renders/head/...
· 头像：https://skins.legacyminecraft.com/avatars/...
· UUID：32ae3a44ea084b0f93c79b8131c480b9
[全身像图片]
--------------------
```

## 配置（_conf_schema.json）
- 在插件根目录定义 Schema，WebUI 可视化配置，实际文件生成到 `data/config/astrbot_plugin_minecraftskin_config.json`。
- 主要开关：`send_skin_url`、`send_cape_url`、`send_body_url`、`send_head_url`、`send_avatar_url`、`send_uuid`、`send_body_image`，以及 `request_timeout_seconds`。

## 接口
- 演示：`http://xiaoxun.my/api/v1/mc_skin/?name=BvzRays`
