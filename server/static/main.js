// $('.login1').submit(function( event ) {
//     event.preventDefault();
    
//     //$(this).append($(this).serialize());
//     x = $(this).serializeArray();

//     console.log(x[0].value)  //--> email value
//     console.log(x[1].value) // --> password value


//     $.ajax({
//         type: "POST",
//         url: "/login",
//         data: $(this).serialize(),
//         success: function() {
//             console.log("Success ")
//             window.location.href = '/home'
//         },
//         error : function(){
//             console.log("Error")

//         }
//     })

//     // alert("Hello");
// });

// $('.signup1').submit(function( event ) {
//     event.preventDefault();
    
//     // x = $(this).serializeArray();
//     // console.log(x[0].value)  //--> email value
//     // console.log(x[1].value) // --> password value
//     // console.log(x[2].value) // --> password value
//     // alert("Hello");
//     // alert("HEllo");
//     // if(x[1].value == x[2].value){
//         $.ajax({
//             type : "POST",
//             url : "/signup",
//             data: $(this).serialize(),
//             success: function(resp) {
//                 if (resp.message == "Already Exists"){
//                     $('#err').html("<i>Email Already Registred ...</i>")
//                 }
//                 if (resp.message == "continue"){
//                     console.log(resp.email);
//                     window.location.href = '/details'
//                     console.log(resp.password);
//                     $('.signup1').inputValues({'email':resp.email}  );
//                     alert("Hello")
//                 }
//                 console.log("Data Sent");
//             },
//             error : function(){

//                 console.log("Error");
//             }
//         })
//     // }
//     // else{
//     //     $('#err').text('Password Not Match')
//     // }
//     // alert("Hello")
// });