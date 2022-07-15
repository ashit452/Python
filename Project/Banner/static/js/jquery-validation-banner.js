$(function(){
    
    $("#addbanner").validate({
      
      rules : {
        entitle : "required",
        cntitle : "required",
        encontent : "required",
        cncontent : "required",
        bannergroup : "required",
        order : "required",
        status : "required",
        'bannerimage[]' : "required",
        'url[]' : {
          required : true,
          urlcheck : true,
          },
        
      },
        messages : {
          entitle : "Please Enter Title",
          cntitle : "Please Enter Title",
          encontent : "Please Enter Content",
          cncontent : "Please Enter Content",
        bannergroup : "Please Choose Banner Group",
        order : "Please Enter Sorting order", 
        status : "Please Choose Status",  
        'bannerimage[]' : "Please Choose an Image",
        'url[]' : {
          required : "Please Enter URL",
          urlcheck : "Please Enter Correct URL",
          },
        
        
    },
   
    
    
      
    });
    $('[id^=url]').each(function () {
      $(this).rules('add', {
          required: true,
          urlcheck: true
      });
      $(this).messages('add', {
          required: "Please enter URL",
          urlcheck: "Please Enter Correct URL"
      });
    });
    $('.tabs div div input[type="text"]').each(function () {
        $(this).rules('add', {
            required: true
        });
        $(this).messages('add', {
            required: "Please enter Name"
        });
      });
//     var address = $('input[name^="address"]');

// address.filter('input[name$="[name]"]').each(function() {
//     $(this).rules("add", {
//         required: true,
//         messages: {
//             required: "Name is Mandatory"
//         }
//     });
// });
    
$("#updatebanner").validate({
      
  rules : {
    bannergroup : "required",
    order : "required",
    status : "required",
    
    'url[]' : {
      required : true,
      urlcheck : true,
      },
    
  },
    messages : {
    bannergroup : "Please Choose Banner Group",
    order : "Please Enter Sorting order", 
    status : "Please Choose Status",  
    
    'url[]' : {
      required : "Please Enter URL",
      urlcheck : "Please Enter Correct URL",
      },
    
    
},



  
});
    $.validator.addMethod("urlcheck",
        function(value, element) {
            return /[Hh][Tt][Tt][Pp][Ss]?:\/\/(?:(?:[a-zA-Z\u00a1-\uffff0-9]+-?)*[a-zA-Z\u00a1-\uffff0-9]+)(?:\.(?:[a-zA-Z\u00a1-\uffff0-9]+-?)*[a-zA-Z\u00a1-\uffff0-9]+)*(?:\.(?:[a-zA-Z\u00a1-\uffff]{2,}))(?::\d{2,5})?(?:\/[^\s]*)?"/.test(value);
    });
    

    

    });
