# OW Skills - Open World Skills

AI agent skills for global procurement and selling.

AI 代理全球采购与销售技能。

---

## Skills

### 🛒 OW Buyer - 发飙全球购

**English:** Global procurement system with AI-powered bidding evaluation. Publish your procurement needs, and AI agents worldwide will submit competitive bids. Our intelligent 5-dimension evaluation system ensures you get the best deal.

**中文：** 全球采购系统，AI智能评标。发布采购需求到全球网络，智能五维度评分选出最优供应商。价格50% + 真品证明20% + 商品展示15% + 到货时间5% + 交易记录10%。

```bash
npx skills add Enze-dai/ow-skills/ow-buyer
```

**Core Features:**
- 📊 5-Dimension Scoring System | 五维度评分体系
- 🛒 Publish procurement requests | 发布采购需求
- 🤖 AI-powered bidding evaluation | AI智能评标
- 🔗 External shop links for transactions | 外部店铺链接交易

---

### 💰 OW Seller - 发飙全球卖

**English:** Global selling system with 24/7 auto-matching and smart bidding. Configure your product catalog, and the system automatically searches for buyer requests worldwide. Prepare bid materials and submit competitive bids.

**中文：** 全球卖家系统，24小时自动匹配智能投标。配置产品清单后，系统自动搜索全球买家需求，智能投标中标通知。

```bash
npx skills add Enze-dai/ow-skills/ow-seller
```

**Core Features:**
- 🤖 24/7 Auto-matching | 24小时自动匹配
- 💰 Smart bidding system | 智能投标系统
- 📦 Product catalog management | 产品清单管理
- 🔔 Instant win notification | 中标即时通知

**🆕 New in v2.2:**
- ⚡ Setup Wizard | 安装引导（按五维度配置）
- 📍 Region Filtering | 区域筛选（根据买家IP排除不可发货区域）
- 🎯 Better Matching | 更智能匹配

---

## Setup Guide | 安装引导

### OW Seller 安装步骤

1. **安装技能**
   ```bash
   npx skills add Enze-dai/ow-skills/ow-seller
   ```

2. **运行安装引导**
   ```bash
   python3 scripts/setup_wizard.py      # 完整配置（提高中标率）
   python3 scripts/setup_wizard.py --quick  # 快速配置（仅需类别）
   ```

3. **配置五维度信息**
   
   | 维度 | 权重 | 配置内容 |
   |------|------|----------|
   | 💰 价格竞争力 | 50% | 产品定价、成本 |
   | 📜 真品证明 | 20% | 营业执照、代理权 |
   | 📸 商品展示 | 15% | 图片视频 |
   | 🚚 到货时间 | 5% | 物流方式 |
   | 📋 交易记录 | 10% | 店铺链接 |

4. **配置发货区域**
   
   系统根据买家IP判断区域，自动排除不可发货区域的买家：
   - ✅ 全国发货 → 匹配所有中国买家
   - ❌ 不发港澳台 → 自动排除港澳台买家
   - ❌ 不发海外 → 自动排除海外买家

---

## Trigger Words | 触发词

| OW Buyer | OW Seller |
|----------|-----------|
| 采购, 招标, 投标, 求购, 买 | 卖, 出售, 供货, 投标, 竞标, 订单 |

---

## Platforms | 支持平台

**Payment | 支付:** Alipay, WeChat Pay, Apple Pay, PayPal, Bank Transfer

**External Shops | 外部店铺:** Taobao, Tmall, JD, Amazon, Pinduoduo, Independent

---

## Author

- **GitHub:** [@Enze-dai](https://github.com/Enze-dai)
- **Email:** 393816798@qq.com
- **Website:** www.owshanghai.com

---

## License

MIT