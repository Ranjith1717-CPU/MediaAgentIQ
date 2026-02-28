"""
MediaAgentIQ — Response Formatter

Converts agent output dicts into rich interactive UI formats:
  • Slack Block Kit  (https://api.slack.com/block-kit)
  • MS Teams Adaptive Cards (https://adaptivecards.io)

Every agent has a dedicated formatter function.
The dispatcher `format_result()` picks the right one automatically.

Button action_ids follow the pattern:
  miq_<action>_<agent_key>
  e.g. miq_export_compliance, miq_approve_playout, miq_publish_social
"""

from typing import Any, Dict, List, Optional


# ─── Slack Block Kit helpers ──────────────────────────────────────────────────

def _sl_header(text: str) -> Dict:
    return {"type": "header", "text": {"type": "plain_text", "text": text}}

def _sl_section(md: str) -> Dict:
    return {"type": "section", "text": {"type": "mrkdwn", "text": md}}

def _sl_divider() -> Dict:
    return {"type": "divider"}

def _sl_button(label: str, action_id: str, style: str = "default", value: str = "") -> Dict:
    btn = {
        "type": "button",
        "text": {"type": "plain_text", "text": label},
        "action_id": action_id,
        "value": value or action_id,
    }
    if style in ("primary", "danger"):
        btn["style"] = style
    return btn

def _sl_actions(*buttons) -> Dict:
    return {"type": "actions", "elements": list(buttons)}

def _sl_context(text: str) -> Dict:
    return {
        "type": "context",
        "elements": [{"type": "mrkdwn", "text": text}],
    }

def _score_emoji(score: float, /, threshold_ok: float = 70) -> str:
    if score >= 90:   return "✅"
    if score >= threshold_ok: return "⚠️"
    return "❌"


# ─── Teams Adaptive Card helpers ──────────────────────────────────────────────

def _tc_text(text: str, size: str = "default", weight: str = "default",
             color: str = "default") -> Dict:
    block = {"type": "TextBlock", "text": text, "wrap": True}
    if size != "default":   block["size"] = size
    if weight != "default": block["weight"] = weight
    if color != "default":  block["color"] = color
    return block

def _tc_fact(title: str, value: str) -> Dict:
    return {"title": title, "value": value}

def _tc_action_btn(title: str, data: Dict) -> Dict:
    return {"type": "Action.Submit", "title": title, "data": data}


# ─── Agent formatters — Slack ─────────────────────────────────────────────────

def _fmt_slack_compliance(data: Dict) -> List[Dict]:
    score = data.get("risk_score", 0)
    issues = data.get("issues", [])
    emoji = _score_emoji(100 - score, threshold_ok=30)

    blocks = [
        _sl_header(f"⚖️ Compliance Scan Result"),
        _sl_section(
            f"*Risk Score:* {score}/100 {emoji}\n"
            f"*Issues Found:* {len(issues)}\n"
            f"*Content:* {data.get('content_id', 'N/A')}"
        ),
    ]

    if issues:
        issue_lines = "\n".join(
            f"• [{i.get('severity','').upper()}] {i.get('rule','')} — {i.get('description','')}"
            for i in issues[:5]
        )
        blocks.append(_sl_section(f"*Issues:*\n{issue_lines}"))

    blocks += [
        _sl_divider(),
        _sl_actions(
            _sl_button("📄 Full Report", "miq_export_compliance"),
            _sl_button("🔔 Alert Team", "miq_alert_compliance"),
            _sl_button("✅ Mark Reviewed", "miq_reviewed_compliance", style="primary"),
        ),
        _sl_context(f"MediaAgentIQ Compliance Agent • {data.get('mode','demo')} mode"),
    ]
    return blocks


def _fmt_slack_caption(data: Dict) -> List[Dict]:
    segments = data.get("segments", [])
    word_count = sum(len(s.get("text","").split()) for s in segments)
    confidence = data.get("average_confidence", 0)
    issues = data.get("qa_issues", [])

    blocks = [
        _sl_header("📝 Caption Generation Complete"),
        _sl_section(
            f"*Segments:* {len(segments)}\n"
            f"*Word Count:* {word_count}\n"
            f"*Avg Confidence:* {confidence:.0%}\n"
            f"*QA Issues:* {len(issues)}"
        ),
    ]

    if segments:
        preview = "\n".join(
            f"`{s.get('start_time','')}` {s.get('text','')}"
            for s in segments[:3]
        )
        blocks.append(_sl_section(f"*Preview:*\n{preview}"))

    blocks += [
        _sl_divider(),
        _sl_actions(
            _sl_button("⬇️ Download SRT", "miq_download_srt"),
            _sl_button("⬇️ Download VTT", "miq_download_vtt"),
            _sl_button("🌍 Translate", "miq_translate_caption", style="primary"),
        ),
        _sl_context("MediaAgentIQ Caption Agent"),
    ]
    return blocks


