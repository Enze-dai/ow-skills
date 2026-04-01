#!/usr/bin/env python3
"""
OW Seller 安装引导脚本
按评标五维度引导卖家配置产品清单和企业资料

评标维度：
- 💰 价格竞争力 50% -> 提供产品定价策略
- 📜 真品证明 20% -> 提供企业资质、代理权、授权书
- 📸 商品展示 15% -> 上传图片视频
- 🚚 到货时间 5% -> 配置物流方式和发货区域
- 📋 交易记录 10% -> 提供店铺链接和历史交易
"""

import json
import sys
from pathlib import Path
from datetime import datetime

STATE_DIR = Path(__file__).parent.parent / "state"
CATALOG_FILE = STATE_DIR / "product_catalog.json"
REGION_FILE = STATE_DIR / "region_config.json"

def print_header():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    💰 OW Seller - 发飙全球卖 安装引导                        ║
║                                                              ║
║    配置产品清单，让AI买家自动找到你                          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

def print_scoring_intro():
    print("""
📊 评标五维度 - 配置越完整，中标率越高

┌─────────────────────────────────────────────────────────────┐
│  维度          │ 权重  │ 你需要配置的内容                   │
├─────────────────────────────────────────────────────────────┤
│  💰 价格竞争力 │ 50%   │ 产品定价、成本、利润空间           │
│  📜 真品证明   │ 20%   │ 营业执照、代理权、授权书           │
│  📸 商品展示   │ 15%   │ 产品图片(最多3张)、视频(30秒)      │
│  🚚 到货时间   │ 5%    │ 物流方式、发货区域                 │
│  📋 交易记录   │ 10%   │ 店铺链接、历史成交                 │
└─────────────────────────────────────────────────────────────┘

⚠️  至少需要配置：产品类别
✅ 全部配置有利于：提高中标率，获得更多订单
""")

def get_input(prompt, default=None, required=False):
    """获取用户输入"""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    
    while True:
        value = input(prompt).strip()
        if value:
            return value
        if default:
            return default
        if not required:
            return ""
        print("❌ 此项为必填项，请输入")

def get_yes_no(prompt, default="n"):
    """获取是/否选择"""
    value = get_input(f"{prompt} (y/n)", default)
    return value.lower() == 'y'

def setup_basic_info():
    """配置卖家基本信息"""
    print("\n" + "="*60)
    print("📝 第一步：卖家基本信息")
    print("="*60 + "\n")
    
    seller_id = get_input("卖家ID", f"seller-{datetime.now().strftime('%Y%m%d%H%M')}", required=True)
    seller_name = get_input("店铺/企业名称", required=True)
    contact = get_input("联系方式（微信/电话/邮箱）")
    
    return {
        "seller_id": seller_id,
        "seller_name": seller_name,
        "contact": contact
    }

