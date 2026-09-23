# Schema của `data.json`

Cả `build_scorecard.py` và `build_memo.py` đọc cùng một file này. Điền sau khi nghiên cứu. Xem `example-data.json` để có khuôn mẫu đầy đủ đã điền.

## Cấu trúc

```jsonc
{
  "sector_title": "NGÀNH KHOÁNG SẢN",          // tiêu đề lớn của memo
  "subtitle": "Sáu tiêu chí đánh giá & so sánh …",
  "report_date": "17/07/2026",                  // ngày lập báo cáo
  "data_date": "16/07/2026",                    // ngày của số liệu
  "context": [                                   // 1–3 đoạn bối cảnh ngành
    "Đoạn 1 …",
    "Đoạn 2 …"
  ],

  // Trọng số 6 tiêu chí (tùy chọn — bỏ trống để dùng mặc định 25/10/20/20/15/10).
  // Tổng phải = 1.0
  "weights": {
    "reserves": 0.25, "production": 0.10, "margin": 0.20,
    "fcf": 0.20, "debt": 0.15, "valuation": 0.10
  },

  "companies": [
    {
      "ticker": "KSV",
      "commodity": "đồng–vàng–đất hiếm",
      // Các ô hiển thị trong bảng so sánh của memo & sheet dữ liệu nền:
      "reserves":  "Sin Quyền ~52,8tr t; Đông Pao 1,1tr t REO — dài, đa dạng",
      "production":"~918 kg vàng; 30.079 t đồng tấm",
      "net_margin":"15,7%",
      "fcf_debt":  "FCF ~10%; tiền mặt ròng (D/E 0,30)",
      "roe":       "46,6%",
      "pe":        "11,6",
      "ev_ebitda": "6,6",
      // Điểm 1–5 cho 6 tiêu chí (bắt buộc, số nguyên 1..5):
      "scores": {
        "reserves": 4, "production": 4, "margin": 4,
        "fcf": 4, "debt": 5, "valuation": 4
      }
    }
    // … thêm các mã khác
  ],

  // Đoạn văn so sánh cho từng mục tiêu chí trong memo (tùy chọn nhưng nên có).
  // Nếu bỏ trống, memo chỉ in phần "vì sao quan trọng" mặc định.
  "criteria_notes": {
    "reserves":  "So sánh trữ lượng/đời mỏ giữa các mã …",
    "production":"So sánh sản lượng …",
    "margin":    "So sánh biên LN …",
    "fcf":       "So sánh FCF …",
    "debt":      "So sánh nợ …",
    "valuation": "So sánh định giá …"
  },

  "conclusions": [                               // xếp hạng & luận điểm ngắn từng mã
    { "ticker": "KSV", "note": "cân bằng tốt nhất: đầu ngành, lãi kỷ lục …" }
  ],
  "sources": "stockanalysis.com; BCTN doanh nghiệp; cafef/tinnhanhchungkhoan (16/07/2026)."
}
```

## Ghi chú
- `scores` là bắt buộc và phải đủ 6 khóa: `reserves, production, margin, fcf, debt, valuation`.
- Các trường chuỗi (reserves, production, fcf_debt…) hiển thị nguyên văn — viết ngắn gọn, có đơn vị.
- Thứ tự `conclusions` nên theo thứ tự ưu tiên (mã tốt nhất trước).
- Để trống `criteria_notes` một khóa nào đó thì mục tương ứng trong memo chỉ có phần khung; nên điền để memo giàu nội dung.