def _fmt_slack_clip(data: Dict) -> List[Dict]:
    moments = data.get("viral_moments", [])
    blocks = [
        _sl_header("🎬 Viral Clip Detection"),
        _sl_section(f"*{len(moments)} viral moment(s) detected*"),
    ]

    for m in moments[:3]:
        score = m.get("viral_score", 0)
        blocks.append(_sl_section(
            f"*{m.get('title','Clip')}*\n"
            f"⏱ `{m.get('start_time','')} → {m.get('end_time','')}` | "
            f"Viral Score: {score:.0%}\n"
            f"_{m.get('reason','')}_\n"
            f"Tags: {', '.join(m.get('hashtags',[])[:4])}"
        ))

    blocks += [
        _sl_divider(),
        _sl_actions(
            _sl_button("✂️ Export Clips", "miq_export_clips"),
            _sl_button("📱 Publish Social", "miq_publish_clips", style="primary"),
        ),
        _sl_context("MediaAgentIQ Clip Agent"),
    ]
    return blocks


def _fmt_slack_trending(data: Dict) -> List[Dict]:
    trends = data.get("trends", [])[:5]
    breaking = data.get("breaking_news", [])

    lines = "\n".join(
        f"*{i+1}. {t.get('topic','')}*  |  "
        f"Velocity: {t.get('velocity_score',0)}  |  "
        f"Vol: {t.get('volume',0):,}/hr  |  {t.get('sentiment','')}"
        for i, t in enumerate(trends)
    )

    blocks = [
        _sl_header("📈 Trending Now"),
        _sl_section(lines or "_No active trends_"),
    ]

    if breaking:
        breaking_lines = "\n".join(f"🚨 {b.get('headline','')}" for b in breaking[:3])
        blocks.append(_sl_section(f"*Breaking News:*\n{breaking_lines}"))

    blocks += [
        _sl_divider(),
        _sl_actions(
            _sl_button("📱 Publish Trending", "miq_publish_trending"),
            _sl_button("📦 Archive Topics", "miq_archive_trending"),
            _sl_button("🔔 Set Alert", "miq_alert_trending"),
        ),
        _sl_context("MediaAgentIQ Trending Agent"),
    ]
    return blocks


def _fmt_slack_deepfake(data: Dict) -> List[Dict]:
    score = data.get("deepfake_probability", 0)
    level = data.get("risk_level", "unknown")
    held = data.get("held_from_broadcast", False)

    color_map = {"authentic": "✅", "suspicious": "⚠️", "likely_fake": "🔴", "confirmed_fake": "🚫"}
    emoji = color_map.get(level, "❓")

    blocks = [
        _sl_header(f"🕵️ Deepfake Detection Result"),
        _sl_section(
            f"*Risk Level:* {level.replace('_',' ').title()} {emoji}\n"
            f"*Probability:* {score:.0%}\n"
            f"*Auto-Hold Applied:* {'Yes 🔒' if held else 'No'}\n"
            f"*Content:* {data.get('content_id','N/A')}"
        ),
    ]

    findings = data.get("analysis", {})
    if findings:
        lines = "\n".join(
            f"• *{k.replace('_',' ').title()}:* {v}"
            for k, v in findings.items()
        )
        blocks.append(_sl_section(f"*Forensic Findings:*\n{lines}"))

    action_buttons = [_sl_button("📄 Full Forensic Report", "miq_export_deepfake")]
    if held:
        action_buttons.append(_sl_button("✅ Release for Broadcast", "miq_release_deepfake", style="primary"))
        action_buttons.append(_sl_button("🗑 Reject Content", "miq_reject_deepfake", style="danger"))
    else:
        action_buttons.append(_sl_button("🔒 Hold Content", "miq_hold_deepfake", style="danger"))

    blocks += [_sl_divider(), _sl_actions(*action_buttons),
               _sl_context("MediaAgentIQ Deepfake Detection Agent")]
    return blocks


