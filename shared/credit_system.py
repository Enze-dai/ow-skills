#!/usr/bin/env python3
"""
OW 信用系统 - 核心模块
共享模块：买家和卖家都使用

功能：
1. 行为存证 - 记录完整链路
2. 信用评分 - 3次交易后激活
3. 风险检测 - 自动标注恶意行为
4. 风险提醒 - 生成提醒消息

冷启动规则：
- 交易次数 < 3：显示"新用户"，无信用分
- 交易次数 ≥ 3：激活信用，开始计算和检测
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

# 共享数据目录
SHARED_DIR = Path(__file__).parent.parent.parent.parent / "shared"
CREDIT_DIR = SHARED_DIR / "credit"
BUYERS_DIR = CREDIT_DIR / "buyers"
SELLERS_DIR = CREDIT_DIR / "sellers"
TRANSACTIONS_DIR = CREDIT_DIR / "transactions"
RISK_DIR = CREDIT_DIR / "risk"

# 信用等级阈值
CREDIT_LEVELS = [
    (90, "A+", "🏆", "优秀"),
    (80, "A", "⭐", "良好"),
    (70, "B", "✅", "正常"),
    (60, "C", "⚠️", "一般"),
    (50, "D", "❌", "较差"),
    (0, "F", "🚫", "危险")
]

# 风险检测阈值
RISK_THRESHOLDS = {
    "buyer": {
        "虚假需求风险": {"condition": "no_response", "threshold": 3},
        "钓鱼行为风险": {"condition": "never_deal", "threshold": 5},
        "履约风险": {"condition": "abandon_after_win", "threshold": 2}
    },
    "seller": {
        "虚假投标风险": {"condition": "no_response_after_win", "threshold": 3},
        "履约风险": {"condition": "abandon_delivery", "threshold": 2},
        "描述不符风险": {"condition": "complaint", "threshold": 3}
    }
}


def ensure_dirs():
    """确保目录存在"""
    for d in [BUYERS_DIR, SELLERS_DIR, TRANSACTIONS_DIR, RISK_DIR]:
        d.mkdir(parents=True, exist_ok=True)


def get_buyer_profile(agent_id: str) -> Dict:
    """获取买家档案"""
    ensure_dirs()
    profile_file = BUYERS_DIR / f"{agent_id}.json"
    
    if profile_file.exists():
        return json.loads(profile_file.read_text())
    
    # 新用户档案
    return {
        "agent_id": agent_id,
        "agent_name": "",
        "status": "new",
        "transaction_count": 0,
        "行为统计": {
            "发布需求总数": 0,
            "接收投标总数": 0,
            "确认中标总数": 0,
            "完成交易总数": 0,
            "放弃交易总数": 0
        },
        "链路完整率": {
            "发布→中标": 0,
            "中标→交易": 0,
            "发布→交易": 0
        },
        "响应时效": {
            "总响应时间": 0,
            "响应次数": 0,
            "平均响应时间": None
        },
        "信用状态": "pending",
        "信用分": None,
        "信用等级": None,
        "风险标注": [],
        "交易链路": [],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }


def get_seller_profile(agent_id: str) -> Dict:
    """获取卖家档案"""
    ensure_dirs()
    profile_file = SELLERS_DIR / f"{agent_id}.json"
    
    if profile_file.exists():
        return json.loads(profile_file.read_text())
    
    # 新用户档案
    return {
        "agent_id": agent_id,
        "agent_name": "",
        "status": "new",
        "transaction_count": 0,
        "行为统计": {
            "投标总数": 0,
            "中标总数": 0,
            "确认发货总数": 0,
            "完成交易总数": 0,
            "放弃发货总数": 0
        },
        "链路完整率": {
            "投标→中标": 0,
            "中标→发货": 0,
            "中标→完成": 0
        },
        "响应时效": {
            "总投标时间": 0,
            "投标次数": 0,
            "平均投标时间": None,
            "总发货时间": 0,
            "发货次数": 0,
            "平均发货时间": None
        },
        "信用状态": "pending",
        "信用分": None,
        "信用等级": None,
        "风险标注": [],
        "交易链路": [],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }


def save_buyer_profile(profile: Dict):
    """保存买家档案"""
    ensure_dirs()
    profile["updated_at"] = datetime.now().isoformat()
    profile_file = BUYERS_DIR / f"{profile['agent_id']}.json"
    profile_file.write_text(json.dumps(profile, indent=2, ensure_ascii=False))


def save_seller_profile(profile: Dict):
    """保存卖家档案"""
    ensure_dirs()
    profile["updated_at"] = datetime.now().isoformat()
    profile_file = SELLERS_DIR / f"{profile['agent_id']}.json"
    profile_file.write_text(json.dumps(profile, indent=2, ensure_ascii=False))


def record_transaction_step(transaction_id: str, step: str, agent_id: str, 
                           agent_role: str, extra: Dict = None):
    """记录交易链路步骤"""
    ensure_dirs()
    tx_file = TRANSACTIONS_DIR / f"{transaction_id}.json"
    
    if tx_file.exists():
        tx = json.loads(tx_file.read_text())
    else:
        tx = {
            "transaction_id": transaction_id,
            "buyer_id": None,
            "seller_id": None,
            "requirement_id": None,
            "bid_id": None,
            "chain": [],
            "created_at": datetime.now().isoformat()
        }
    
    # 更新参与者信息
    if agent_role == "buyer":
        tx["buyer_id"] = agent_id
    elif agent_role == "seller":
        tx["seller_id"] = agent_id
    
    # 添加链路步骤
    step_record = {
        "step": step,
        "timestamp": datetime.now().isoformat(),
        "agent_id": agent_id,
        "agent_role": agent_role
    }
    if extra:
        step_record.update(extra)
    
    tx["chain"].append(step_record)
    tx["updated_at"] = datetime.now().isoformat()
    
    tx_file.write_text(json.dumps(tx, indent=2, ensure_ascii=False))
    
    return tx


def update_transaction_link(transaction_id: str, field: str, value: str):
    """更新交易关联信息"""
    tx_file = TRANSACTIONS_DIR / f"{transaction_id}.json"
    
    if tx_file.exists():
        tx = json.loads(tx_file.read_text())
        tx[field] = value
        tx_file.write_text(json.dumps(tx, indent=2, ensure_ascii=False))


# ==================== 买家行为记录 ====================

def buyer_publish_requirement(agent_id: str, agent_name: str, requirement_id: str) -> Dict:
    """买家发布需求"""
    profile = get_buyer_profile(agent_id)
    profile["agent_name"] = agent_name
    profile["行为统计"]["发布需求总数"] += 1
    save_buyer_profile(profile)
    
    # 记录链路
    tx_id = f"TX-{datetime.now().strftime('%Y%m%d%H%M%S')}-{requirement_id}"
    record_transaction_step(tx_id, "发布需求", agent_id, "buyer", 
                           {"requirement_id": requirement_id})
    
    return {"transaction_id": tx_id, "profile": profile}


def buyer_receive_bid(agent_id: str, transaction_id: str):
    """买家接收投标"""
    profile = get_buyer_profile(agent_id)
    profile["行为统计"]["接收投标总数"] += 1
    save_buyer_profile(profile)
    
    record_transaction_step(transaction_id, "接收投标", agent_id, "buyer")


def buyer_confirm_winner(agent_id: str, transaction_id: str, seller_id: str,
                        response_time_hours: float = None):
    """买家确认中标"""
    profile = get_buyer_profile(agent_id)
    profile["行为统计"]["确认中标总数"] += 1
    update_transaction_link(transaction_id, "seller_id", seller_id)
    
    if response_time_hours:
        profile["响应时效"]["总响应时间"] += response_time_hours
        profile["响应时效"]["响应次数"] += 1
    
    save_buyer_profile(profile)
    
    record_transaction_step(transaction_id, "确认中标", agent_id, "buyer",
                           {"seller_id": seller_id})


def buyer_confirm_delivery(agent_id: str, transaction_id: str):
    """买家确认收货"""
    profile = get_buyer_profile(agent_id)
    profile["行为统计"]["完成交易总数"] += 1
    profile["transaction_count"] += 1
    save_buyer_profile(profile)
    
    record_transaction_step(transaction_id, "确认收货", agent_id, "buyer")
    record_transaction_step(transaction_id, "交易完成", agent_id, "buyer",
                           {"status": "completed"})
    
    # 检查是否激活信用
    return check_and_activate_buyer_credit(agent_id)


def buyer_abandon_transaction(agent_id: str, transaction_id: str, reason: str = ""):
    """买家放弃交易"""
    profile = get_buyer_profile(agent_id)
    profile["行为统计"]["放弃交易总数"] += 1
    save_buyer_profile(profile)
    
    record_transaction_step(transaction_id, "放弃交易", agent_id, "buyer",
                           {"reason": reason})
    
    # 检查风险
    return check_buyer_risk(agent_id)


# ==================== 卖家行为记录 ====================

def seller_submit_bid(agent_id: str, agent_name: str, transaction_id: str,
                     bid_time_hours: float = None):
    """卖家提交投标"""
    profile = get_seller_profile(agent_id)
    profile["agent_name"] = agent_name
    profile["行为统计"]["投标总数"] += 1
    
    if bid_time_hours:
        profile["响应时效"]["总投标时间"] += bid_time_hours
        profile["响应时效"]["投标次数"] += 1
    
    save_seller_profile(profile)
    
    record_transaction_step(transaction_id, "提交投标", agent_id, "seller")


def seller_win_bid(agent_id: str, transaction_id: str):
    """卖家中标"""
    profile = get_seller_profile(agent_id)
    profile["行为统计"]["中标总数"] += 1
    save_seller_profile(profile)
    
    record_transaction_step(transaction_id, "中标通知", agent_id, "seller")


def seller_confirm_delivery(agent_id: str, transaction_id: str, 
                           delivery_days: float = None):
    """卖家确认发货"""
    profile = get_seller_profile(agent_id)
    profile["行为统计"]["确认发货总数"] += 1
    
    if delivery_days:
        profile["响应时效"]["总发货时间"] += delivery_days
        profile["响应时效"]["发货次数"] += 1
    
    save_seller_profile(profile)
    
    record_transaction_step(transaction_id, "确认发货", agent_id, "seller")


def seller_complete_transaction(agent_id: str, transaction_id: str):
    """卖家完成交易"""
    profile = get_seller_profile(agent_id)
    profile["行为统计"]["完成交易总数"] += 1
    profile["transaction_count"] += 1
    save_seller_profile(profile)
    
    # 检查是否激活信用
    return check_and_activate_seller_credit(agent_id)


def seller_abandon_delivery(agent_id: str, transaction_id: str, reason: str = ""):
    """卖家放弃发货"""
    profile = get_seller_profile(agent_id)
    profile["行为统计"]["放弃发货总数"] += 1
    save_seller_profile(profile)
    
    record_transaction_step(transaction_id, "放弃发货", agent_id, "seller",
                           {"reason": reason})
    
    # 检查风险
    return check_seller_risk(agent_id)


# ==================== 信用计算 ====================

def calculate_buyer_credit(agent_id: str) -> Optional[int]:
    """计算买家信用分"""
    profile = get_buyer_profile(agent_id)
    
    if profile["transaction_count"] < 3:
        return None
    
    stats = profile["行为统计"]
    
    # 需求真实率 (40%)
    if stats["发布需求总数"] > 0:
        真实率 = stats["完成交易总数"] / stats["发布需求总数"]
    else:
        真实率 = 0
    真实率分 = 真实率 * 100 * 0.4
    
    # 中标履约率 (30%)
    if stats["确认中标总数"] > 0:
        履约率 = stats["完成交易总数"] / stats["确认中标总数"]
    else:
        履约率 = 0
    履约率分 = 履约率 * 100 * 0.3
    
    # 响应时效分 (20%)
    响应时效 = profile["响应时效"]
    if 响应时效["响应次数"] > 0:
        avg_time = 响应时效["总响应时间"] / 响应时效["响应次数"]
        if avg_time < 1:
            时效分 = 100
        elif avg_time < 6:
            时效分 = 80
        elif avg_time < 24:
            时效分 = 60
        elif avg_time < 48:
            时效分 = 40
        else:
            时效分 = 20
    else:
        时效分 = 60  # 默认中等
    时效分 = 时效分 * 0.2
    
    # 链路完整度 (10%)
    if stats["确认中标总数"] > 0:
        完整度 = stats["完成交易总数"] / stats["确认中标总数"]
    else:
        完整度 = 0
    完整度分 = 完整度 * 100 * 0.1
    
    总分 = 真实率分 + 履约率分 + 时效分 + 完整度分
    
    return round(总分)


def calculate_seller_credit(agent_id: str) -> Optional[int]:
    """计算卖家信用分"""
    profile = get_seller_profile(agent_id)
    
    if profile["transaction_count"] < 3:
        return None
    
    stats = profile["行为统计"]
    
    # 履约率 (40%)
    if stats["中标总数"] > 0:
        履约率 = stats["完成交易总数"] / stats["中标总数"]
    else:
        履约率 = 0
    履约率分 = 履约率 * 100 * 0.4
    
    # 投标成功率 (20%)
    if stats["投标总数"] > 0:
        成功率 = stats["中标总数"] / stats["投标总数"]
    else:
        成功率 = 0
    成功率分 = 成功率 * 100 * 0.2
    
    # 发货时效分 (20%)
    响应时效 = profile["响应时效"]
    if 响应时效["发货次数"] > 0:
        avg_days = 响应时效["总发货时间"] / 响应时效["发货次数"]
        if avg_days < 2:
            时效分 = 100
        elif avg_days < 3:
            时效分 = 80
        elif avg_days < 5:
            时效分 = 60
        elif avg_days < 7:
            时效分 = 40
        else:
            时效分 = 20
    else:
        时效分 = 60  # 默认中等
    时效分 = 时效分 * 0.2
    
    # 链路完整度 (20%)
    if stats["中标总数"] > 0:
        完整度 = stats["完成交易总数"] / stats["中标总数"]
    else:
        完整度 = 0
    完整度分 = 完整度 * 100 * 0.2
    
    总分 = 履约率分 + 成功率分 + 时效分 + 完整度分
    
    return round(总分)


def get_credit_level(score: int) -> Tuple[str, str, str]:
    """获取信用等级"""
    for threshold, level, emoji, desc in CREDIT_LEVELS:
        if score >= threshold:
            return level, emoji, desc
    return "F", "🚫", "危险"


# ==================== 信用激活检查 ====================

def check_and_activate_buyer_credit(agent_id: str) -> Dict:
    """检查并激活买家信用"""
    profile = get_buyer_profile(agent_id)
    
    if profile["transaction_count"] >= 3 and profile["信用状态"] == "pending":
        # 激活信用
        profile["信用状态"] = "active"
        profile["信用分"] = calculate_buyer_credit(agent_id)
        profile["信用等级"] = get_credit_level(profile["信用分"])
        profile["status"] = "active"
        save_buyer_profile(profile)
        
        return {
            "activated": True,
            "credit_score": profile["信用分"],
            "credit_level": profile["信用等级"]
        }
    
    return {"activated": False}


def check_and_activate_seller_credit(agent_id: str) -> Dict:
    """检查并激活卖家信用"""
    profile = get_seller_profile(agent_id)
    
    if profile["transaction_count"] >= 3 and profile["信用状态"] == "pending":
        # 激活信用
        profile["信用状态"] = "active"
        profile["信用分"] = calculate_seller_credit(agent_id)
        profile["信用等级"] = get_credit_level(profile["信用分"])
        profile["status"] = "active"
        save_seller_profile(profile)
        
        return {
            "activated": True,
            "credit_score": profile["信用分"],
            "credit_level": profile["信用等级"]
        }
    
    return {"activated": False}


# ==================== 风险检测 ====================

def check_buyer_risk(agent_id: str) -> Dict:
    """检测买家风险"""
    profile = get_buyer_profile(agent_id)
    
    if profile["transaction_count"] < 3:
        return {"risks": [], "has_risk": False}
    
    risks = []
    stats = profile["行为统计"]
    
    # 虚假需求风险
    发布数 = stats["发布需求总数"]
    无响应数 = 发布数 - stats["接收投标总数"]
    if 无响应数 >= 3:
        risks.append({
            "type": "虚假需求风险",
            "reason": f"发布{发布数}次需求，{无响应数}次无响应",
            "detected_at": datetime.now().isoformat()
        })
    
    # 钓鱼行为风险
    if 发布数 >= 5 and stats["完成交易总数"] == 0:
        risks.append({
            "type": "钓鱼行为风险",
            "reason": f"发布{发布数}次需求，从未成交",
            "detected_at": datetime.now().isoformat()
        })
    
    # 履约风险
    if stats["放弃交易总数"] >= 2:
        risks.append({
            "type": "履约风险",
            "reason": f"中标后放弃交易{stats['放弃交易总数']}次",
            "detected_at": datetime.now().isoformat()
        })
    
    # 更新档案
    if risks:
        profile["风险标注"] = risks
        profile["status"] = "risk"
        save_buyer_profile(profile)
    
    return {"risks": risks, "has_risk": len(risks) > 0}


def check_seller_risk(agent_id: str) -> Dict:
    """检测卖家风险"""
    profile = get_seller_profile(agent_id)
    
    if profile["transaction_count"] < 3:
        return {"risks": [], "has_risk": False}
    
    risks = []
    stats = profile["行为统计"]
    
    # 虚假投标风险
    中标无响应 = stats["中标总数"] - stats["确认发货总数"] - stats["放弃发货总数"]
    if 中标无响应 >= 3:
        risks.append({
            "type": "虚假投标风险",
            "reason": f"中标{stats['中标总数']}次，{中标无响应}次无响应",
            "detected_at": datetime.now().isoformat()
        })
    
    # 履约风险
    if stats["放弃发货总数"] >= 2:
        risks.append({
            "type": "履约风险",
            "reason": f"中标后放弃发货{stats['放弃发货总数']}次",
            "detected_at": datetime.now().isoformat()
        })
    
    # 更新档案
    if risks:
        profile["风险标注"] = risks
        profile["status"] = "risk"
        save_seller_profile(profile)
    
    return {"risks": risks, "has_risk": len(risks) > 0}


# ==================== 信用展示 ====================

def format_buyer_credit_display(agent_id: str) -> str:
    """格式化买家信用展示"""
    profile = get_buyer_profile(agent_id)
    
    if profile["transaction_count"] < 3:
        return f"""
