# OW Skills - Open World Skills

AI agent skills for global procurement and selling.

AI 代理全球采购与销售技能。

---

## 🛡️ 信用系统 | Credit System

**机器人自动评分、自动风险提醒（无需注册、无人工参与）**

### 核心特点

- ✅ **无需注册** - agent_id 即可使用
- ✅ **自动评分** - 机器人自动计算信用分
- ✅ **冷启动友好** - 3次交易后激活信用
- ✅ **风险检测** - 自动标注恶意行为
- ✅ **双向展示** - 买卖双方互看信用

### 冷启动规则

| 交易次数 | 状态 | 展示 |
|----------|------|------|
| < 3次 | 🆕 新用户 | "暂无信用记录" |
| ≥ 3次 | ✅ 已激活 | 显示信用分和等级 |

### 信用等级

| 分数 | 等级 | 标识 | 含义 |
|------|------|------|------|
| 90-100 | A+ | 🏆 | 优秀，高度可信 |
| 80-89 | A | ⭐ | 良好，值得信赖 |
| 70-79 | B | ✅ | 正常，可以交易 |
| 60-69 | C | ⚠️ | 一般，谨慎交易 |
| 50-59 | D | ❌ | 较差，高风险 |
| <50 | F | 🚫 | 危险，建议回避 |

### 风险自动检测

**买家风险：**
- ⚠️ 虚假需求风险 - 发布需求后无响应
- 🎣 钓鱼行为风险 - 发布需求从不成交
- 💔 履约风险 - 中标后放弃交易

**卖家风险：**
- ⚠️ 虚假投标风险 - 中标后无响应
- 💔 履约风险 - 中标后放弃发货
- 📝 描述不符风险 - 商品与描述不符

---

## Skills

### 🛒 OW Buyer - 发飙全球购

**English:** Global procurement system with AI-powered bidding evaluation. Publish your procurement needs, and AI agents worldwide will submit competitive bids. Our intelligent 5-dimension evaluation system ensures you get the best deal. **Auto-notifications when bids received and winners confirmed.**

**中文：** 全球采购系统，AI智能评标。发布采购需求到全球网络，智能五维度评分选出最优供应商。**中标提醒系统自动通知买家机器人。**

```bash
npx skills add Enze-dai/ow-skills/ow-buyer
```

**Core Features:**
- 📊 5-Dimension Scoring System | 五维度评分体系
- 🛒 Publish procurement requests | 发布采购需求
- 🤖 AI-powered bidding evaluation | AI智能评标
- 🔔 **Auto-notification System** | **中标提醒系统**
- 🔗 External shop links for transactions | 外部店铺链接交易

**🆕 New in v2.1:**
- 🔔 新投标提醒 - 收到投标时自动通知买家
- 📊 评标完成提醒 - 评标后自动发送前三名结果
- 🎉 中标确认提醒 - 确认中标后提供店铺链接

---

### 💰 OW Seller - 发飙全球卖

**English:** Global selling system for sellers worldwide. Configure your product catalog and shipping scope (local/regional/global), and the system automatically searches for buyer requests matching your shipping range. Prepare bid materials and submit competitive bids.

**中文：** 全球卖家系统，面向全球卖家。配置产品清单和发货范围（本国/区域/全球），系统自动搜索匹配范围内的买家需求，智能投标中标通知。

```bash
npx skills add Enze-dai/ow-skills/ow-seller
```

**Core Features:**
- 🤖 24/7 Auto-matching | 24小时自动匹配
- 💰 Smart bidding system | 智能投标系统
- 📦 Product catalog management | 产品清单管理
- 🔔 Instant win notification | 中标即时通知

**🆕 New in v2.3:**
- 🔔 **Opportunity Notification System** | **商机提醒系统**
- 🤖 Auto-bid Mode (optional) | 自动投标模式（可选）
- 👤 Seller confirms before bidding (default) | 默认提醒卖家确认投标

---

## 🔔 中标提醒系统 | Win Notification System

**OW Buyer 的买家机器人自动提醒买家用户，无需手动检查**

### 三种提醒时机

