function showDiv(select){
   if(select.value=='Teacher'){
    document.getElementsByClassName('hidden_label_teacher')[0].style.display="block";
    document.getElementsByClassName('hidden_label_teacher')[1].style.display="block";
    document.getElementsByClassName('hidden_label_teacher')[2].style.display="block";
    document.getElementsByClassName('hidden_label_student')[0].style.display="none";
    document.getElementsByClassName('hidden_label_student')[1].style.display="none";
    document.getElementsByClassName('hidden_label_student')[2].style.display="none";
    document.getElementsByClassName('hidden_label_student')[3].style.display="none";
   } if(select.value=='Student'){
    document.getElementsByClassName('hidden_label_teacher')[0].style.display="none";
    document.getElementsByClassName('hidden_label_teacher')[1].style.display="none";
    document.getElementsByClassName('hidden_label_teacher')[2].style.display="none";
    document.getElementsByClassName('hidden_label_student')[0].style.display="block";
    document.getElementsByClassName('hidden_label_student')[1].style.display="block";
    document.getElementsByClassName('hidden_label_student')[2].style.display="block";
    document.getElementsByClassName('hidden_label_student')[3].style.display="block";
   }
}

setTimeout(function() {
    $('#successMessage').fadeOut('slow');
}, 3000); // <-- time in milliseconds