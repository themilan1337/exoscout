#!/usr/bin/env bash
# =========================================================
# 🚀 ExoScout API Functional Test Suite (curl-based)
# =========================================================
# Usage:
#   chmod +x tests.sh
#   ./tests.sh
# =========================================================

BASE_URL="https://ocie-coua-exquisitely.ngrok-free.dev/api/v1"
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

function test_endpoint() {
  local name=$1
  local url=$2
  local expect=$3
  echo -e "\n🛰️  Testing: ${GREEN}$name${NC}"
  echo "→ URL: $url"
  response=$(curl -s -w "\n%{http_code}" "$url")
  body=$(echo "$response" | head -n1)
  code=$(echo "$response" | tail -n1)
  if [[ $code == "$expect" ]]; then
    echo -e "✅ ${GREEN}OK${NC} (status $code)"
  else
    echo -e "❌ ${RED}FAILED${NC} (status $code)"
  fi
  echo "Response: $body"
}

echo "========================================================="
echo "🧪 Starting ExoScout API tests..."
echo "Base URL: $BASE_URL"
echo "========================================================="

# 1️⃣ Health check
test_endpoint "Health Check" "$BASE_URL/health" "200"

# 2️⃣ Resolve TOI target
test_endpoint "Resolve TESS target (TOI-1019.01)" "$BASE_URL/resolve/TOI-1019.01" "200"

# 3️⃣ Features endpoint (TESS)
test_endpoint "TESS Features (TIC 307210830)" "$BASE_URL/features/TESS/307210830" "200"

# 4️⃣ Lightcurve endpoint (TESS)
test_endpoint "Lightcurve (TESS 307210830)" "$BASE_URL/lightcurve/TESS/307210830" "200"

# 5️⃣ Prediction endpoints for all missions
test_endpoint "Predict TESS" "$BASE_URL/predict/TESS/307210830" "200"
test_endpoint "Predict Kepler" "$BASE_URL/predict/KEPLER/10666592" "200"
test_endpoint "Predict K2" "$BASE_URL/predict/K2/206103150" "200"

# 6️⃣ Models status
test_endpoint "Models Status" "$BASE_URL/predict/models/status" "200"

# 7️⃣ Caching check (TESS prediction repeated)
echo -e "\n⚡ Testing caching performance..."
time curl -s "$BASE_URL/predict/TESS/307210830" -o /dev/null
time curl -s "$BASE_URL/predict/TESS/307210830" -o /dev/null

echo -e "\n========================================================="
echo -e "${GREEN}✅ All ExoScout API tests completed.${NC}"
echo "========================================================="