def _fmt_slack_brand_safety(data: Dict) -> List[Dict]:
    score = data.get("brand_safety_score", 0)
    emoji = _score_emoji(score)
    garm_flags = data.get("garm_flags", [])
    blocked = data.get("ad_insertion_blocked", False)

    blocks = [
        _sl_header("🛡️ Brand Safety Score"),
        _sl_section(
            f"*Safety Score:* {score}/100 {emoji}\n"
            f"*Ad Insertion:* {'🚫 Blocked' if blocked else '✅ Approved'}\n"
            f"*GARM Flags:* {len(garm_flags)}\n"
            f"*Revenue Impact:* {data.get('revenue_impact','N/A')}"
        ),
    ]

    if garm_flags:
        flag_lines = "\n".join(f"• {f}" for f in garm_flags[:5])
        blocks.append(_sl_section(f"*GARM Categories Flagged:*\n{flag_lines}"))

    action_buttons = [_sl_button("📄 Advertiser Report", "miq_export_brand_safety")]
    if blocked:
        action_buttons.append(_sl_button("✅ Override & Allow Ads", "miq_override_brand_safety", style="primary"))
    else:
        action_buttons.append(_sl_button("🚫 Block Ad Insertion", "miq_block_brand_safety", style="danger"))

    blocks += [_sl_divider(), _sl_actions(*action_buttons),
               _sl_context("MediaAgentIQ Brand Safety Agent")]
    return blocks


def _fmt_slack_fact_check(data: Dict) -> List[Dict]:
    claims = data.get("claims", [])
    broadcast_risk = data.get("broadcast_risk_score", 0)

    blocks = [
        _sl_header("✅ Live Fact-Check Result"),
        _sl_section(
            f"*Claims Verified:* {len(claims)}\n"
            f"*Broadcast Risk Score:* {broadcast_risk}/100\n"
            f"*Databases Queried:* {data.get('databases_queried', 'N/A')}"
        ),
    ]

    verdict_emoji = {"true": "✅", "mostly_true": "🟢", "half_true": "🟡",
                     "misleading": "🟠", "false": "❌", "unverified": "❓", "outdated": "⏰"}
    for claim in claims[:4]:
        v = claim.get("verdict", "unverified")
        blocks.append(_sl_section(
            f"{verdict_emoji.get(v,'❓')} *{v.replace('_',' ').title()}*\n"
            f"_{claim.get('claim','')[:120]}_\n"
            f"Source: {claim.get('source','N/A')} | Confidence: {claim.get('confidence',0):.0%}"
        ))

    blocks += [
        _sl_divider(),
        _sl_actions(
            _sl_button("📄 Full Fact-Check Report", "miq_export_factcheck"),
            _sl_button("🔔 Alert Anchor", "miq_alert_anchor", style="danger"),
        ),
        _sl_context("MediaAgentIQ Live Fact-Check Agent"),
    ]
    return blocks


def _fmt_slack_social(data: Dict) -> List[Dict]:
    posts = data.get("posts", {})
    blocks = [
        _sl_header("📱 Social Posts Generated"),
        _sl_section(f"*Platforms:* {', '.join(posts.keys())}"),
    ]

    for platform, post in list(posts.items())[:3]:
        text = post.get("content", "")[:200] if isinstance(post, dict) else str(post)[:200]
        blocks.append(_sl_section(f"*{platform.title()}*\n{text}"))

    blocks += [
        _sl_divider(),
        _sl_actions(
            _sl_button("🚀 Publish All", "miq_publish_all_social", style="primary"),
            _sl_button("✏️ Edit First", "miq_edit_social"),
            _sl_button("📋 Copy Text", "miq_copy_social"),
        ),
        _sl_context("MediaAgentIQ Social Publishing Agent"),
    ]
    return blocks


