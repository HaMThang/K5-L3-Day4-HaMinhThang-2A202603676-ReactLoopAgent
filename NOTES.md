# Ghi chú phân tích · Day 04

Họ và tên: Hà Minh Thắng
MSSV: 2A202603676

## 1. Case được chọn

- ID case: E1
- Câu trả lời của agent: Hiện tại, GitHub Actions đang trong trạng thái \"operational\" và không có sự cố nào đang diễn ra. Tất cả các hệ thống đều hoạt động bình thường.\n\nGần đây, đã có một số sự cố đã được ghi nhận và đã được giải quyết. Dưới đây là một số incident gần đây liên quan đến GitHub Actions:\n\n1. **Incident with Actions**\n   - Trạng thái: Đã giải quyết\n   - Cập nhật lần cuối: 5 tháng 11, 2026\n\n2. **Degraded performance for multiple GitHub services**\n   - Trạng thái: Đã giải quyết\n   - Cập nhật lần cuối: 6 tháng 11, 2026\n\n3. **Incident with Actions and Pages**\n   - Trạng thái: Đã giải quyết\n   - Cập nhật lần cuối: 7 tháng 11, 2026\n\nThông tin chi tiết về incident có thể được tìm thấy tại [GitHub Status](https://www.githubstatus.com).
- Điểm ở lần chạy 1: 75

## 2. Bằng chứng trong trace

**Xác nhận lại từ `eval_before.json` (E1):** trace gọi `get_status(provider="github", component="GitHub Actions")`. Tool trả `captured_at=2026-11-09T03:50:47.065020+00:00`, `overall.indicator="none"` (“All Systems Operational”) và các incident gần đây đều có trạng thái `resolved`. Agent trả lời không có sự cố đang diễn ra nhưng vẫn liệt kê nhiều incident cũ; judge nhận xét câu trả lời chưa tập trung vào trạng thái tại snapshot.

**Đối chiếu trace mới nhất (`eval_after_with_judge.json`, E1):** agent kiểm tra status rồi lấy chi tiết incident, có dẫn URL và đánh dấu incident đã resolved. Judge chấm 92/100 nhưng vẫn lưu ý cách diễn giải thời điểm resolved chưa chính xác và câu trả lời chưa nói rõ `GitHub overall = none`. Lỗi đã giảm nhưng chưa được xử lý hoàn toàn.

## 3. Thay đổi đã thực hiện

- Sửa gì, ở đâu: Sửa lại System_promt
- Vì sao chọn thay đổi này: Vì dự đoán promt chưa rõ ràng sau khi đọc các imporvement.

## 4. Tổng hợp các lần chạy

| Chỉ số | `eval_before` | `eval_after` | `after_v1` | `after_v2` | `after_with_judge` |
|---|---:|---:|---:|---:|---:|
| Điểm tổng (22 case) | 77.73 | 74.09 | 81.14 | 82.41 | **86.32** |
| Điểm E1 | 75 | 55 | 70 | 75 | **92** |
| Judge | gpt-4o-mini | gpt-4o-mini | gpt-4o-mini | gpt-4o-mini | **gpt-6-luna** |
| Calls (agent + judge) | 53 + 22 | 48 + 22 | 45 + 22 | 48 + 22 | 53 + 22 |
| Token (prompt / completion / tổng) | 69,816 / 13,405 / 83,221 | 64,210 / 8,966 / 73,176 | 103,512 / 8,276 / 111,788 | 87,651 / 11,313 / 98,964 | 89,684 / 19,786 / 109,470 |
| Chi phí | Không có dữ liệu | Không có dữ liệu | Không có dữ liệu | Không có dữ liệu | Không có dữ liệu |

- **Đã cải thiện:** E1 nói rõ trạng thái tại snapshot; ở lượt mới nhất có URL nguồn và phân loại incident là resolved.
- **Còn tồn tại:** diễn giải thời điểm resolved chưa chính xác, chưa nêu rõ overall là `none`; 

## 5. Giới hạn

- **Judge:** điểm là ước lượng kết hợp kiểm tra bằng code, không phải xác nhận tuyệt đối. Hầu hết lần chạy dùng `gpt-4o-mini`; `eval_after_with_judge` dùng `gpt-6-luna`, nên chênh lệch điểm không chỉ phản ánh thay đổi agent.
- **Snapshot:** dữ liệu cố định tại `2026-11-09T03:50:47.065020+00:00`, không đại diện status hiện tại. Tool chỉ tìm tối đa 50 incident gần nhất và có thể lược bớt nội dung update.
- **Số lần chạy:** mỗi phiên bản chỉ có một lượt; kết quả có thể dao động theo lần sinh của agent và judge, không chứng minh system prompt là nguyên nhân duy nhất hay cải thiện ổn định.

**Kết luận:** `eval_after_with_judge` có điểm cao nhất (86.32/100; E1 92) và xác nhận được `gpt-6-luna`, nhưng chưa phải phép so sánh chỉ thay judge. E1 đã có nguồn và nhận diện incident resolved tốt hơn, song vẫn cần sửa cách diễn giải thời điểm resolved và nêu rõ overall `none`. Cần chạy lặp lại cùng cấu hình và xem trace các case yếu trước khi kết luận cải thiện bền vững.
