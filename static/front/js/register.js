var RegisterHandler = function (){

}

RegisterHandler.prototype.listenSendCaptchaEvent = function (){
  var callback = function (event){
    // 原生的JS對象：this => jQuery對象
    var $this = $(this);
    // 阻止默認的點擊事件
    event.preventDefault();
    var email = $("input[name='email']").val();
    var reg = /^\w+((.\w+)|(-\w+))@[A-Za-z0-9]+((.|-)[A-Za-z0-9]+).[A-Za-z0-9]+$/;
    if(!email || !reg.test(email)){
      alert("請輸入正確格式的email！");
      return;
    }
    petajax.get({
      url: "/email/captcha?email=" + email,
      success: function (result){
        if(result['code'] == 200){
          console.log("Email發送成功！");
          // 取消按鈕的點擊事件
          $this.off("click");
          // 添加禁用狀態
          $this.attr("disabled", "disabled");
          // 開始倒計時
          var countdown = 15;
          var interval = setInterval(function (){
            if(countdown > 0){
              $this.text(countdown);
            }else{
              $this.text("發送Email驗證碼");
              $this.attr("disabled", false);
              $this.on("click", callback);
              // 清理定時器
              clearInterval(interval);
            }
            countdown--;
          }, 1000);
        }else{
          var message = result['message'];
          alert(message);
        }
      }
    })
  }
  $("#email-captcha-btn").on("click", callback);
}

RegisterHandler.prototype.listenGraphCaptchaEvent = function (){
  $("#captcha-img").on("click", function (){
    console.log("點擊了圖形驗證碼");
    var $this = $(this);
//    獲取src標籤
    var src = $this.attr("src");
    // /graph/captcha
    // /graph/captcha?sign=Math.random()
    // 防止舊的瀏覽器在兩次url相同的情况下不會重新發送請求，導致圖片驗證碼不會更新
    let new_src = param.setParam(src, "sign", Math.random())
//    獲取src標籤設置成新的src
    $this.attr("src",new_src);
  });
}

RegisterHandler.prototype.listenSubmitEvent = function (){
  $("#submit-btn").on("click", function (event){
    event.preventDefault();
    var email = $("input[name='email']").val();
    var email_captcha = $("input[name='email-captcha']").val();
    var username = $("input[name='username']").val();
    var password = $("input[name='password']").val();
    var repeat_password = $("input[name='repeat-password']").val();
    var graph_captcha = $("input[name='graph-captcha']").val();

    // 如果是商业项目，一定要先验证这些数据是否正确
    petajax.post({
      url: "/register",
      data: {
        "email": email,
        "email_captcha": email_captcha,
        "username": username,
        password, // "password": password
        repeat_password,
        graph_captcha
      },
      success: function (result){
        if(result['code'] == 200){
          window.location = "/login";
        }else{
          alert(result['message']);
        }
      }
    })
  });
}

RegisterHandler.prototype.run = function (){
  this.listenSendCaptchaEvent();
  this.listenGraphCaptchaEvent();
  this.listenSubmitEvent();
}

// $(function(){})
//全部網頁加載完成後再執行function
$(function (){
  var handler = new RegisterHandler();
  handler.run();
})
