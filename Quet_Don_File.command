#!/bin/bash
# Chuyển đến thư mục hiện tại của script
cd "$(dirname "$0")"

echo "======================================================"
echo "   ZALO STUDY AGENT - QUÉT VÀ PHÂN LOẠI TÀI LIỆU"
echo "======================================================"
echo ""

# Chạy chế độ quét 1 lần (On-demand scan)
python3 agent_classifier.py

echo ""
echo "======================================================"
read -p "Hoàn tất! Nhấn phím [Enter] để đóng cửa sổ này..."
