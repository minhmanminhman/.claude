---
name: mining-sector-analysis
description: >-
  Phân tích và so sánh nhóm cổ phiếu khoáng sản Việt Nam (khai thác & chế biến kim
  loại/khoáng sản niêm yết trên HOSE/HNX/UPCoM — ví dụ KSV, MSR, HGM, BKC, BMC, KSB,
  KSB, than-Vinacomin) theo sáu tiêu chí then chốt và xuất ra một MEMO phân tích
  chuyên nghiệp (.docx) cùng một BẢNG CHẤM ĐIỂM (.xlsx). Hãy dùng skill này bất cứ
  khi nào người dùng muốn đánh giá, so sánh, sàng lọc, hay viết báo cáo về cổ phiếu
  khoáng sản/kim loại Việt Nam — kể cả khi họ chỉ nêu một mã (ví dụ "phân tích KSV
  và các mã cùng ngành") mà không nói rõ chữ "memo" hay "khoáng sản". Trigger trên
  các cụm như: phân tích ngành khoáng sản, so sánh cổ phiếu khoáng sản, đánh giá mỏ,
  trữ lượng/sản lượng/AISC, cổ phiếu kim loại (đồng, vàng, vonfram, antimon, đất
  hiếm, kẽm, titan), memo/báo cáo phân tích khoáng sản. KHÔNG dùng cho phân tích
  ngành phi khoáng sản, hay khi người dùng chỉ hỏi giá cổ phiếu đơn thuần.
---

# Phân tích ngành khoáng sản (Việt Nam) → Memo + Bảng chấm điểm

## Skill này làm gì

Biến một yêu cầu kiểu "phân tích KSV và các mã cùng ngành" thành hai sản phẩm hoàn chỉnh:
1. **Memo phân tích (.docx)** — phong cách báo cáo của công ty chứng khoán Việt Nam: tiêu đề, các mục rõ ràng, văn phong cô đọng, bảng so sánh, kết luận.
2. **Bảng chấm điểm (.xlsx)** — chấm 1–5 có trọng số trên sáu tiêu chí, tự tính điểm tổng và xếp hạng bằng công thức.

Cả hai được dựng từ **một file dữ liệu duy nhất `data.json`** mà bạn điền sau khi nghiên cứu, nên số liệu luôn nhất quán giữa memo và bảng chấm điểm.

## Vì sao khoáng sản cần khung riêng

Doanh nghiệp khoáng sản khác biệt căn bản: đây là **tài sản cạn kiệt dần** (mỗi tấn khai thác là một tấn trữ lượng mất đi — nên P/E rẻ trên một mỏ sắp hết đời là "rẻ" ảo) và phần lớn là **doanh nghiệp chấp nhận giá** (lợi nhuận do giá hàng hóa thế giới chi phối hơn là nội lực). Vì vậy thứ tự đánh giá đúng là: *mỏ còn khai thác bao lâu → chi phí có đủ thấp → dòng tiền thực sau đầu tư → bảng cân đối chịu được đáy giá → rồi mới đến định giá.* Sáu tiêu chí dưới đây bám đúng trật tự này.

## Sáu tiêu chí (trọng số mặc định)

| # | Tiêu chí | Trọng số | Vì sao quan trọng (tóm tắt) |
|---|----------|:---:|---|
| 1 | Trữ lượng & tuổi thọ mỏ | 25% | Đặc thù nhất; R/P thấp thì "rẻ" là ảo |
| 2 | Sản lượng khai thác | 10% | Tách bạch tăng trưởng do lượng hay do giá |
| 3 | Biên lợi nhuận | 20% | Proxy cho vị thế chi phí; ai sống qua đáy giá |
| 4 | Dòng tiền tự do (FCF) | 20% | EBITDA đẹp nhưng FCF có thể âm; ngành ngốn vốn |
| 5 | Nợ & bảng cân đối | 15% | Nợ cao + LN biến động = nguy hiểm |
| 6 | Định giá | 10% | Ưu tiên EV/EBITDA & P/NAV hơn P/E chu kỳ |

Chi tiết từng tiêu chí, thang điểm 1–5 và nguồn dữ liệu: đọc **`references/criteria.md`** trước khi chấm điểm. Đừng chấm điểm theo cảm tính — mỗi điểm phải neo vào một dữ kiện.

## Quy trình

### Bước 1 — Xác định mã trung tâm và nhóm cùng ngành
Từ mã người dùng nêu, xác định khoáng sản chủ lực rồi lập nhóm so sánh các mã khai khoáng niêm yết cùng/gần phân ngành. Gợi ý bản đồ ngành có trong `references/criteria.md` (đồng/vàng, vonfram, antimon, kẽm/chì, titan, đất hiếm, than…). Thường 4–6 mã là đủ. **Luôn kiểm tra mã còn niêm yết/giao dịch** — ngành khoáng sản VN có nhiều vụ sáp nhập/hủy niêm yết (ví dụ TC6, TDN đã sáp nhập). Nếu một mã người dùng nêu đã hủy niêm yết, ghi rõ và thay bằng mã kế thừa.

### Bước 2 — Thu thập số liệu tài chính & thị trường
Với mỗi mã, lấy số liệu mới nhất (giá, vốn hóa, P/E, P/B, EV/EBITDA, ROE, biên LN ròng, cổ tức, tình trạng nợ/FCF). Nguồn và cách tra: `references/criteria.md` (mục "Nguồn dữ liệu"). Luôn ghi **ngày dữ liệu**.

### Bước 3 — Trích trữ lượng, sản lượng, chi phí từ báo cáo thường niên
Đây là phần tạo khác biệt so với một bảng so sánh thông thường. Tìm báo cáo thường niên (BCTN) mới nhất của doanh nghiệp để lấy **trữ lượng mỏ, đời mỏ, sản lượng khai thác/năm**, và **giá vốn/biên** (lưu ý: doanh nghiệp VN hầu như không công bố AISC/giá thành đơn vị — dùng biên LN làm proxy và ghi rõ giới hạn này). Cách tìm BCTN: `references/criteria.md`.

### Bước 4 — Điền `data.json`
Sao chép **`references/example-data.json`** làm khuôn, điền dữ liệu và chấm điểm 1–5 cho sáu tiêu chí của từng mã. Schema đầy đủ: `references/data-schema.md`.

### Bước 5 — Sinh bảng chấm điểm và memo
Chạy hai script (đọc cùng `data.json`):

```bash
python scripts/build_scorecard.py data.json Bang_cham_diem.xlsx
python scripts/build_memo.py data.json Memo_phan_tich.docx
# Nạp giá trị cache cho công thức Excel (để bảng hiện điểm ở mọi trình xem):
python /root/.claude/skills/xlsx/scripts/recalc.py Bang_cham_diem.xlsx   # hoặc: soffice --headless --convert-to xlsx
```

`build_scorecard.py` dùng công thức SUMPRODUCT + RANK (không hardcode kết quả) nên đổi điểm/trọng số là bảng tự cập nhật — nhưng openpyxl không ghi sẵn giá trị, vì vậy **phải chạy recalc** sau khi tạo, nếu không bảng sẽ trống điểm khi mở. `build_memo.py` dựng memo phong cách CTCK: tiêu đề, 6 mục tiêu chí, bảng so sánh, kết luận & thứ tự ưu tiên, tuyên bố miễn trừ (đã bỏ mục "Bước tiếp theo").

### Bước 6 — Kiểm tra và bàn giao
Kết xuất PDF để soi memo (`soffice --headless --convert-to pdf`), kiểm tra bảng Excel không lỗi công thức, rồi giao cả hai file cho người dùng (kèm nguồn dẫn). Nếu người dùng đã kết nối thư mục trên máy, lưu file vào đó.

## Văn phong (bám sát báo cáo phân tích CTCK Việt Nam)
Memo phải đọc như báo cáo của khối phân tích một công ty chứng khoán (SSI, VCSC, HSC, VNDirect…): cô đọng, dẫn dắt bằng số liệu, dùng ngôi "chúng tôi". Khi điền `context`, `criteria_notes`, `conclusions` trong `data.json`, viết theo văn phong đó — ưu tiên các cụm chuẩn ngành: "luận điểm đầu tư", "động lực tăng trưởng", "rủi ro chính", "chúng tôi cho rằng/đánh giá", "định giá", "biên lợi nhuận", "dòng tiền", "chất xúc tác". Câu ngắn, mỗi câu một ý; tránh văn nói, tránh cảm thán. Không đưa khuyến nghị Mua/Bán/giá mục tiêu (skill là tài liệu tham khảo, có miễn trừ) nhưng vẫn giữ giọng phân tích sắc, có quan điểm.

## Xử lý phân ngành đặc thù (quan trọng)
Khung sáu tiêu chí giả định doanh nghiệp **sở hữu mỏ** và **chấp nhận giá thị trường**. Một số phân ngành phá vỡ giả định này — cần điều chỉnh và nói rõ trong memo:
- **Than Vinacomin (NBC, TVD, THT, HLC, MDC…):** các công ty con **không sở hữu trữ lượng** (TKV giao mỏ) và **không tự định giá bán** (giá chuyển giao/bao tiêu nội bộ TKV), nên biên LN gần như đồng đều 1–3% và tiêu chí "biên = vị thế chi phí" mất nhiều ý nghĩa. Với nhóm này, tiêu chí trữ lượng nên hiểu là **đời mỏ theo lộ trình đóng cửa của TKV + lộ thiên vs hầm lò**, và ghi rõ mô hình khoán chi phí làm biên kém phân hóa. Nêu các điểm này ở phần bối cảnh và ghi chú tiêu chí.
- Nguyên tắc chung: nếu một giả định nền không đúng với đối tượng, hãy nói thẳng và diễn giải lại tiêu chí cho phù hợp, thay vì chấm điểm máy móc.

## Nguyên tắc chất lượng
- **Ghi rõ mốc thời gian & nguồn** cho mọi con số; phân biệt "thực hiện" vs "kế hoạch".
- **Trung thực về khoảng trống dữ liệu** — nếu không lấy được trữ lượng/AISC, nói rõ đó là đánh giá định tính, đừng bịa số.
- **Không kết luận mua/bán**; skill sản xuất khung phân tích tham khảo, luôn kèm tuyên bố miễn trừ.
- Điều chỉnh quy mô theo yêu cầu: "nhìn nhanh" thì 4 mã; "phân tích kỹ" thì mở rộng nhóm và đào BCTN sâu hơn.
