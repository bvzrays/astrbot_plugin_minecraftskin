from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger, AstrBotConfig

@register("astrbot_plugin_minecraftskin", "BvzRays", "从 API 查询我的世界玩家皮肤信息", "1.0.0")
class MinecraftSkinPlugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig = None):
        super().__init__(context)
        # AstrBot 会根据 _conf_schema.json 生成并传入 config（data/config 下）
        self.config = config or AstrBotConfig({
            "send_username": True,
            "send_uuid": True,
            "send_skin_url": True,
            "send_cape_url": True,
            "send_body_url": True,
            "send_head_url": True,
            "send_avatar_url": True,
            "send_body_image": True,
            "request_timeout_seconds": 10,
        })

    async def initialize(self):
        logger.info(f"[mcskin] 配置已注入: {dict(self.config or {})}")

    @filter.command("mcskin")
    async def mcskin(self, event: AstrMessageEvent):
        """查询玩家皮肤：/mcskin <用户名>"""
        import aiohttp
        import asyncio
        from urllib.parse import quote
        import astrbot.api.message_components as Comp

        message_str = event.message_str or ""
        parts = message_str.strip().split()
        target_name = parts[1] if len(parts) >= 2 else None
        if not target_name:
            yield event.plain_result("用法：/mcskin <正版用户名>")
            return

        timeout_sec = int(self.config.get("request_timeout_seconds", 10) or 10)
        api_url = f"http://xiaoxun.my/api/v1/mc_skin/?name={quote(target_name)}"
        logger.info(f"[mcskin] 请求开始 name={target_name} url={api_url} timeout={timeout_sec}s")

        resp_json = None
        try:
            timeout = aiohttp.ClientTimeout(total=timeout_sec)
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(api_url) as resp:
                    resp.raise_for_status()
                    resp_json = await resp.json(content_type=None)
        except Exception as e:
            logger.error(f"[mcskin] 请求失败: {e}")

        if not resp_json:
            yield event.plain_result("查询失败：接口请求异常或超时。")
            return

        if not resp_json.get("success"):
            yield event.plain_result(f"查询失败：{resp_json}")
            return

        username = resp_json.get("username") or target_name
        uuid = resp_json.get("uuid")
        skin_url = resp_json.get("skin_url")
        cape_url = resp_json.get("cape_url")
        body_url = resp_json.get("body_url")
        head_url = resp_json.get("head_url")
        avatar_url = resp_json.get("avatar_url")

        logger.info(f"[mcskin] 返回 success 用户={username} uuid={uuid}")

        # 1) 先发玩家名（纯文本）
        if self.config.get("send_username", True):
            yield event.plain_result(f"Minecraft玩家名：【{username}】")

        # 2) 单个转发消息（一个 Node），每个链接后跟对应图片，并用换行分隔
        contents = []
        def add_entry(enabled: bool, label: str, url: str):
            if enabled and url:
                contents.append(Comp.Plain(f"{label}：{url}"))
                try:
                    contents.append(Comp.Image.fromURL(url))
                except Exception as e:
                    logger.error(f"[mcskin] 组装图片失败 label={label} url={url} err={e}")
                contents.append(Comp.Plain("\n"))

        add_entry(self.config.get("send_skin_url", True), "皮肤", skin_url)
        add_entry(self.config.get("send_cape_url", True), "披风", cape_url)
        add_entry(self.config.get("send_body_url", True), "全身", body_url)
        add_entry(self.config.get("send_head_url", True), "头像头", head_url)
        add_entry(self.config.get("send_avatar_url", True), "头像", avatar_url)
        if self.config.get("send_uuid", True) and uuid:
            contents.append(Comp.Plain(f"UUID：{uuid}\n"))

        if contents:
            try:
                # uin/name 仅用于展示
                try:
                    uin = int(event.get_self_id()) if event.get_self_id() and event.get_self_id().isdigit() else 0
                except Exception:
                    uin = 0
                node = Comp.Node(uin=uin, name="mcskin", content=contents)
                yield event.chain_result([node])
            except Exception as e:
                logger.error(f"[mcskin] 发送转发消息失败: {e}")
        else:
            logger.info("[mcskin] 无可展示链接内容，跳过转发消息发送")

        # 3) 最后发全身图（单独一条消息，保留可选）
        if self.config.get("send_body_image", True) and body_url:
            try:
                yield event.image_result(body_url)
                logger.info(f"[mcskin] 全身图已发送 url={body_url}")
            except Exception as e:
                logger.error(f"[mcskin] 发送全身图失败: {e}")

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
