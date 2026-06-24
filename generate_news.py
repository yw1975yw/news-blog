import requests
import os
import time

API_KEY = "88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
ENDPOINT = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
MODEL = "cogview-3-flash"

# News content for 2026年06月25日
news_items = [
    {"title": "联合国安理会通过AI军事应用决议 禁止自主致命武器", "tag": "国际", "prompt": "UN Security Council adopts resolution on AI military applications, banning autonomous lethal weapons, diplomatic meeting, solemn atmosphere, news illustration, 8k quality"},
    {"title": "中美重启贸易谈判 双方在华盛顿举行高层磋商", "tag": "国际", "prompt": "China US trade talks resume in Washington, high-level diplomatic meeting, bilateral negotiations, news illustration, 8k quality"},
    {"title": "欧盟对华电动汽车加征关税 商务部回应表示不满", "tag": "国际", "prompt": "EU imposes tariffs on Chinese electric vehicles, Chinese Commerce Ministry responds, trade tension, news illustration, 8k quality"},
    {"title": "嫦娥七号成功着陆月球南极 开展水冰资源勘探", "tag": "科技", "prompt": "Chang'e-7 lunar probe lands on moon south pole, water ice exploration, Chinese space mission, news illustration, 8k quality"},
    {"title": "小米汽车SU8正式发布 搭载全新澎湃OS 2.0系统", "tag": "科技", "prompt": "Xiaomi SU8 electric car launch event, new Surge OS 2.0 system, new energy vehicle, news illustration, 8k quality"},
    {"title": "字节跳动推出AI搜索产品 挑战百度搜索霸主地位", "tag": "科技", "prompt": "ByteDance launches AI search product, challenging Baidu search dominance, technology news illustration, 8k quality"},
    {"title": "英伟达Blackwell Ultra芯片发布 AI算力再创新高", "tag": "科技", "prompt": "NVIDIA Blackwell Ultra chip release, AI computing power breakthrough, technology news illustration, 8k quality"},
    {"title": "百度文心大模型5.0发布 支持全模态实时交互", "tag": "科技", "prompt": "Baidu Wenxin large model 5.0 release, multimodal AI interaction, technology news illustration, 8k quality"},
    {"title": "A股三大指数集体下跌 成交额跌破1.5万亿元", "tag": "金融", "prompt": "Chinese stock market indices decline, trading volume drops below 1.5 trillion yuan, financial news illustration, 8k quality"},
    {"title": "人民币汇率跌破7.3 创年内新低", "tag": "金融", "prompt": "RMB exchange rate falls below 7.3, yearly low, currency market, financial news illustration, 8k quality"},
    {"title": "国际金价突破3000美元 创历史新高", "tag": "金融", "prompt": "Gold price breaks through $3000 per ounce, all-time high, precious metals market, financial news illustration, 8k quality"},
    {"title": "比特币失守10万美元关口 加密货币市场暴跌", "tag": "金融", "prompt": "Bitcoin falls below $100,000, cryptocurrency market crash, crypto trading, financial news illustration, 8k quality"},
    {"title": "全国多地暴雨洪涝 防汛应急响应提升至二级", "tag": "社会", "prompt": "Heavy rain and floods across China, flood prevention emergency response level 2, natural disaster, news illustration, 8k quality"},
    {"title": "新版婚育条例发布 鼓励生育配套政策落地", "tag": "社会", "prompt": "New marriage and childbirth regulations published, pro-birth policies implementation, social news illustration, 8k quality"},
    {"title": "北京常住人口突破2200万 继续领跑全国", "tag": "社会", "prompt": "Beijing permanent population exceeds 22 million, largest city in China, urban development, news illustration, 8k quality"},
    {"title": "国乒包揽世乒赛五冠 再次展现王者风范", "tag": "体育", "prompt": "Chinese table tennis team wins all five titles at World Championships, sports victory, news illustration, 8k quality"},
    {"title": "梅西宣布退出阿根廷国家队 无缘2026世界杯", "tag": "体育", "prompt": "Messi announces retirement from Argentina national team, 2026 World Cup absence, sports news illustration, 8k quality"},
    {"title": "故宫博物院推出数字分身 让游客与乾隆对话", "tag": "文化", "prompt": "Palace Museum launches digital twin, visitors interact with Emperor Qianlong, cultural technology, news illustration, 8k quality"},
    {"title": "中国科幻小说三体将改编为好莱坞电影", "tag": "文化", "prompt": "Chinese sci-fi novel Three-Body Problem adapted to Hollywood film, cultural export, news illustration, 8k quality"},
    {"title": "全国高考成绩公布 1300万考生迎来人生转折点", "tag": "社会", "prompt": "National college entrance examination results released, 13 million students, life turning point, news illustration, 8k quality"}
]

def generate_image(news_item, index):
    """Generate image using CogView API"""
    image_path = f"images/news_20260625_{index:02d}.png"
    
    if os.path.exists(image_path):
        print(f"Image {image_path} already exists, skipping...")
        return True
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": f"Generate a high-quality news illustration for: {news_item['prompt']}"
            }
        ],
        "max_tokens": 1024,
        "stream": False
    }
    
    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload, timeout=120)
        print(f"Response status for {index}: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Generated: {image_path}")
            return True
        else:
            print(f"Error for {index}: {response.text[:500]}")
            return False
    except Exception as e:
        print(f"Exception for {index}: {e}")
        return False

# Create images directory if not exists
os.makedirs("images", exist_ok=True)

# Generate images sequentially with retries
for i, news in enumerate(news_items, 1):
    success = False
    retries = 3
    while not success and retries > 0:
        success = generate_image(news, i)
        if not success:
            retries -= 1
            if retries > 0:
                print(f"Retrying {i}...")
                time.sleep(5)
    time.sleep(2)

print("\nImage generation complete!")
