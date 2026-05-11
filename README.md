# Dự án: PHÂN TÍCH DỮ LIỆU GIAO DỊCH TRÊN NỀN TẢNG INSTACART NHẰM TĂNG SỐ LƯỢNG SẢN PHẨM BÁN RA TRÊN MỖI ĐƠN HÀNG
## Giảng viên hướng dẫn: TS. Lê Diên Tuấn
### Nhóm: 1
### Thành viên: Đinh Hoài Nam, Bùi Quang Huy, Nguyễn Hoàng Duy



## Mô tả ngắn
Hệ thống được chia làm hai phần chính:
1. **Luật kết hợp (Association Rules):** Phân cụm khách hàng - để giảm chi phí tính toán luật kết hợp về sau và Phân tích tập dữ liệu khách hàng và đơn hàng để khai phá các luật kết hợp (Association rules).
2. **Recomendation base:** Hệ thống gợi ý ứng dụng các luật kết hợp đã được trích xuất để đưa ra các gợi ý sản phẩm phù hợp.

## Cài đặt (Installation)
Đầu tiên, mở terminal/cmd tại đường dẫn thư mục gốc 
Dự án yêu cầu Python. Để cài đặt môi trường và các thư viện phụ thuộc, hãy chạy lệnh sau cho từng phần của dự án:

```bash
# Tạo môi trường ảo
python -m venv .env
./.env/Scripts/activate.ps1
```
Sau đó, cài đặt thư viện được sử dụng cho các phần
```bash
# Cài đặt thư viện cho phần Luật kết hợp
pip install -r "Luật kết hợp/requirements.txt"

# Cài đặt thư viện cho phần Ứng dụng Gợi ý
pip install -r "Recomendation base/requirements.txt"
```

## Hướng dẫn sử dụng (Usage)
- **Khai phá dữ liệu:** Truy cập vào thư mục `Luật kết hợp/` và mở các file Jupyter Notebook (`EDA.ipynb`, `AssociationRules.ipynb`) để xem quá trình phân tích dữ liệu và sinh luật kết hợp.
- **Chạy ứng dụng Gợi ý:** Truy cập vào thư mục `Recomendation base/` và khởi chạy file `app.py`:
  ```bash
  cd "Recomendation base"
  python app.py
  ```
    hoặc sử dụng câu lệnh sau nếu câu lệnh trên không hoạt động:
    ``` bash
    streamlit run app.py 
    ```

## Cấu trúc dự án (Project Structure)
```text
Cap1/
├── Luật kết hợp/           # Thư mục xử lý dữ liệu và khai phá luật
│   ├── Data/               # Chứa dữ liệu đầu vào (orders, products, aisles...)
│   ├── Output/             # Chứa kết quả luật sinh ra dưới dạng CSV
│   ├── EDA.ipynb           # Notebook phân tích dữ liệu khám phá
│   ├── AssociationRules.ipynb # Notebook chạy thuật toán Apriori/FP-Growth khai phá luật
│   └── requirements.txt    # Các thư viện Python cần thiết
│
└── Recomendation base/     # Ứng dụng hệ thống gợi ý
    ├── Rule/               # Chứa các file kết quả luật từ thư mục Output
    ├── app.py              # File chạy ứng dụng web giao diện
    ├── recommender.py      # Logic chính xử lý hệ thống gợi ý
    └── requirements.txt    # Các thư viện Python cần thiết 
```

## Giấy phép (License)
Dự án được phân phối cho mục đích học tập. 

## Thông tin tác giả/liên hệ (Author/Contact)
- **Tác giả:** [Đinh Hoài Nam, Bùi Quang Huy, Nguyễn Hoàng Duy]
- **Email:** [buiquanghuy352k5.com]
- **Môn học:** Đề án thực hành 1
