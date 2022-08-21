var SettingHandler = function (){}

SettingHandler.prototype.listenAvatarUploadEvent = function (){
  $("#avatar-input").on("change", function (){
    var image = this.files[0];
    var formData = new FormData();
//    image:二進制圖片
    formData.append("image", image);
    petajax.post({
      url: "/avatar/upload",
      data: formData,
      // 如果使用jQuery上傳，需要指定以下參數
      processData: false,
      contentType: false,
      success: function (result){
        if(result['code'] == 200){
          // result = {"code": 200, "data": {"avatar": "/xxx"}}
          var avatar = result['data']['avatar'];
          var avatar_url = "/media/avatar/" + avatar;
          $("#avatar-img").attr("src", avatar_url);
        }
      }
    })
  });
}

SettingHandler.prototype.listenSubmitEvent = function (){
  $("#submit-btn").on("click", function (event){
    event.preventDefault();
    var signature = $("#signagure-input").val();
    if(!signature){
      alert("成功送出");
      return;
    }
    if(signature && (signature.length > 50)){
      alert("個性簽名最多50字");
      return;
    }
    petajax.post({
      url: "/profile/edit",
      data: {signature},
      success: function (result){
        if(result['code'] == 200){
          alert("成功送出");
        }else{
          alert(result['message'])
        }
      }
    })
  });
}

SettingHandler.prototype.run = function (){
  this.listenAvatarUploadEvent();
  this.listenSubmitEvent();
}

$(function (){
  var handler = new SettingHandler();
  handler.run();
})