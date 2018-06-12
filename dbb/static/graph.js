var stats = [12, 5, 2];
var type = ['Tops','Bottoms','Shoes']

var chart = d3.select(".chart");
var bar = chart.selectAll("div");
var barUpdate = bar.data(stats);
var barEnter = barUpdate.enter().append("div");

barEnter.transition().duration(2000).style("width", function(d){
    return d * 10 + "px";});
barEnter.data(type);
barEnter.text(function(d) {return d;});
