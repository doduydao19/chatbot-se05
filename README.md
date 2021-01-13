# ChatbotH3D
ChatbotH3D là chatbot doanh nghiệp được xây dựng dựa trên dữ liệu của công ty House 3D.
Sản phẩm được xây dựng bởi nhóm sinh viên lớp máy tính và khoa học thông tin chất lượng cao K63A5, trường Đại học Khoa học Tự Nhiên, Đại học Quốc Gia Hà Nội.

Authors:

- Đỗ Duy Đạo - 18001030 - K63A5 - HUS
- Nguyễn Khánh Hòa - 18001041 - K63A5 - HUS
- Lê Huy - 18001045 - K63A5 - HUS

Reference:

- Build Facebook Messenger Contextual ChatBot with TensorFlow and Keras.
https://medium.com/@ferrygunawan/build-facebook-messenger-contextual-chatbot-with-tensorflow-and-keras-4f8cc79438cf

## Update

Phiên bản mới được đưa ra ở các bản *.1 có thể dùng được ổn định.
Các phiên bản đưa ra được thừa kế ở nhánh "dev".

## Requirement

- Python 3.6
- Tensorflow 1.7.0
- Flask==0.11.1
- Keras==2.1.5
- Uderthesea==1.2.3

Tải đầy đủ các yêu cầu bằng cách chạy dòng lệnh sau đây trong command line :
```
pip install -r requirements.txt 
```

## Get started
#### Tôi khuyến khích các bạn cài trên hệ điều hành Ubuntu
#### Nếu bạn chạy trên Window thì cần cài Anaconda
#### Clone the repository
```
git clone https://github.com/huyle73/SE05-N3.git
```

#### Data
- Data raw (Dữ liệu thô): là các tệp đã được sắp xếp vào các tệp có chứa chủ đề và câu hỏi câu trả lời của từng chủ đề.
- Dataset (Bộ dữ liệu): Tệp `intents.json` chứa toàn bộ dữ liệu của dữ liệu thô đã được chia theo chủ đề và các câu hỏi và trả lời kèm theo cùng với ngữ cảnh.

*** Nếu bạn muốn tạo bộ dữ liệu mới và đưa về đúng định dạng của file `intents.json` thì chạy file load_data_raw.py
```
 python load_data_raw.py
```

*** Kết quả của việc chạy file trên là file intents có định dạng như sau:
```
{
    "intents": [
        {
            "tag": "chức năng đóng góp mặt bằng",
            "questions": [],
            "answers": [],
            "contexture_lv1": "dựng tường",
            "contexture_lv2": "chức năng thiết kế cơ bản"
        },
        {
            "tag": "xuất bản vẽ sơ đồ mặt bằng",
            "questions": [],
            "answers": [],
            "contexture_lv1": "dựng tường",
            "contexture_lv2": "chức năng thiết kế cơ bản"
        },
        ...
        ]
}
```

#### Training
Ở đây chúng tôi có pretrained model ``H3D.h5`` chạy ổn định.

Nếu bạn muốn retrain model thì chuyển tới folder model và chạy file `model.py`
```
python model.py
```

Sau khi chạy hoàn tất sẽ có file `H3D.h5` và các file kèm theo ở trong thư mục `app` bao gồm:
```
- classes.pkl
- documents.pkl
- ignore_words.pkl
- words.pkl
```
*** Khi chạy hoàn tất sẽ có chỉ số đánh giá mô hình, với độ chính xác trên 0.9 thì có thể chấp nhận được.

#### Testing

Chạy file ``test_model.py`` để test model và chat `thoát` để thoát khỏi chương trình.

#### Deploy on Facebook

#### Ở đây chúng tôi xử dụng nền tảng ``Flask`` và free server ``Heroku`` để xây dựng web app.

####1. Build app

Các bạn cần đăng kí tài khoản [Heroku](http://heroku.com/) tại đây.
Và tải heroku về bằng lệnh:
```
sudo snap install --classic heroku
```
sau đó chạy các lệnh sau để đẩy app lên server:
```
git init
git add .
git commit —am 'chatbot'
heroku create
git push heroku master
```
Sau khi chạy thành công thì sẽ nhận được 1 đường dẫn tới trang web của bạn.
Chúng ta sẽ dùng đường dẫn này để thiết lập cho Webhooks ở phần tiếp theo.
####2. Connect app to Facebook

Đăng nhập vào [FacebookforDeveloper](https://developers.facebook.com/) sau đó vào ứng dụng của tôi và tạo ứng dụng mới.

Trong phần sản phẩm bạn thêm vào 2 mục là:
```
Webhooks
Messenger
```
Under Token Generation, select App's Name page to generate the page access token. Take note the generated token, we will be using this information when we setup the Heroku app.

Khi đó hãy chạy dòng lệnh sau:
```
heroku config:add PAGE_ACCESS_TOKEN=your_page_token_here
heroku config:add VERIFY_TOKEN=your_token
```
* You can verify the setting in Heroku dashboard Settings > Config Vars.

Setting up the Webhook
Bạn cần nhập lại đường dẫn của web app ở trên và mã xác nhận (`VERIFY_TOKEN=your_token`, ở đây mã xác nhận là `your_token`).
Sau đó hãy chọn lấy các mục thuộc tính mô tả sau:
```
messages
messages_deliveries
messaging_postbacks
```
Các bạn có thể test app của mình trên Facebook rồi đó.
***
#### Nếu app của bạn là doanh nghiệp thì hãy xác minh doanh nghiệp rồi hãy thử nghiệm trên Facebook nhé.


### Update version

Chạy file `update.py` để update dữ liệu và mô hình.

Các file ``intents.json`` và ``H3D.h5`` sẽ được tạo mới ở thư mục update. Hãy sao chép và thay thế ở trong thư mục `app`.
Sau đó chạy lại các lệnh sau:
```
git add .
git commit —am 'chatbot'
git push heroku master
```