def _fmt_slack_ingest(data: Dict) -> List[Dict]:
    blocks = [
        _sl_header("📥 Ingest & Transcode"),
        _sl_section(
            f"*Status:* {data.get('status','N/A')}\n"
            f"*Source:* {data.get('source_url','N/A')[:60]}\n"
            f"*Duration:* {data.get('duration','N/A')}\n"
            f"*Output Profiles:* {', '.join(data.get('output_profiles',[]))}\n"
            f"*Proxy Generated:* {'✅' if data.get('proxy_generated') else '❌'}"
        ),
        _sl_divider(),
        _sl_actions(
            _sl_button("▶️ Process All Agents", "miq_process_all_ingest", style="primary"),
            _sl_button("📤 Send to MAM", "miq_mam_ingest"),
            _sl_button("📄 Ingest Report", "miq_export_ingest"),
        ),
        _sl_context("MediaAgentIQ Ingest & Transcode Agent"),
    ]
    return blocks


def _fmt_slack_signal_quality(data: Dict) -> List[Dict]:
    score = data.get("quality_score", 0)
    emoji = _score_emoji(score)
    issues = data.get("issues", [])

    blocks = [
        _sl_header("📡 Signal Quality Report"),
        _sl_section(
            f"*Quality Score:* {score}/100 {emoji}\n"
            f"*Loudness:* {data.get('loudness_lufs','N/A')} LUFS\n"
            f"*EBU R128 Compliant:* {'✅' if data.get('ebu_r128_compliant') else '❌'}\n"
            f"*Issues Detected:* {len(issues)}"
        ),
    ]

    if issues:
        issue_lines = "\n".join(f"• {i}" for i in issues[:5])
        blocks.append(_sl_section(f"*Issues:*\n{issue_lines}"))

    action_buttons = [_sl_button("📄 Full QC Report", "miq_export_signal")]
    if issues:
        action_buttons.append(_sl_button("🔔 Alert NOC", "miq_alert_noc", style="danger"))
        action_buttons.append(_sl_button("🔧 Auto-Correct", "miq_autocorrect_signal", style="primary"))

    blocks += [_sl_divider(), _sl_actions(*action_buttons),
               _sl_context("MediaAgentIQ Signal Quality Agent")]
    return blocks


def _fmt_slack_playout(data: Dict) -> List[Dict]:
    schedule = data.get("schedule", [])[:5]
    blocks = [
        _sl_header("📺 Playout Schedule"),
        _sl_section(
            f"*Items Scheduled:* {data.get('total_items', len(schedule))}\n"
            f"*Next Break:* {data.get('next_break','N/A')}\n"
            f"*Automation Server:* {data.get('automation_server','N/A')}"
        ),
    ]

    if schedule:
        lines = "\n".join(
            f"`{i.get('timecode','--:--:--')}` {i.get('title','')[:40]} "
            f"[{i.get('duration','')}"
            f"{' ⚠️' if i.get('warning') else ''}]"
            for i in schedule
        )
        blocks.append(_sl_section(f"*Upcoming:*\n{lines}"))

    blocks += [
        _sl_divider(),
        _sl_actions(
            _sl_button("✅ Approve Schedule", "miq_approve_playout", style="primary"),
            _sl_button("✏️ Edit Schedule", "miq_edit_playout"),
            _sl_button("📤 Push to Automation", "miq_push_playout"),
        ),
        _sl_context("MediaAgentIQ Playout & Scheduling Agent"),
    ]
    return blocks


def _fmt_slack_ott(data: Dict) -> List[Dict]:
    blocks = [
        _sl_header("🌐 OTT / Multi-Platform Distribution"),
        _sl_section(
            f"*Platforms Published:* {data.get('platforms_published', 0)}\n"
            f"*CDN Status:* {data.get('cdn_status','N/A')}\n"
            f"*HLS URL:* {data.get('hls_url','N/A')[:60]}\n"
            f"*DASH URL:* {data.get('dash_url','N/A')[:60]}"
        ),
        _sl_divider(),
        _sl_actions(
            _sl_button("🔗 Copy HLS URL", "miq_copy_hls"),
            _sl_button("🔗 Copy DASH URL", "miq_copy_dash"),
            _sl_button("📊 CDN Analytics", "miq_cdn_analytics"),
        ),
        _sl_context("MediaAgentIQ OTT Distribution Agent"),
    ]
    return blocks


