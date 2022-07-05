$(function(){
    
    $("#addcustomerform").validate({
      
      rules : {
        firstName : "required",
        lastName : "required",
        profile : "required",
        email : {
           required : true,
           emailcheck : true
        },
        mobile: {
           required : true,
           minlength:10,
           maxlength: 10
        },
        password : {
            required : true,
            pwcheck : true,
            minlength : 8
        },
        confirmpassword : {
           required : true,
           equalTo : "#password" 
        },
      },
        messages : {
        firstName : "Please enter First Name",
        lastName : "Please enter Last Name", 
        profile : "Please choose any image for profile",  
        email:{
            required:"Please enter email",
            emailcheck: "Please enter valid email"
            
        },
        
        mobile: {
           required : "Please enter mobile no.",
           minlength: "Length of mobile no. should be 10",
           maxlength: "Length of mobile no. should be 10"
        },
        password : {
            required : "Please enter a password",
            pwcheck : "please enter strong password(1 Uppercase, 1 Lowercase, 1 Symbol, 1 Number) with minimum 8 latters",
            minlength : "please enter strong password(1 Uppercase, 1 Lowercase, 1 Symbol, 1 Number) with minimum 8 latters",
        },
        confirmPassword : {
            required : "Please enter a password",
            equalTo : "Please enter the same password "
        },
        
        
    }

    
      
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
            firstName : "required",
            lastName : "required",
            email : {
               required : true,
               emailcheck : true
            },
            mobile: {
               required : true,
               minlength:10,
               maxlength: 10
            },
            // password : {
            //     pwcheck : true,
            //     minlength : 8
            // },
            // confirmpassword : {
            //    equalTo : "#password" 
            // },
          },
            messages : {
            firstName : "Please enter First Name",
            lastName : "Please enter Last Name", 
            email:{
                required:"Please enter email",
                emailcheck: "Please enter valid email"
                
            },
            
            mobile: {
               required : "Please enter mobile no.",
               minlength: "Length of mobile no. should be 10",
               maxlength: "Length of mobile no. should be 10"
            },
            // password : {
            //     pwcheck : "please enter strong password(1 Uppercase, 1 Lowercase, 1 Symbol, 1 Number) with minimum 8 latters",
            //     minlength : "please enter strong password(1 Uppercase, 1 Lowercase, 1 Symbol, 1 Number) with minimum 8 latters",
            // },
            // confirmPassword : {
            //     equalTo : "Please enter the same password"
            // },
            
            
        }
    
    })

    $.validator.addMethod("pwcheck",
        function(value, element) {
            return /(?=^.{8,}$)(?=.*\d)(?=.*[!@#$%^&*]+)(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$/.test(value);
    });
    $.validator.addMethod("emailcheck",
        function(value, element) {
            return /^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$/.test(value);
    });

    

    });
