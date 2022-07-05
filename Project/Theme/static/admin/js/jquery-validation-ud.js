$().ready(function(){
        $("#addcustomerform").validate({
          ignore: [],
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
            
            
        }
          }
        });
        $.validator.addMethod("pwcheck",
            function(value, element) {
                return /(?=^.{8,}$)(?=.*\d)(?=.*[!@#$%^&*]+)(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$/.test(value);
        });
        $.validator.addMethod("emailcheck",
            function(value, element) {
                return /^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$/.test(value);
        });

        

        });