def _fmt_slack_newsroom(data: Dict) -> List[Dict]:
    rundown = data.get("rundown_items", [])[:6]
    blocks = [
        _sl_header("📰 Newsroom Integration"),
        _sl_section(
            f"*Rundown Items:* {data.get('total_items', len(rundown))}\n"
            f"*Newsroom System:* {data.get('system','N/A')}\n"
            f"*Last Sync:* {data.get('last_sync','N/A')}"
        ),
    ]

    if rundown:
        lines = "\n".join(
            f"`{i.get('slug','')[:12]}` {i.get('title','')[:40]} "
            f"[{i.get('duration','')}] {i.get('status','')}"
            for i in rundown
        )
        blocks.append(_sl_section(f"*Today's Rundown:*\n{lines}"))

    blocks += [
        _sl_divider(),
        _sl_actions(
            _sl_button("🔄 Sync Rundown", "miq_sync_newsroom", style="primary"),
            _sl_button("📤 Push to Playout", "miq_newsroom_to_playout"),
            _sl_button("📄 Export Rundown", "miq_export_newsroom"),
        ),
        _sl_context("MediaAgentIQ Newsroom Integration Agent"),
    ]
    return blocks


def _fmt_slack_generic(agent_key: str, data: Dict) -> List[Dict]:
    """Fallback formatter for agents without a specific template."""
    import json
    preview = json.dumps(data, indent=2, default=str)[:600]
    return [
        _sl_header(f"🤖 {agent_key.replace('_',' ').title()} Result"),
        _sl_section(f"```{preview}```"),
        _sl_divider(),
        _sl_actions(_sl_button("📄 Export", f"miq_export_{agent_key}")),
        _sl_context(f"MediaAgentIQ — {agent_key}"),
    ]


def _fmt_slack_status(data: Dict) -> List[Dict]:
    agents = data.get("agents", {})
    lines = "\n".join(
        f"{'✅' if v.get('ready') else '❌'} *{k}* — {v.get('mode','demo')} mode"
        for k, v in list(agents.items())[:14]
    )
    return [
        _sl_header("🤖 MediaAgentIQ Agent Status"),
        _sl_section(lines or "_No agents registered_"),
        _sl_divider(),
        _sl_actions(
            _sl_button("🔌 Connectors", "miq_show_connectors"),
            _sl_button("📊 Full Dashboard", "miq_open_dashboard"),
        ),
        _sl_context("MediaAgentIQ Platform"),
    ]


def _fmt_slack_connectors(data: Dict) -> List[Dict]:
    summary = data.get("summary", {})
    lines = []
    for category, connectors in data.get("by_category", {}).items():
        for c in connectors:
            status = c.get("status", "unknown")
            emoji = "🟢" if status == "connected" else "🔴"
            lines.append(f"{emoji} *{c.get('name','')}* ({category})")

    return [
        _sl_header("🔌 Connector Status"),
        _sl_section(
            f"*Total:* {summary.get('total',0)}  |  "
            f"*Connected:* {summary.get('connected',0)}  |  "
            f"*Health:* {summary.get('health_pct',0)}%\n"
            f"*MCP Tools Available:* {data.get('total_tools',0)}"
        ),
        _sl_section("\n".join(lines[:15]) or "_No connectors registered_"),
        _sl_context("MediaAgentIQ Connector Registry"),
    ]


# ─── Main dispatch ─────────────────────────────────────────────────────────────

_SLACK_FORMATTERS = {
    "compliance":           _fmt_slack_compliance,
    "caption":              _fmt_slack_caption,
    "clip":                 _fmt_slack_clip,
    "trending":             _fmt_slack_trending,
    "deepfake":             _fmt_slack_deepfake,
    "brand_safety":         _fmt_slack_brand_safety,
    "fact_check":           _fmt_slack_fact_check,
    "social":               _fmt_slack_social,
    "ingest_transcode":     _fmt_slack_ingest,
    "signal_quality":       _fmt_slack_signal_quality,
    "playout":              _fmt_slack_playout,
    "ott":                  _fmt_slack_ott,
    "newsroom":             _fmt_slack_newsroom,
}


def format_slack(
    agent_key: str,
    result: Dict[str, Any],
    system_command: str = None,
) -> Dict:
    """
    Format an agent result as a Slack Block Kit message payload.
    Returns dict ready to pass to slack_sdk chat.postMessage.
    """
    if system_command == "status":
        blocks = _fmt_slack_status(result)
    elif system_command == "connectors":
        blocks = _fmt_slack_connectors(result)
    else:
        data = result.get("data", result)
        formatter = _SLACK_FORMATTERS.get(agent_key)
        if formatter:
            blocks = formatter(data)
        else:
            blocks = _fmt_slack_generic(agent_key, data)

    return {"blocks": blocks}


