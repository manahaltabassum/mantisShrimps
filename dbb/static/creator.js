var slideIndex = [1,1,1];
var slideId = ["mySlides1", "mySlides2", "mySlides3"]
showSlides(1, 0);
showSlides(1, 1);
showSlides(1, 2);

var topSelect = document.getElementById("topForm");
var pantSelect = document.getElementById("pantForm");
var shoeSelect = document.getElementById("shoeForm");

function plusSlides(n, no) {
    showSlides(slideIndex[no] += n, no);
    if (no == 0) {
	topSelect.value = (parseInt(topSelect.value) + n).toString();
    }
    if (no == 1) {
	pantSelect.value = (parseInt(pantSelect.value) + n).toString();
    }
    if (no == 2) {
	shoeSelect.value = (parseInt(shoeSelect.value) + n).toString();;
    }
}

function showSlides(n, no) {
    var i;
    var x = document.getElementsByClassName(slideId[no]);
    if (n > x.length) {slideIndex[no] = 1}    
    if (n < 1) {slideIndex[no] = x.length}
    for (i = 0; i < x.length; i++) {
	x[i].style.display = "none";  
    }
    x[slideIndex[no]-1].style.display = "block";  
}