def setup_product():
    """配置单个产品"""
    print("\n" + "-"*60)
    print("📦 产品配置（按评标维度引导）")
    print("-"*60 + "\n")
    
    # 必填：产品类别
    print("【必填】产品基本信息")
    name = get_input("产品名称", required=True)
    category = get_input("产品类别（如：红酒、数码、服装）", required=True)
    
    product = {
        "product_id": f"PROD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "name": name,
        "category": category,
        "active": True
    }
    
    # 可选：品牌和关键词
    brand = get_input("品牌")
    if brand:
        product["brand"] = brand
    
    keywords_input = get_input("搜索关键词（逗号分隔，如：红酒,葡萄酒,洋酒）")
    if keywords_input:
        product["keywords"] = [k.strip() for k in keywords_input.split(",")]
    else:
        # 自动生成基础关键词
        product["keywords"] = [name, category]
        if brand:
            product["keywords"].append(brand)
    
    # 💰 价格竞争力 (50%)
    print("\n【💰 价格竞争力 - 权重50%】")
    print("   配置价格信息可提高中标率")
    
    if get_yes_no("是否配置价格信息？", "y"):
        cost = get_input("成本价（元）", "0")
        try:
            product["cost"] = float(cost)
        except:
            product["cost"] = 0
        
        price_min = get_input("最低售价（元）", str(int(product["cost"] * 1.1)))
        price_max = get_input("最高售价（元）", str(int(product["cost"] * 2)))
        try:
            product["price_range"] = [float(price_min), float(price_max)]
        except:
            product["price_range"] = [product["cost"], product["cost"] * 2]
        
        stock = get_input("库存数量", "10")
        try:
            product["stock"] = int(stock)
        except:
            product["stock"] = 10
    
    # 📜 真品证明 (20%)
    print("\n【📜 真品证明 - 权重20%】")
    print("   提供资质文件可大幅提高信任度")
    
    auth_docs = []
    if get_yes_no("有营业执照？", "y"):
        auth_docs.append("business_license")
        bl_url = get_input("营业执照图片链接（可选）")
        if bl_url:
            auth_docs.append({"type": "business_license", "url": bl_url})
    
    if get_yes_no("有产品代理权/授权书？"):
        auth_docs.append("agency_cert")
        ag_url = get_input("代理权证明链接（可选）")
        if ag_url:
            auth_docs.append({"type": "agency_cert", "url": ag_url})
    
    if get_yes_no("有质检报告/认证？"):
        auth_docs.append("quality_report")
    
    if auth_docs:
        product["auth_docs"] = auth_docs
    
    # 📸 商品展示 (15%)
    print("\n【📸 商品展示 - 权重15%】")
    print("   图片视频让买家更放心")
    
    if get_yes_no("是否上传商品展示？"):
        product["images"] = []
        for i in range(1, 4):
            img = get_input(f"图片{i}链接（留空跳过）")
            if img:
                product["images"].append(img)
        
        video = get_input("视频链接（可选，30秒以内）")
        if video:
            product["video"] = video
    
    # 📋 交易记录 (10%)
    print("\n【📋 交易记录 - 权重10%】")
    print("   店铺链接和成交记录提升信誉")
    
    shop_links = []
    if get_yes_no("是否提供店铺链接？", "y"):
        while True:
            platform = get_input("平台名称（淘宝/天猫/京东/抖音/其他，留空结束）")
            if not platform:
                break
            shop_url = get_input("店铺链接", required=True)
            shop_name = get_input("店铺名称")
            shop_links.append({
                "platform": platform,
                "url": shop_url,
                "shop_name": shop_name if shop_name else f"{seller_name} {platform}店"
            })
    
    if shop_links:
        product["shop_links"] = shop_links
    
    return product

def setup_shipping_regions():
    """配置发货区域"""
    print("\n" + "="*60)
    print("🚚 发货区域配置")
    print("="*60 + "\n")
    
    print("📍 配置可发货区域，系统将自动匹配同区域买家")
    print("   买家IP可判断其所在区域\n")
    
    regions_config = {
        "ship_regions": {
            "enabled": [],
            "disabled": [],
            "international": {
                "enabled": False,
                "countries": []
            }
        }
    }
    
    # 国内发货
    china_regions = [
        "全国", "华东", "华南", "华北", "华中", "西南", "西北", "东北"
    ]
    
    print("【国内发货】")
    print(f"   可选区域：{', '.join(china_regions)}")
    
    if get_yes_no("是否全国发货？", "y"):
        regions_config["ship_regions"]["enabled"].append("中国-全国")
    else:
        print("   选择可发货区域：")
        for region in china_regions:
            if get_yes_no(f"   发货到{region}？"):
                regions_config["ship_regions"]["enabled"].append(f"中国-{region}")
    
    # 港澳台和海外
    print("\n【特殊区域】")
    if get_yes_no("发货到港澳台？"):
        regions_config["ship_regions"]["enabled"].append("港澳台")
    else:
        regions_config["ship_regions"]["disabled"].append("港澳台")
    
    if get_yes_no("发货到海外？"):
        regions_config["ship_regions"]["international"]["enabled"] = True
        countries = get_input("可发货国家（逗号分隔，如：美国,日本,韩国）")
        if countries:
            regions_config["ship_regions"]["international"]["countries"] = [c.strip() for c in countries.split(",")]
    else:
        regions_config["ship_regions"]["disabled"].append("海外")
    
    # 物流方式
    print("\n【物流方式】")
    logistics_methods = []
    for method in ["顺丰", "京东", "圆通", "中通", "申通", "韵达", "邮政"]:
        if get_yes_no(f"使用{method}？"):
            logistics_methods.append(method)
    
    regions_config["logistics"] = {
        "methods": logistics_methods if logistics_methods else ["顺丰"],
        "default_delivery_days": 3
    }
    
    return regions_config