# ─── Teams Adaptive Card formatters ───────────────────────────────────────────

def format_teams(
    agent_key: str,
    result: Dict[str, Any],
    system_command: str = None,
) -> Dict:
    """
    Format an agent result as a Teams Adaptive Card attachment.
    Returns dict ready for Bot Framework Activity.
    """
    data = result.get("data", result) if not system_command else result

    title_map = {
        "compliance":       "⚖️ Compliance Scan Result",
        "caption":          "📝 Caption Generation Complete",
        "clip":             "🎬 Viral Clip Detection",
        "trending":         "📈 Trending Now",
        "deepfake":         "🕵️ Deepfake Detection",
        "brand_safety":     "🛡️ Brand Safety Score",
        "fact_check":       "✅ Live Fact-Check",
        "social":           "📱 Social Posts Generated",
        "ingest_transcode": "📥 Ingest & Transcode",
        "signal_quality":   "📡 Signal Quality Report",
        "playout":          "📺 Playout Schedule",
        "ott":              "🌐 OTT Distribution",
        "newsroom":         "📰 Newsroom Integration",
    }
    title = title_map.get(agent_key, f"🤖 {agent_key.replace('_',' ').title()}")

    import json
    body = [
        _tc_text(title, size="Large", weight="Bolder"),
        {"type": "FactSet", "facts": [
            _tc_fact(k.replace("_", " ").title(), str(v)[:80])
            for k, v in data.items()
            if not isinstance(v, (list, dict)) and k != "mode"
        ][:8]},
    ]

    actions = [
        _tc_action_btn("📄 Full Report", {"action": f"miq_export_{agent_key}", "agent": agent_key}),
        _tc_action_btn("🔔 Alert Team",  {"action": "miq_alert_team",           "agent": agent_key}),
    ]

    return {
        "type": "message",
        "attachments": [{
            "contentType": "application/vnd.microsoft.card.adaptive",
            "content": {
                "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                "type": "AdaptiveCard",
                "version": "1.4",
                "body": body,
                "actions": actions,
            }
        }]
    }


# ─── HOPE formatters ──────────────────────────────────────────────────────────

def format_hope_created(rule: dict) -> dict:
    """Slack block confirming a new HOPE rule was registered."""
    rule_id = rule.get("rule_id", "hope_???")
    agent = rule.get("agent", "unknown")
    status = rule.get("status", "created")
    note = rule.get("note", "")

    lines = [
        f"*Rule ID:* `{rule_id}`",
        f"*Agent:* {agent}",
        f"*Status:* {status}",
    ]
    if note:
        lines.append(f"_Note: {note}_")

    return {
        "blocks": [
            _sl_header("✅ HOPE Rule Created"),
            _sl_section("\n".join(lines)),
            _sl_context(
                "Rule is now ACTIVE and will evaluate on every agent result. "
                f"To cancel: `stop watching {rule_id}`"
            ),
        ]
    }


def format_hope_cancelled(rule_id: str) -> dict:
    """Slack block confirming a HOPE rule was cancelled."""
    return {
        "blocks": [
            _sl_header("🔕 HOPE Rule Cancelled"),
            _sl_section(f"Rule `{rule_id}` has been set to *INACTIVE*. No further alerts will fire."),
            _sl_context("To see remaining rules: 'list my rules'"),
        ]
    }


