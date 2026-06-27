#!/bin/bash
# Generate news images for 2026年06月28日

DATE_STR="20260628"
API_KEY="88d03a7652c24d3c8bfab66f061698a8.ZQWZhWZyiEdW4mDB"
IMG_DIR="/home/swg/.openclaw/workspace/news-blog/images"
mkdir -p "$IMG_DIR"

# Image prompts for all 20 news items
declare -A PROMPTS
PROMPTS["01"]="Chinese scientists in a advanced semiconductor laboratory examining a AI chip under microscope, photorealistic, ultra detailed, 8K, professional laboratory environment with blue lighting"
PROMPTS["02"]="World leaders at an international summit conference hall, flags of BRICS nations displayed, photorealistic, ultra detailed, 8K, diplomatic meeting with elegant interior design"
PROMPTS["03"]="Stock market trading floor with large digital displays showing rising stock prices, investors watching screens, photorealistic, ultra detailed, 8K, modern financial district backdrop"
PROMPTS["04"]="Huawei product launch event showing smartphone running new OS with futuristic interface, photorealistic, ultra detailed, 8K, modern tech conference stage with dramatic lighting"
PROMPTS["05"]="Busy international shipping port with containers and cargo ships, e-commerce packages being sorted, photorealistic, ultra detailed, 8K, aerial view of modern logistics hub"
PROMPTS["06"]="Modern electric car factory assembly line with humanoid robots, photorealistic, ultra detailed, 8K, sleek electric vehicle being assembled in clean modern factory"
PROMPTS["07"]="Chinese astronauts in space suits performing spacewalk outside space station, Earth visible in background, photorealistic, ultra detailed, 8K, dramatic space scene with solar panels"
PROMPTS["08"]="Modern city skyline with residential buildings and urban development, photorealistic, ultra detailed, 8K, aerial view of prosperous city with green spaces"
PROMPTS["09"]="International conference on AI governance with diverse world leaders and tech executives, photorealistic, ultra detailed, 8K, elegant conference room with digital AI visualization"
PROMPTS["10"]="Tang Dynasty ancient Chinese palace with poetic atmosphere, traditional Chinese ink painting style scene, photorealistic, ultra detailed, 8K, beautiful ancient Chinese architecture with mountains and rivers"
PROMPTS["11"]="Electric car charging station with Chinese brand EVs charging, European city background, photorealistic, ultra detailed, 8K, modern sustainable transportation scene"
PROMPTS["12"]="SpaceX Starship rocket launching from pad with massive flames, photorealistic, ultra detailed, 8K, dramatic rocket launch at dawn with smoke trails"
PROMPTS["13"]="Digital payment concept with Chinese yuan symbol and smartphone payment interface, photorealistic, ultra detailed, 8K, futuristic financial technology visualization"
PROMPTS["14"]="Extreme summer heat wave scene with temperature display showing 40 degrees, people with umbrellas on hot street, photorealistic, ultra detailed, 8K, urban summer heat scene with visible heat shimmer"
PROMPTS["15"]="World AI conference exhibition hall with robot displays and futuristic technology exhibits, photorealistic, ultra detailed, 8K, modern tech exhibition with visitors interacting with AI"
PROMPTS["16"]="Table tennis match in international stadium, Chinese player serving with determined expression, photorealistic, ultra detailed, 8K, sports arena with cheering crowd"
PROMPTS["17"]="Lush green forest belt bordering desert landscape in Inner Mongolia, trees and vegetation preventing desert expansion, photorealistic, ultra detailed, 8K, beautiful nature scene with green vegetation meeting sandy desert"
PROMPTS["18"]="Smartphone showing social media app with billions of users, colorful interface, photorealistic, ultra detailed, 8K, modern digital content creation scene"
PROMPTS["19"]="China-Europe freight train on cross-border railway bridge, loaded with containers, photorealistic, ultra detailed, 8K, modern railway infrastructure connecting different countries"
PROMPTS["20"]="Scientists in laboratory observing nuclear fusion experiment with plasma glow, photorealistic, ultra detailed, 8K, advanced scientific research facility with fusion reactor"

generate_image() {
    local num=$1
    local prompt=$2
    local output="${IMG_DIR}/news_${DATE_STR}_${num}.png"
    
    echo "Generating image ${num}..."
    
    # Call API and extract URL from response
    local response=$(curl -s -X POST "https://open.bigmodel.cn/api/paas/v4/chat/completions" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer ${API_KEY}" \
        -d "{\"model\": \"cogview-3-flash\", \"messages\": [{\"role\": \"user\", \"content\": \"Image prompt: ${prompt}\"}]}" \
        --max-time 60)
    
    # Extract URL from JSON response - the URL is in content[0].url
    local url=$(echo "$response" | python3 -c "import sys, json; d=json.load(sys.stdin); print(d['choices'][0]['message']['content'][0]['url'])" 2>/dev/null)
    
    if [ -n "$url" ]; then
        # Download the image
        curl -s -L "$url" --max-time 30 -o "$output"
        if [ -s "$output" ]; then
            echo "  Saved: $output"
            return 0
        else
            echo "  Failed to download: $url"
            return 1
        fi
    else
        echo "  Failed to get URL from API response"
        return 1
    fi
}

# Generate all 20 images
for i in $(seq -w 1 20); do
    generate_image "$i" "${PROMPTS[$i]}"
    sleep 1
done

echo ""
echo "Done! Images generated:"
ls -la "${IMG_DIR}"/news_${DATE_STR}_*.png 2>/dev/null | wc -l