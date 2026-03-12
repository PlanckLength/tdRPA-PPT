import re
import json

HTML_FILE = r"d:\code\python\rpa\tdRPA-PPT\index.html"

with open(HTML_FILE, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update QR code text
html = html.replace('扫码联系我们', '使用微信扫码联系')

# 2. Add Toggle UI HTML
toggle_html = """
    <div class="lang-toggle">
        <button id="langZh" class="active">中文</button>
        <button id="langEn">EN</button>
    </div>
"""
if '<div class="lang-toggle">' not in html:
    html = html.replace('<div class="progress-bar" id="progressBar"></div>', f'<div class="progress-bar" id="progressBar"></div>\n{toggle_html}')

# 3. Add CSS for toggle UI
toggle_css = """
        /* ===== Language Toggle ===== */
        .lang-toggle {
            position: fixed;
            top: 24px;
            right: 30px;
            z-index: 1000;
            display: flex;
            background: rgba(15, 23, 42, 0.8);
            border-radius: 20px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            overflow: hidden;
            backdrop-filter: blur(10px);
        }
        .lang-toggle button {
            background: transparent;
            border: none;
            color: #94a3b8;
            padding: 6px 14px;
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            outline: none;
        }
        .lang-toggle button.active {
            background: rgba(59, 130, 246, 0.4);
            color: #fff;
        }
"""
if '/* ===== Language Toggle ===== */' not in html:
    html = html.replace('    </style>', f'{toggle_css}\n    </style>')

# 4. Inject JS code with dictionary
i18n_dict = {
    "tdRPA - 技术驱动机器人流程自动化系统 路演宣讲": "tdRPA - Technology Driven RPA System Roadshow",
    "技术驱动机器人流程自动化系统": "Technology Driven Robotic Process Automation System",
    "告别重复劳动 · 把工作交给 tdRPA，把生活还给自己": "Say goodbye to repetitive work · Leave work to tdRPA, give life back to yourself",
    "零门槛 + 专业级 + 极致安全 · 自动化生产力平台": "Zero Threshold + Pro Grade + Extreme Security · Productivity Platform",
    "tdRPA 产品概述": "tdRPA Product Overview",
    'tdRPA 是一款集<strong style="color:#60a5fa">「零门槛 + 专业级 + 极致安全」</strong>于一体的<strong style="color:#60a5fa">自动化生产力平台</strong>。通过软件模拟人类在电脑上的操作，按照预设规则自动执行流程任务，将复杂的业务流程简化为"点击"与"拖拽"。': 'tdRPA is an <strong style="color:#60a5fa">automated productivity platform</strong> integrating <strong style="color:#60a5fa">"Zero Threshold + Pro Grade + Extreme Security"</strong>. By simulating human operations on computers, it automatically executes process tasks according to preset rules, simplifying complex business processes into "clicks" and "drags".',
    "适用场景：": "Applicable Scenarios: ",
    "数据量大、重复度高、规则明确、跨业务系统、高人力成本的业务场景": "Business scenarios with large data volumes, high repetition, clear rules, cross-business systems, and high labor costs.",
    "核心理念：": "Core Concept: ",
    "这不仅是一个工具，更是一次工作范式的升级": "This is not just a tool, but an upgrade of the working paradigm.",
    "核心应用领域": "Core Application Areas",
    "📊 数据传输": "📊 Data Transmission",
    "📋 数据整理": "📋 Data Organization",
    "⚙️ 执行系统操作": "⚙️ Exec System Ops",
    "🌐 Web 自动化": "🌐 Web Automation",
    "📧 邮件处理": "📧 Email Processing",
    "📁 文件处理": "📁 File Processing",
    "🔄 基于规则的流程处理": "🔄 Rule-based Processing",
    "🤖 AI 大模型集成": "🤖 AI Model Integration",
    "📈 Excel 自动化": "📈 Excel Automation",
    "tdRPA 核心特点": "tdRPA Core Features",
    "7×24 小时无休": "7×24 Non-stop",
    "全天候运行，24小时不间断执行任务，无需人工值守，确保业务连续性，成为真正的\"数字员工\"。": "Runs around the clock, 24/7 without manual supervision, ensuring business continuity as a true \"digital employee\".",
    "非侵入式开发": "Non-intrusive Dev",
    "基于规则在用户界面进行自动化操作，不影响原有IT基础架构，零侵入部署，拒绝盲写代码。": "Automates via UI based on rules without affecting existing IT infrastructure. Zero-intrusion deployment, say no to blind coding.",
    "零门槛 · 极简开发": "Zero Threshold · Minimalist Dev",
    "命令原型系统让您无需手写代码，通过点击即可自动生成 Python 代码，参数可见即所得。": "Command prototype system allows you to auto-generate Python code by clicking without writing code manually. WYSIWYG parameters.",
    "全程可控可追溯": "Fully Controllable & Traceable",
    "安全沙箱隔离测试环境，业务流程具有明确的数字化触发指令，不会出现未定义的例外情况。": "Secure sandbox isolates test environments. Business processes have clear digital triggers, ensuring no undefined exceptions.",
    "tdRPA-Creator 交互式开发工具": "tdRPA-Creator Interactive IDE",
    "<em>交互式代码版</em> RPA 开发工具": "<em>Interactive Code-based</em> RPA IDE",
    "tdRPA-Creator 完美平衡了「简单直观」与「强大专业」，让零基础用户和专业开发者都能高效创建自动化流程。7分钟即可玩转企业级 RPA 自动化。": "tdRPA-Creator perfectly balances \"simplicity\" and \"professionalism\", enabling beginners and experts alike to efficiently create automated workflows in just 7 minutes.",
    "\"复杂的业务流程被简化为'点击'与'拖拽'，拒绝盲写，参数可见即所得\"": "\"Complex business processes are simplified into 'clicks' and 'drags'. No blind coding, WYSIWYG parameters.\"",
    "命令原型系统": "Command Prototype",
    '独创功能：无需手写代码，通过点击如"Web 自动化 > 创建浏览器"即可自动生成 Python 代码': 'Original feature: Generate Python code by simply clicking (e.g., "Web Auto > Create Browser"), no manual coding required.',
    "交互式参数配置": "Interactive Config",
    "直观操作面板，网址、路径、等待时间等参数可视化调整，实时预览代码变化": "Intuitive panel for visual adjustment of URLs, paths, timeouts, etc. Real-time code preview.",
    "安全沙箱环境": "Secure Sandbox",
    "一键开启测试环境，在隔离窗口中运行机器人，确保不影响已有流程和电脑环境": "1-click test environment. Run bots in isolated windows to ensure existing processes and environments remain unaffected.",
    "纯 Python 内核": "Pure Python Core",
    "无缝调用 Pandas、Requests、OpenCV 及 AI 大模型库，专业开发上限极高": "Seamless integration with Pandas, Requests, OpenCV, and AI models. Unlimited professional potential.",
    "六大核心能力": "Six Core Capabilities",
    "模拟手工<br>操作": "Simulate<br>Manual Ops",
    "基于规则<br>操作": "Rule-based<br>Ops",
    "处理重复<br>任务": "Handle Repetitive<br>Tasks",
    "非侵入式<br>部署": "Non-intrusive<br>Deployment",
    "极简<br>开发": "Minimalist<br>Dev",
    "7×24<br>无休": "7×24<br>Non-stop",
    "模拟手工操作及交互": "Simulate Manual Operations & Interactions",
    "执行登录系统、打开菜单、录入数据、查询报表等一系列电脑交互操作": "Execute actions like logging in, opening menus, entering data, and querying reports.",
    "基于明确的规则操作": "Rule-based Operations",
    "可被数字化的触发指令和输入，流程不会出现例外情况，无人因操作风险": "Digitized trigger commands ensure no unexpected exceptions and eliminate human error.",
    "处理高度可重复任务": "Handle Highly Repetitive Tasks",
    "通过命令原型系统辅以 Python 编程，准确无误地自动处理重复人工任务": "Command prototype system paired with Python programming to handle repetitive manual tasks accurately.",
    "非侵入式进行部署": "Non-intrusive Deployment",
    "基于规则在用户界面进行自动化操作，不影响原有IT基础架构": "Automated UI operations based on rules. Does not alter existing IT architecture.",
    "极简开发，快速上岗": "Minimalist Development, Quick Onboarding",
    "命令原型 + 交互式参数配置，无适应期，高效解决问题": "Command prototype + interactive config. No learning curve, solves problems efficiently.",
    "全天候 7×24 小时无休": "Runs 24/7 Uninterrupted",
    "真正的\"数字员工\"，24小时不间断运行，持续为业务提供自动化支持": "A true \"digital employee\" running 24/7, providing continuous automation support.",
    "产品优势": "Product Advantages",
    "底层架构": "Core Architecture",
    "国产自主可控": "Domestically Controllable",
    "核心基于 Python 生态": "Python-ecosystem Core",
    "可调用 AI 大模型库": "AI Model Integration",
    "安全稳定可靠": "Secure & Reliable",
    "开发环境": "Development Env",
    "tdRPA-Creator 交互式工具": "tdRPA-Creator IDE",
    "支持 VS Code / PyCharm": "VS Code / PyCharm Support",
    "提供 RESTful API 接口": "RESTful APIs",
    "暗黑模式 / 智能搜索": "Dark Mode / Smart Search",
    "开放灵活": "Open & Flexible",
    "可集成到 ERP 等系统内部": "Integrable with ERPs",
    "可嵌入 tdRPA 功能": "Embeddable tdRPA Features",
    "提供 OEM 贴标服务": "OEM Whitelabeling",
    "可被任意语言调用": "Callable from Any Language",
    "私有化部署": "Private Deployment",
    "可内网环境(离线)运行": "Intranet (Offline) Capable",
    "安全沙箱隔离测试": "Secure Sandbox Testing",
    "流程可打包为 exe 分发": "Packagable as .exe for Distro",
    "数据安全有保障": "Guaranteed Data Security",
    "行业覆盖": "Industry Coverage",
    "银行": "Banking",
    "证券": "Securities",
    "能源": "Energy",
    "医药": "Medical",
    "保险": "Insurance",
    "制造": "Manufacturing",
    "旅游": "Tourism",
    "零售": "Retail",
    "地产": "Real Estate",
    "政务": "Government",
    "覆盖金融、制造、能源、医药、政务等多个行业领域，为各行各业提供智能自动化解决方案": "Covering finance, manufacturing, energy, medical, government, and other sectors, providing intelligent automation solutions for all industries.",
    "应用场景": "Scenarios",
    "💰 财务管理": "💰 Financial Mgmt",
    "应收账款": "Accounts Receivable",
    "开票": "Invoicing",
    "采购付款": "Procurement Payment",
    "订单": "Orders",
    "收款": "Collections",
    "财务报告": "Financial Reports",
    "每日报表自动汇总": "Daily Report Auto-summary",
    "邮件定时发送": "Scheduled Emails",
    "存货盘点": "Inventory Audits",
    "👥 人力资源": "👥 Human Resources",
    "入职": "Onboarding",
    "考勤": "Attendance",
    "人事档案": "Personnel Files",
    "福利管理": "Benefits Mgmt",
    "薪酬": "Payroll",
    "员工信息批量录入": "Batch Employee Entry",
    "合同自动生成": "Auto Contract Gen",
    "教育及培训": "Ed & Training",
    "招聘": "Recruitment",
    "🛒 电商运营": "🛒 E-commerce Ops",
    "竞品价格抓取": "Competitor Price Scraping",
    "库存自动抓取": "Auto Inventory Scraping",
    "数据自动入库": "Auto Data Entry",
    "客户关系": "CRM",
    "工作流管理": "Workflow Mgmt",
    "舞弊识别": "Fraud Detection",
    "数据获取": "Data Acquisition",
    "信息采集": "Info Collection",
    "📦 供应链管理": "📦 Supply Chain",
    "存货管理": "Inventory Mgmt",
    "采购需求计划": "Procurement Planning",
    "合同管理": "Contract Mgmt",
    "询价管理": "Inquiry Mgmt",
    "订单管理": "Order Mgmt",
    "物流配送": "Logistics & Delivery",
    "退货处理": "Returns Processing",
    "🖥️ IT 管理": "🖥️ IT Management",
    "安装": "Installations",
    "下载上传备份": "Download/Upload Backup",
    "文件管理": "File Mgmt",
    "邮件管理": "Email Mgmt",
    "文件同步": "File Sync",
    "批处理": "Batch Processing",
    "服务器监控": "Server Monitoring",
    "多平台数据同步": "Cross-platform Data Sync",
    "谁需要 tdRPA？": "Who needs tdRPA?",
    "企业白领": "White-collar Workers",
    "被重复工作折磨的运营、财务、HR 人员，告别重复劳动，释放创造力": "Operations, finance, and HR personnel tormented by repetitive tasks. Say goodbye to repetition and unleash your creativity.",
    "运营专员": "Ops Specialist",
    "财务人员": "Finance Staff",
    "HR": "HR",
    "行政人员": "Admin Staff",
    "中小企业主": "SME Owners",
    '追求效率与成本优化的企业决策者，以"数字员工"替代重复人力成本': 'Decision-makers seeking efficiency and cost optimization. Replace repetitive labor costs with "digital employees".',
    "降本增效": "Cost Reduction & Efficiency",
    "数字化转型": "Digital Transformation",
    "流程标准化": "Process Standardization",
    "Python 开发者": "Python Developers",
    "追求极致开发体验的专业程序员，无缝调用 Pandas、OpenCV、AI 大模型等库": "Pro programmers seeking an ultimate dev experience. Seamlessly call Pandas, OpenCV, and AI models.",
    "纯 Python 内核": "Pure Python Kernel",
    "RESTful API": "RESTful API",
    "上限极高": "Unlimited Potential",
    "场景无限，价值裂变": "Unlimited Scenarios, Fission of Value",
    "成本降低": "Cost Reduction",
    "效率提升": "Efficiency Increase",
    "出错率": "Error Rate",
    "不间断运行": "Continuous Operation",
    "把工作交给 tdRPA，把生活还给自己<br>数据技术驱动每一刻价值裂变": "Leave work to tdRPA, give life back to yourself<br>Data technology drives value fission every moment",
    "开启自动化之旅": "Start Automation Journey",
    "使用微信扫码联系": "Contact via WeChat QR",
    "tdRPA — 构建新质生产力，助力社会数字化": "tdRPA — Building New Productive Forces, Assisting Social Digitalization"
}

i18n_json = json.dumps(i18n_dict, ensure_ascii=False, indent=4)

js_logic = f"""
        // ===== Language Toggle Logic =====
        const i18n = {i18n_json};
        const textNodes = [];

        function initI18n(node) {{
            if (node.nodeType === 3) {{
                let text = node.nodeValue.trim();
                if (text && i18n[text]) {{
                    textNodes.push({{ node, zh: text, en: i18n[text], isHtml: false }});
                }}
            }} else if (node.nodeType === 1) {{
                if (node.tagName !== "SCRIPT" && node.tagName !== "STYLE") {{
                    let htmlContent = node.innerHTML.trim();
                    if (i18n[htmlContent]) {{
                        textNodes.push({{ node, zh: htmlContent, en: i18n[htmlContent], isHtml: true }});
                        return; // Done for this node tree
                    }}
                    if (node.tagName === 'TITLE') {{
                        if (i18n[htmlContent]) {{
                            textNodes.push({{ node, zh: htmlContent, en: i18n[htmlContent], isHtml: true }});
                        }}
                    }}
                    for (let i = 0; i < node.childNodes.length; i++) {{
                        initI18n(node.childNodes[i]);
                    }}
                }}
            }}
        }}

        // Wait for DOM to load
        document.addEventListener('DOMContentLoaded', () => {{
            initI18n(document.body);
            initI18n(document.head);
            
            const btnZh = document.getElementById('langZh');
            const btnEn = document.getElementById('langEn');
            
            function switchLang(lang) {{
                btnZh.classList.toggle('active', lang === 'zh');
                btnEn.classList.toggle('active', lang === 'en');
                
                textNodes.forEach(item => {{
                    const targetText = lang === 'en' ? item.en : item.zh;
                    if (item.isHtml) {{
                        item.node.innerHTML = targetText;
                    }} else {{
                        item.node.nodeValue = targetText;
                    }}
                }});
                
                // Keep html lang attribute correct
                document.documentElement.lang = lang === 'en' ? 'en' : 'zh-CN';
            }}
            
            btnZh.addEventListener('click', () => switchLang('zh'));
            btnEn.addEventListener('click', () => switchLang('en'));
        }});
"""

if '// ===== Language Toggle Logic =====' not in html:
    html = html.replace('// ===== Slide Logic =====', f'{js_logic}\\n        // ===== Slide Logic =====')

with open(HTML_FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print("Modification complete.")
