#!/bin/bash

echo "================================"
echo "🔍 Redis Data Comparison"
echo "================================"
echo ""

echo "📍 LOCAL REDIS (localhost:6379)"
echo "--------------------------------"
echo "All keys:"
redis-cli KEYS "*"
echo ""
echo "Session count:"
redis-cli KEYS "session:*" | wc -l
echo ""
echo "Stats - Scams detected:"
redis-cli GET "stats:public_guest:scams_detected"
echo ""

echo "================================"
echo ""

echo "☁️  UPSTASH REDIS (cloud)"
echo "--------------------------------"
UPSTASH_URL="rediss://default:AV1uAAIncDIzNjIwOTY3ZGNkMzI0NDIzODQ0ODM2MjliZmU0ZmJmMXAyMjM5MTg@factual-marmot-23918.upstash.io:6379"

echo "All keys:"
redis-cli --tls -u "$UPSTASH_URL" KEYS "*"
echo ""
echo "Session count:"
redis-cli --tls -u "$UPSTASH_URL" KEYS "session:*" | wc -l
echo ""
echo "Stats - Scams detected:"
redis-cli --tls -u "$UPSTASH_URL" GET "stats:public_guest:scams_detected"
echo ""

echo "================================"
echo "✅ Comparison Complete"
echo "================================"
