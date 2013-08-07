$(document).ready(function(){
                $('#submit').click(function() {
                  var selected_users = $('input[type=checkbox]:checked').map(function(_, el) {
                    return $(el).val();
                    }).get();
                    if (selected_users !== null)
                    {
                      alert("Select Users");     // works fine  
                    }
                    
                    $.post("get_data/",{users:selected_users});   // not able to post
                });    


         })