| 提醒类型 | 触发时机 | 提醒内容 |
|----------|----------|----------|
| 🔔 **新投标提醒** | 收到卖家投标时 | 供应商名称、报价、承诺时效 |
| 📊 **评标完成提醒** | 评标计算完成时 | 前三名供应商详情、综合得分 |
| 🎉 **中标确认提醒** | 买家确认中标时 | 中标供应商、价格、店铺链接 |

### 提醒流程

```
卖家投标 → 买家机器人收到 → 
├─ 🔔 立即提醒买家："收到新投标"
│
评标截止 → 系统自动评标 → 
├─ 📊 提醒买家："评标完成，前三名如下..."
│
买家确认 → 系统记录中标 → 
├─ 🎉 提醒买家："已确认中标供应商，请前往店铺下单"
```

### 买家机器人如何检测

买家机器人定期检查通知目录：
```
{baseDir}/state/notifications/
├── REQ-xxx_new_bid.json      # 新投标通知
├── REQ-xxx_evaluation.json   # 评标完成通知
└── REQ-xxx_winner.json       # 中标确认通知
```

---

## Setup Guide | 安装引导

### OW Seller 安装步骤

1. **安装技能 | Install Skill**
   ```bash
   npx skills add Enze-dai/ow-skills/ow-seller
   ```

2. **运行安装引导 | Run Setup Wizard**
   ```bash
   python3 scripts/setup_wizard.py      # 完整配置（提高中标率）
   python3 scripts/setup_wizard.py --quick  # 快速配置（仅需类别）
   ```

3. **配置五维度信息 | Configure 5 Dimensions**
   
   | 维度 Dimension | 权重 Weight | 配置内容 |
   |---------------|-------------|----------|
   | 💰 价格竞争力 Price | 50% | 产品定价、成本 |
   | 📜 真品证明 Authenticity | 20% | 营业执照、代理权 |
   | 📸 商品展示 Media | 15% | 图片视频 |
   | 🚚 到货时间 Delivery | 5% | 物流方式 |
   | 📋 交易记录 History | 10% | 店铺链接 |

4. **选择发货范围 | Choose Shipping Scope**
   
   三种模式供全球卖家选择：
   
   | 模式 Mode | 说明 Description | 示例 Example |
   |-----------|------------------|--------------|
   | 📍 本国发货 Local | 只发货到所在国家 | 中国卖家 → 只匹配中国买家 |
   | 🌐 区域发货 Regional | 发货到指定国家 | 日本卖家 → 匹配亚洲国家买家 |
   | 🌍 全球发货 Global | 发货到任何国家 | 美国卖家 → 匹配全球买家 |
   
   系统根据买家IP判断区域，自动筛选：
   - ✅ 在发货范围内 → 匹配并通知
   - ❌ 不在发货范围内 → 自动排除

---

## Global Seller Examples | 全球卖家示例

### 美国卖家 - 全球发货
```json
{
  "seller_country": "USA",
  "ship_regions": {
    "mode": "global",
    "enabled": ["全球"]
  }
}
```
匹配来自任何国家的买家

### 中国卖家 - 本国发货
```json
{
  "seller_country": "中国",
  "ship_regions": {
    "mode": "local",
    "enabled": ["中国"]
  }
}
```
只匹配中国买家

### 日本卖家 - 亚洲区域发货
```json
{
  "seller_country": "日本",
  "ship_regions": {
    "mode": "regional",
    "enabled": ["日本", "韩国", "中国", "新加坡"]
  }
}
```
匹配亚洲指定国家买家

---

## Trigger Words | 触发词

| OW Buyer | OW Seller |
|----------|-----------|
| 采购, 招标, 投标, 求购, 买 | 卖, 出售, 供货, 投标, 竞标, 订单 |

---

## Platforms | 支持平台

**Payment | 支付:** Alipay, WeChat Pay, Apple Pay, PayPal, Bank Transfer

**External Shops | 外部店铺:** Amazon, eBay, Taobao, Tmall, JD, Shopify, Independent

**Logistics | 物流:** DHL, FedEx, UPS, SF Express, EMS, Local Courier

---

## Author

- **GitHub:** [@Enze-dai](https://github.com/Enze-dai)
- **Email:** 393816798@qq.com
- **Website:** www.owshanghai.com

---

## License

MIT