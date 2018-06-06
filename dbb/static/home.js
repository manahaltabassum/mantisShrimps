var type = "top";
var data;

var getData = function() {
    $.ajax({
	url: "/getClothes",
	type: "GET",
	data : {},
	success: function(d){
	    console.log(d);
	    data = JSON.parse( d.replace(/'/g, '"').replace(/u"/g, '"'));
	}
    })
};

getData();
	
var update = function() {
    if( type == document.getElementById("type").value ){}
    else{
	type = document.getElementById("type").value;
	var clothes = data[type];
	for (i = 0; i < clothes.length; i++){
	    if (i % 3 == 0){
		// add <br> in the html code
	    }
	    //putting clothes in a list in html
	}
    }

};
