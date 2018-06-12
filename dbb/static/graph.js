var getData = function(){
    $.ajax({
	url: "/d3_helper",
	type: "GET",
	data: {},
	success: function(d){
	    var stats = JSON.parse(d);
	    console.log(stats);
	    var type = ['Tops','Bottoms','Shoes']
	    var info = new Array(stats[0] + " " + type[0],
				 stats[1] + " " + type[1],
				 stats[2] + " " + type[2]);
	    console.log(info);
	    var chart = d3.select(".chart");
	    var bar = chart.selectAll("div");
	    var barUpdate = bar.data(stats);
	    var barEnter = barUpdate.enter().append("div");

	    barEnter.transition().duration(2000).style("width", function(d){
		return d * 50 + "px";});
	    barEnter.data(info);
	    barEnter.text(function(d) {return d;});

	}
    });
};

getData()
