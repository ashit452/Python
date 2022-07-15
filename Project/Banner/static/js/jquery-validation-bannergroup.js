$(function(){
    
    $("#addbannergroup").validate({
      
      rules : {
        enname: "required",
        cnname: "required",
        code : "required",
        order : "required",
        status : "required",
        
      },
        messages : {
            enname: "Please Enter Name",
            cnname: "Please Enter Name",
        code : "Please Enter Code",
        order : "Please Enter Sorting order", 
        status : "Please Choose Status",  
        
        
        
    }

    
      
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
    $("#updatecustomerform").validate({
        rules : {
            code : "required",
            order : "required",
            status : "required",
            
          },
            messages : {
            code : "Please Enter Code",
            order : "Please Enter Sorting order", 
            status : "Please Choose Status",  
            
            
            
        }
    })

    

    

    });
