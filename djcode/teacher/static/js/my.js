var questionNum = 0;

function disableCheckBox() {
var obj=document.getElementsByTagName("input") 
for(var i=0;i<obj.length;i++) 
{
if ( !obj[i].checked && obj[i].type=="checkbox"){
obj[i].disabled = true;
}
} 
} 
function ableCheckBox() { 
var obj=document.getElementsByTagName("input") 
for(var i=0;i<obj.length;i++) 
obj[i].disabled = false; 
} 

function check() 
{ 
var obj=document.getElementsByTagName("input") 
var sun=0; 

for(var i=0;i<obj.length;i++)
{ 
if(obj[i].type=="checkbox" && 
obj[i].checked) 
sun++; 

if( sun< questionNum )
{ 
ableCheckBox(); 
//break; 
} 
else if(sun == questionNum )
{ 
disableCheckBox(); 
event.srcElement.checked=true; 
break; 
} 
else if(sun > questionNum )
{ 
event.srcElement.checked=false; 
break; 
} 
} 
} 

function isenough(){
	var obj=document.getElementsByTagName("input") 
	var sun=0;
	for(var i=0;i<obj.length;i++)
	{ 
		if(obj[i].type=="checkbox" && 
		obj[i].checked) 
		sun++; 
  }
	if( sun< questionNum )
	{
		alert(questionNum + " questions need to be selected!");
        return false;

	}

}

var dataset = [];
function drawChart(dataset , Str){
        var width = 600;  
        var height = 600;  
        // var dataset = [];  
        // var num = 20;  //数组的数量  
          
        // for(var i = 0; i < num ; i++){  
             // var tempnum = Math.floor( Math.random() * 50 );   // 返回 0~49 整数  
             // dataset.push(tempnum);  
        // }  
        num=dataset.length;
        var svg = d3.select("body").append("svg")  
                                .attr("width",width)  
                                .attr("height",height);
        var xAxisScale = d3.scale.ordinal()  
                        //.domain(d3.range(dataset.length))  
                        .rangeRoundBands([0,500]);  
                              
        var yAxisScale = d3.scale.linear()  
                        .domain([0,d3.max(dataset)])  
                        .range([500,0]);  
                              
         var xAxis = d3.svg.axis()  
                         .scale(xAxisScale)  
                        .orient("bottom");  
          
        var yAxis = d3.svg.axis()  
                        .scale(yAxisScale)  
                        .orient("left");  
  
        var xScale = d3.scale.ordinal()  
                        .domain(d3.range(dataset.length))  
                        .rangeRoundBands([0,500],0.05);  
                              
        var yScale = d3.scale.linear()  
                        .domain([0,d3.max(dataset)])  
                        .range([0,500]);  
          
        svg.selectAll("rect")  
           .data(dataset)  
           .enter()  
           .append("rect")  
           .attr("x", function(d,i){  
                return 30 + xScale(i);  
           } )  
           .attr("y",function(d,i){  
                return 50 + 500 - yScale(d) ;  
           })  
           .attr("width", function(d,i){  
                return xScale.rangeBand();  
           })  
           .attr("height",yScale)  
           .attr("fill","gray");  
       svg.selectAll("text")  
            .data(dataset)  
            .enter().append("text")  
            .attr("x", function(d,i){  
                return 30 + xScale(i);  
           } )  
           .attr("y",function(d,i){  
                return 50 + 500 - yScale(d) ;  
           })  
            .attr("dx", function(d,i){  
                return xScale.rangeBand()/3;  
           })  
            .attr("dy", 15)  
            .attr("text-anchor", "begin")  
            .attr("font-size", 14)  
            .attr("fill","white")
            .text(function(d,i){  
                return d;  
            });
      svg.selectAll("text12")  
            .data(Str)  
            .enter().append("text")  
            .attr("x", function(d,i){  
                return 30 + xScale(i);  
           } )  
           .attr("y",function(d,i){  
                return 60 + 500  ;  
           })  
            .attr("dx", function(d,i){  
                return xScale.rangeBand()/3;  
           })  
            .attr("dy", 15)  
            .attr("text-anchor", "begin")  
            .attr("font-size", 14)  
            .attr("fill","black")
            .text(function(d,i){  
                return d;  
            });



        svg.append("g")  
            .attr("class","axis")  
            .attr("transform","translate(30,550)") 
            .call(xAxis);   

        svg.append("g")  
            .attr("class","axis")  
            .attr("transform","translate(30,50)")  
            .call(yAxis);   
}