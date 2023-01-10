# 齊助浪寶討論專區(DEMO)

## 齊助浪寶首頁(Click to learn more): [![](https://img.shields.io/badge/-🐾🐕🐈%20齊助浪寶no_more_stray-000)](https://github.com/Francescatai/NoMoreStray_flaskAPI.git)

### Introduction
齊助浪寶領養平台的DEMO版本，用於讓領養者及寵物領域相關專家進行交流，也可以互相討論養寵相關心得

### Project Tech Stack


| Frontend | Backend    | Database |
| -------- | --------   | -------- |
| Bootstrap|Python-Flask|MySQL|
| Jquery   |            |Redis|
| wangEditor|||

### Function Display
#### 討論專區
![](https://i.imgur.com/H4xWLrt.png)

#### 登入及註冊
註冊
* 使用celery進行非同步任務排程Email驗證碼寄送
* 藉由Redis進行Emai及圖形驗證碼緩存
![](https://i.imgur.com/lXu4QT7.png)

登入
![](https://i.imgur.com/NJBz5YX.png)

#### 討論功能
發表討論
* 內容編輯器使用wangEditor實現
![](https://i.imgur.com/rCydvjO.png)

單篇文章
![](https://i.imgur.com/1N16oei.png)


#### 用戶後台
![](https://i.imgur.com/K0h553R.png)

