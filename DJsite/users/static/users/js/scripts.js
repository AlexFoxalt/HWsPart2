function showDiv(select){
   if(select.value==1){
    document.getElementsByClassName('hidden_label_teacher')[0].style.display="block";
    document.getElementsByClassName('hidden_label_teacher')[1].style.display="block";
    document.getElementsByClassName('hidden_label_teacher')[2].style.display="block";
    document.getElementsByClassName('hidden_label_student')[0].style.display="none";
    document.getElementsByClassName('hidden_label_student')[1].style.display="none";
    document.getElementsByClassName('hidden_label_student')[2].style.display="none";
   } if(select.value==0){
    document.getElementsByClassName('hidden_label_teacher')[0].style.display="none";
    document.getElementsByClassName('hidden_label_teacher')[1].style.display="none";
    document.getElementsByClassName('hidden_label_teacher')[2].style.display="none";
    document.getElementsByClassName('hidden_label_student')[0].style.display="block";
    document.getElementsByClassName('hidden_label_student')[1].style.display="block";
    document.getElementsByClassName('hidden_label_student')[2].style.display="block";
   }
}