def setup_auto_match():
    """配置自动匹配"""
    print("\n" + "="*60)
    print("🤖 自动匹配配置")
    print("="*60 + "\n")
    
    print("⚡ 系统将自动搜索全球求购信息，匹配成功后通知你")
    
    auto_match = {
        "enabled": True,
        "scan_interval_minutes": 30,
        "price_match_tolerance": 0.3,
        "keywords_weight": 0.6,
        "category_weight": 0.4,
        "min_match_score": 0.3,
        "notify_on_match": True,
        "auto_bid_enabled": False,
        "auto_bid_min_score": 0.8
    }
    
    if get_yes_no("启用自动搜索匹配？", "y"):
        interval = get_input("搜索间隔（分钟）", "30")
        try:
            auto_match["scan_interval_minutes"] = int(interval)
        except:
            pass
        
        auto_match["enabled"] = True
    else:
        auto_match["enabled"] = False
    
    return auto_match

def run_setup():
    """执行完整安装引导"""
    print_header()
    print_scoring_intro()
    
    # 基本信息
    basic_info = setup_basic_info()
    
    # 产品清单
    products = []
    print("\n" + "="*60)
    print("📦 产品清单配置")
    print("="*60)
    
    while True:
        product = setup_product()
        products.append(product)
        
        if not get_yes_no("\n继续添加下一个产品？"):
            break
    
    # 发货区域
    shipping_config = setup_shipping_regions()
    
    # 自动匹配
    auto_match = setup_auto_match()
    
    # 组装完整配置
    catalog = {
        "seller_id": basic_info["seller_id"],
        "seller_name": basic_info["seller_name"],
        "contact": basic_info["contact"],
        "products": products,
        "ship_regions": shipping_config["ship_regions"],
        "logistics": shipping_config["logistics"],
        "auto_match": auto_match,
        "setup_completed": True,
        "setup_time": datetime.now().isoformat()
    }
    
    # 保存
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    CATALOG_FILE.write_text(json.dumps(catalog, indent=2, ensure_ascii=False))
    
    # 保存区域配置
    region_config = {
        "seller_id": basic_info["seller_id"],
        "seller_name": basic_info["seller_name"],
        "ship_regions": shipping_config["ship_regions"],
        "logistics": shipping_config["logistics"]
    }
    REGION_FILE.write_text(json.dumps(region_config, indent=2, ensure_ascii=False))
    
    # 完成提示
    print("\n" + "╔"+ "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║    ✅ 配置完成！你的产品清单已保存                        ║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    print(f"""
📊 配置摘要：
   • 卖家ID: {basic_info['seller_id']}
   • 店铺名称: {basic_info['seller_name']}
   • 产品数量: {len(products)}
   • 可发货区域: {len(shipping_config['ship_regions']['enabled'])} 个
   • 自动匹配: {'已启用' if auto_match['enabled'] else '未启用'}

🚀 下一步：
   1. 系统将每{auto_match['scan_interval_minutes']}分钟自动搜索匹配
   2. 发现商机时会自动通知你
   3. 你也可以手动搜索："搜索红酒求购信息"

💡 提高中标率：
   • 补充资质文件链接（真品证明+20%）
   • 上传商品图片视频（展示+15%）
   • 提供店铺成交记录（信誉+10%）

📁 配置文件位置：
   {CATALOG_FILE}
""")
    
    return catalog

def quick_setup():
    """快速配置（只配置必填项）"""
    print_header()
    
    print("⚡ 快速配置模式 - 只配置必要信息\n")
    
    seller_name = get_input("店铺/企业名称", required=True)
    category = get_input("产品类别（如：红酒、数码、服装）", required=True)
    
    catalog = {
        "seller_id": f"seller-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "seller_name": seller_name,
        "products": [
            {
                "product_id": f"PROD-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "name": category,
                "category": category,
                "keywords": [category],
                "active": True
            }
        ],
        "ship_regions": {
            "enabled": ["中国-全国"],
            "disabled": ["海外"],
            "international": {"enabled": False, "countries": []}
        },
        "logistics": {
            "methods": ["顺丰"],
            "default_delivery_days": 3
        },
        "auto_match": {
            "enabled": True,
            "scan_interval_minutes": 30,
            "min_match_score": 0.3,
            "notify_on_match": True
        },
        "setup_completed": True,
        "setup_time": datetime.now().isoformat()
    }
    
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    CATALOG_FILE.write_text(json.dumps(catalog, indent=2, ensure_ascii=False))
    
    print(f"\n✅ 快速配置完成！")
    print(f"   店铺: {seller_name}")
    print(f"   类别: {category}")
    print(f"\n💡 后续可运行完整配置补充更多信息，提高中标率")
    
    return catalog

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="OW Seller 安装引导")
    parser.add_argument("--quick", action="store_true", help="快速配置模式")
    args = parser.parse_args()
    
    if args.quick:
        quick_setup()
    else:
        run_setup()