🆕 新用户（暂无信用记录）
📊 交易记录：{profile['transaction_count']}次
"""
    
    score = profile["信用分"]
    level, emoji, desc = profile["信用等级"]
    stats = profile["行为统计"]
    
    # 计算真实率
    if stats["发布需求总数"] > 0:
        真实率 = stats["完成交易总数"] / stats["发布需求总数"] * 100
    else:
        真实率 = 0
    
    display = f"""
{emoji} 信用等级：{level} (信用分 {score}/100)
📊 真实需求率：发布{stats['发布需求总数']}次，成交{stats['完成交易总数']}次 ({真实率:.0f}%)
🔗 链路完整：{profile['transaction_count']}次完整交易
"""
    
    # 风险标注
    if profile["风险标注"]:
        display += "\n🚨 风险标注：\n"
        for risk in profile["风险标注"]:
            display += f"   • {risk['type']}：{risk['reason']}\n"
    
    return display


def format_seller_credit_display(agent_id: str) -> str:
    """格式化卖家信用展示"""
    profile = get_seller_profile(agent_id)
    
    if profile["transaction_count"] < 3:
        return f"""
🆕 新用户（暂无信用记录）
📊 交易记录：{profile['transaction_count']}次
"""
    
    score = profile["信用分"]
    level, emoji, desc = profile["信用等级"]
    stats = profile["行为统计"]
    
    # 计算履约率
    if stats["中标总数"] > 0:
        履约率 = stats["完成交易总数"] / stats["中标总数"] * 100
    else:
        履约率 = 0
    
    display = f"""
{emoji} 信用等级：{level} (信用分 {score}/100)
📊 履约记录：中标{stats['中标总数']}次，完成{stats['完成交易总数']}次 ({履约率:.0f}%履约)
🔗 链路完整：{profile['transaction_count']}次完整交易
"""
    
    # 发货时效
    响应时效 = profile["响应时效"]
    if 响应时效["发货次数"] > 0:
        avg_days = 响应时效["总发货时间"] / 响应时效["发货次数"]
        display += f"⏱️ 平均发货：{avg_days:.1f}天\n"
    
    # 风险标注
    if profile["风险标注"]:
        display += "\n🚨 风险标注：\n"
        for risk in profile["风险标注"]:
            display += f"   • {risk['type']}：{risk['reason']}\n"
    
    return display


def get_credit_warning(agent_id: str, role: str) -> Optional[str]:
    """获取信用风险警告"""
    if role == "buyer":
        profile = get_buyer_profile(agent_id)
    else:
        profile = get_seller_profile(agent_id)
    
    if profile["transaction_count"] < 3:
        return "💡 提示：该用户为新用户，暂无信用记录\n   这是正常的首次交易场景，请根据实际情况判断"
    
    if profile["status"] == "risk":
        return "🚨 警告：该用户存在风险标注，建议谨慎交易\n💡 建议：选择信用更高的交易对象"
    
    score = profile["信用分"]
    if score and score < 60:
        return f"⚠️ 警告：该用户信用分较低({score}分)，存在交易风险\n💡 建议：谨慎选择，或确认对方意向后再交易"
    
    if score and score >= 80:
        return "✅ 建议：该用户信用良好，可放心交易"
    
    return None


# ==================== 初始化 ====================

def init_credit_system():
    """初始化信用系统"""
    ensure_dirs()
    print("✅ OW 信用系统已初始化")
    print(f"   买家档案目录：{BUYERS_DIR}")
    print(f"   卖家档案目录：{SELLERS_DIR}")
    print(f"   交易记录目录：{TRANSACTIONS_DIR}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="OW 信用系统")
    parser.add_argument("action", choices=["init", "show-buyer", "show-seller", "list"])
    parser.add_argument("--agent-id", help="代理ID")
    
    args = parser.parse_args()
    
    if args.action == "init":
        init_credit_system()
    
    elif args.action == "show-buyer":
        if not args.agent_id:
            print("需要 --agent-id")
        else:
            print(format_buyer_credit_display(args.agent_id))
    
    elif args.action == "show-seller":
        if not args.agent_id:
            print("需要 --agent-id")
        else:
            print(format_seller_credit_display(args.agent_id))
    
    elif args.action == "list":
        ensure_dirs()
        buyers = list(BUYERS_DIR.glob("*.json"))
        sellers = list(SELLERS_DIR.glob("*.json"))
        print(f"买家档案：{len(buyers)} 个")
        print(f"卖家档案：{len(sellers)} 个")