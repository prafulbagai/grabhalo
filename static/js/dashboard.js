$(function(){
    
  $('#logout_li').click(function(){
    $("#home_li").removeClass("active");
    $("#chat_li").removeClass("active");
    $("#logout_li").addClass("active");
  });



  $('#submit').click(function() {
    
    var selected_users = $('input[type=checkbox]:checked').map(function(_, el) {
      return $(el).val();
    }).get();
    var message = $("#message").val();

    if (selected_users.length == 0)
    {
      $("#alert").addClass("alert-red");
      $("#alert").html("Please select atleast 1 user.")
      
      setTimeout(function() {
        $("#alert").removeClass( "alert-red", 1500 );
        $("#alert").html("");
      }, 1000 );
      return false;
    }

    if (message == "") {
      $("#alert").addClass("alert-red");
      $("#alert").html("Enter some text.")
      setTimeout(function() {
        $("#alert").removeClass( "alert-red", 1500 );
        $("#alert").html("");
      }, 1000 );
      return false; 
    };

    $.ajax({
      type: "POST",
      url : "/dashboard/",
      data : {"selected_users" : selected_users,"message":message},
      success : function(result){
        $("#alert").html("Message sent.")
        $("#alert").addClass("alert-green");
        setTimeout(function() {
          $("#alert").removeClass( "alert-green", 1500 );
          $("#alert").html("");
        }, 1000 );
      }

    });
  });    
});

$(function(){
  $('#inbox').on('click', 'li', function(){

    $("#inbox li").removeClass("active");
    $(this).addClass("active");

    var selected_message_id = $(this).attr('id');
    var chat_html = ""
    $.ajax({
      type: "POST",
      dataType : "json",
      url : "/dashboard/chats/",
      data : {"selected_message_id" : selected_message_id},
      success : function(result){
        selected_chat_id = selected_message_id;
        for ( var time in result){
          for (var name in result[time]){
            chat_html += "<b style='color:#3a87ad'>" + name + ": </b> " + result[time][name] + "<br><small><b>" + time + "</b></small><br>";
          }
        }

        $("#selected_chat_div").html(chat_html);
      }
    });
  });
});



$(function(){
    
  $('#chat_submit').click(function() {
    
    var message = $("#chat_message").val();
    var selected_chat = selected_chat_id;

    if (selected_chat == "")
    {
      $("#alert").addClass("alert-red");
      $("#alert").html("Please select a chat first.")
      
      setTimeout(function() {
        $("#alert").removeClass( "alert-red", 1500 );
        $("#alert").html("");
      }, 1000 );
      return false;
    }

    if (message == "") {
      $("#alert").addClass("alert-red");
      $("#alert").html("Enter some text.")
      setTimeout(function() {
        $("#alert").removeClass( "alert-red", 1500 );
        $("#alert").html("");
      }, 1000 );
      return false; 
    };

    $.ajax({
      type: "POST",
      url : "/dashboard/chats/",
      data : {"save_chat" : "save_chat","selected_chat_id" : selected_chat_id,"message":message},
      success : function(result){
        $("#alert").html("Message sent.")
        $("#alert").addClass("alert-green");
        setTimeout(function() {
          $("#alert").removeClass( "alert-green", 1500 );
          $("#alert").html("");
        }, 1000 );
        var chat_html = "<b style='color:#3a87ad'>" + 111 + ": </b> " + message + "<br><small><b>" + 123 + "</b></small>";
        $("#selected_chat_div").append(chat_html)

      }

    });
  });    
});
