#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Actions에서 실행: 네이버에서 종목 데이터를 받아 data.json으로 저장
"""
import json, datetime, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

# 조회할 종목 목록
STOCKS = ["005010", "018880", "458250"]

def fetch(url):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        print(f"  오류: {e}")
        return None

def get_stock_data(code):
    print(f"[{code}] 데이터 수집 중...")
    integ  = fetch(f"https://m.stock.naver.com/api/stock/{code}/integration")
    trend  = fetch(f"https://m.stock.naver.com/api/stock/{code}/trend")
    annual = fetch(f"https://m.stock.naver.com/api/stock/{code}/finance/annual")
    return {"integ": integ, "trend": trend, "annual": annual}

result = {}
for code in STOCKS:
    result[code] = get_stock_data(code)

now = (datetime.datetime.utcnow() + datetime.timedelta(hours=9)).strftime("%Y-%m-%d %H:%M")
output = {"updated": now, "stocks": result}

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\n완료! data.json 저장됨 (업데이트: {now})")
