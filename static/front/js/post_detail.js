$(function (){
  // code高亮
  hljs.highlightAll();

  $("#comment-btn").on("click", function (event){
    event.preventDefault();
    var $this = $(this);

    var user_id = $this.attr("data-user-id");
    if(!user_id || user_id == ""){
      window.location = "/login";
      return;
    }

    var content = $("#comment-textarea").val();
    var post_id = $this.attr("data-post-id");

    petajax.post({
      url: "/comment",
      data: {content, post_id},
      success: function (result){
        if(result['code'] == 200){
          window.location.reload();
        }else{
          alert(result['message']);
        }
      }
    })
  });
});