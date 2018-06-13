var data = "testD"
var d = document.getElementById('date');
var createView = document.getElementById('createView');
var message = document.getElementById("message");
createView.setAttribute("disabled", "disabled")
/*var getData = function(){
    $.ajax({
	url: "/d3_helper",
	type: "GET",
	data: {},
	success: function(d){
	    console.log(d)
	    data = JSON.parse(d.replace(/'/g, '"').replace(/u"/g, '"'));
	}
    });
};

getData()
*/

var outfitHistory = function(){
    $.ajax({
	url: "/outHist",
	type: "GET",
	data: {},
	success: function(d){
	    data = JSON.parse(d.replace(/'/g, '"').replace(/u"/g, '"'));
	    //console.log("data: " + data)
	}
    });
};

//console.log("data " + data);
//outfitHistory()
//console.log("data " + data);
var month_year = document.getElementById("label");

var addEventToDate = function(){
    var date = document.getElementsByClassName("d");
    console.log(date);
    //console.log("Got new dates")
    for (i = 0; i < date.length; i++) {
	//console.log(date[i].innerHTML);
	//console.log(date[i]);
	date[i].addEventListener("click", getDate);
    }
}

var getDate = function(e){
    outfitHistory();
    console.log(data);
    createView.removeAttribute("disabled");
    //console.log(this.innerHTML);
    //console.log(month_year.innerHTML);
    var day = String(this.innerHTML);
    var monthyear = month_year.innerHTML;
    var date = day.concat(monthyear);
    console.log(date);
    dateSplit = date.split(" ");
    //console.log(dateSplit);
    d.innerHTML = date;
    keys = Object.keys(data);
    for (var i = 0; i < keys.length; i++) {
	key = keys[i].split("-");
	//console.log(key);
	if ((key[0] == dateSplit[2]) && (key[2] == dateSplit[0])) {
	    message.innerHTML = "You Already Have An Outfit For";
	    createView.innerHTML = "View Outfit";
	    return date;
	    
	}
    }
    createView.innerHTML = "Create Outfit";
    message.innerHTML = "Create An Outfit For";
    return date;
}

var CALENDAR = function () {
    var wrap, label, 
	months = ["January", "February", "March", "April", "May", "June", "July","August", "September", "October", "November", "December"];
    function init(newWrap) {
	wrap  = $(newWrap || "#cal");
	label = wrap.find("#label");
	
	wrap.find("#prev").bind("click.calender", function () { switchMonth(false); });
	wrap.find("#next").bind("click.calender", function () { switchMonth(true); });
	label.bind("click.calendar", function () { switchMonth(null, new Date().getMonth(), new Date().getFullYear() ); });
    }
    
    function switchMonth(next, month, year) {
	var curr = label.text().trim().split(" "), calendar, tempYear = parseInt(curr[1], 10);
	month = month || ((next) ? ((curr[0] === "December") ? 0 : months.indexOf(curr[0]) + 1) : ( (curr[0] === "January") ? 11 : months.indexOf(curr[0]) - 1) );
	year  = year  || ((next && month === 0) ? tempYear + 1 : (!next && month === 11) ? tempYear -1 : tempYear);
	
	console.profile("createCal");
	calendar = createCal(year, month);
	console.profileEnd("createCal");
	
	$("#cal-frame", wrap)
	    .find(".curr")
	    .removeClass("curr")
	    .addClass("temp")
	    .end()
	    .prepend(calendar.calendar())
	    .find(".temp")
	    .fadeOut("slow", function () { $(this).remove(); });
	label.text(calendar.label);
	//muy importante
	addEventToDate();
	
    }

    
    function createCal(year, month) {
	var day = 1, i, j, haveDays = true, 
	    startDay = new Date(year, month, day).getDay(),
	    daysInMonth = [31, (((year%4===0)&&(year%100!==0))||(year%400===0)) ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ],
	    calendar = [];
	if (createCal.cache[year]) {
	    if (createCal.cache[year][month]) {
		return createCal.cache[year][month];
	    }
	} else {
	    createCal.cache[year] = {};
	}
	i = 0;
	while(haveDays) {
	    calendar[i] = [];
	    for (j = 0; j < 7; j++) {
		if (i === 0) {
		    if (j === startDay) {
			/*if (day in data) {
			    console.log(day);
			    console.log(data);
			    calendar[i][j] = day++ + "<br>Hi: " + data[day]["min"];
			}
			else {
			    calendar[i][j] = day++;
			    }*/
			calendar[i][j] = day++;
			startDay++;
		    }
		} else if ( day <= daysInMonth[month]) {
		   /* if (day in data) {
			console.log(day);
			console.log(data);
			calendar[i][j] = day++ + "<br>Hi: " + data[day]["min"];
		    }
		    else {
			calendar[i][j] = day++;
			}*/
		    calendar[i][j] = day++;
		} else {
		    calendar[i][j] = "";
		    haveDays = false;
		}

		if (day > daysInMonth[month]) {
		    addEventToDate();
		    haveDays = false;
		}
	    }
	    i++;
	}	
	
	if (calendar[5]) {
	    for (i = 0; i < calendar[5].length; i++) {
		if (calendar[5][i] !== "") {
		    calendar[4][i] = "<span>" + calendar[4][i] +  "</span><span>" + calendar[5][i] + "</span>";
		}
	    }
	    calendar = calendar.slice(0, 5);
	}
	
	for (i = 0; i < calendar.length; i++) {
	    calendar[i] = "<tr><td class=d>" + calendar[i].join("</td><td class=d>") + "</td></tr>";
	}

	calendar = $("<table>" + calendar.join("") + "</table").addClass("curr");
	addEventToDate();
	$("td:empty", calendar).addClass("nil");
	if (month === new Date().getMonth()) {
	    $('td', calendar).filter(function () { return $(this).text() === new Date().getDate().toString(); }).addClass("today");
	}

	createCal.cache[year][month] = { calendar : function () { return calendar.clone(); }, label : months[month] + " " + year };
	return createCal.cache[year][month];
    }
    createCal.cache = {};
    return {
	init : init,
	switchMonth : switchMonth,
	createCal : createCal
    };

};

addEventToDate();