def format_hope_list(rules: list, agent_key: str = "all") -> dict:
    """Slack block table of HOPE rules — active rules highlighted."""
    if not rules:
        return {
            "blocks": [
                _sl_header("📋 HOPE Rules"),
                _sl_section(
                    f"_No rules found for agent `{agent_key}`._\n"
                    "Create one: _\"Whenever you detect X, alert me\"_"
                ),
            ]
        }

    active = [r for r in rules if r.get("status") == "ACTIVE"]
    inactive = [r for r in rules if r.get("status") != "ACTIVE"]

    def _rule_line(r: dict) -> str:
        rid = r.get("rule_id", "?")
        cond = r.get("condition", "")[:50]
        sched = r.get("schedule", "IMMEDIATE")
        prio = r.get("priority", "NORMAL")
        count = r.get("trigger_count", 0)
        return f"`{rid}` *{prio}* | {sched} | _{cond}_ | fired: {count}"

    blocks = [_sl_header(f"📋 HOPE Rules — {agent_key}")]

    if active:
        lines = "\n".join(_rule_line(r) for r in active)
        blocks.append(_sl_section(f"*Active ({len(active)}):*\n{lines}"))

    if inactive:
        lines = "\n".join(f"~~`{r.get('rule_id','?')}`~~ _{r.get('condition','')[:40]}_" for r in inactive)
        blocks.append(_sl_section(f"*Inactive ({len(inactive)}):*\n{lines}"))

    blocks.append(_sl_context(
        f"Total: {len(rules)} rules | "
        "Cancel a rule: 'stop watching hope_001' | "
        "Add: 'whenever you see X, alert me'"
    ))
    return {"blocks": blocks}


def format_hope_alert(rule, result: dict, priority: str) -> dict:
    """
    Urgent-formatted Slack alert fired by HOPE Engine.

    CRITICAL → 🚨 bold header + @here
    HIGH     → ⚠️ alert header
    NORMAL   → informational
    LOW      → digest summary
    """
    priority = priority.upper()

    if priority == "CRITICAL":
        icon = "🚨"
        header_text = "🚨 CRITICAL HOPE ALERT"
    elif priority == "HIGH":
        icon = "⚠️"
        header_text = "⚠️ HOPE Alert"
    elif priority == "NORMAL":
        icon = "ℹ️"
        header_text = "ℹ️ HOPE Alert"
    else:
        icon = "📋"
        header_text = "📋 HOPE Digest"

    # Safe attribute or dict access
    def _attr(obj, key, default=""):
        if hasattr(obj, key):
            return getattr(obj, key)
        if isinstance(obj, dict):
            return obj.get(key, default)
        return default

    rule_id = _attr(rule, "rule_id", "hope_???")
    agent_slug = _attr(rule, "agent_slug", "agent")
    condition = _attr(rule, "condition", "")
    action = _attr(rule, "action", "")
    trigger_count = _attr(rule, "trigger_count", 0)

    # Extract a short summary from result
    result_summary = ""
    if isinstance(result, dict):
        data = result.get("data", result)
        if isinstance(data, dict):
            # Grab first few scalar values
            items = [(k, v) for k, v in data.items() if not isinstance(v, (dict, list))][:3]
            result_summary = " | ".join(f"{k}: {v}" for k, v in items)
        else:
            result_summary = str(data)[:120]

    lines = [
        f"*Rule:* `{rule_id}` on *{agent_slug}*",
        f"*Condition matched:* _{condition[:80]}_",
        f"*Action:* {action}",
        f"*Result preview:* {result_summary or '_no data_'}",
        f"*Total fires:* {trigger_count}",
    ]

    if priority == "CRITICAL":
        lines.insert(0, "<!here> — *Critical standing-instruction triggered*")

    blocks = [
        _sl_header(header_text),
        _sl_section("\n".join(lines)),
        _sl_divider(),
        _sl_actions(
            _sl_button("🔕 Cancel Rule", f"miq_hope_cancel_{rule_id}"),
            _sl_button("📋 List All Rules", "miq_hope_list"),
        ),
        _sl_context(f"MediaAgentIQ HOPE Engine • {priority} priority"),
    ]

    return {"blocks": blocks}


# ─── Error / loading formatters ───────────────────────────────────────────────

def format_slack_thinking(agent_key: str) -> Dict:
    """'Agent is processing...' placeholder sent immediately."""
    return {
        "blocks": [
            _sl_section(f"_Running {agent_key.replace('_',' ').title()} Agent..._  ⏳"),
        ]
    }


def format_slack_error(error: str, agent_key: str = "") -> Dict:
    return {
        "blocks": [
            _sl_section(f"❌ *Error{' in ' + agent_key if agent_key else ''}:*\n{error}"),
        ]
    }


def format_slack_unrecognized(original_text: str) -> Dict:
    return {
        "blocks": [
            _sl_section(
                f"🤔 I didn't quite understand: _{original_text}_\n\n"
                f"Try `/miq-help` to see available commands, "
                f"or be more specific (e.g. *'check compliance on [url]'*)."
            ),
        ]
    }
