function openNav() {
	if(document.getElementById("mySidenav").style.height == "0px")
		document.getElementById("mySidenav").style.height = "300px";
	else
		document.getElementById("mySidenav").style.height = "0";
}

/* Set the width of the side navigation to 0 */
function closeNav() {
    document.getElementById("mySidenav").style.display = "none";
}
function menu1()
{
	if(document.getElementById("personal").style.display=="none")
	{
		document.getElementById("personal").style.display="block";
		document.getElementById("personal").style.marginTop="8px";
		document.getElementById("personal").style.width=document.getElementById("ele2").getBoundingClientRect().width+"px";
	//	document.getElementById("sample").value=(document.getElementById("cont-flu").getBoundingClientRect().bottom-8)+"px";
	}
	else
		document.getElementById("personal").style.display="none";
}
function set_pos()
{
	document.getElementById("body_item").style.marginTop=(document.getElementById("cont-flu").getBoundingClientRect().bottom+8)+"px";
	//document.getElementById("sample").value=(document.getElementById("ele2").getBoundingClientRect().bottom+8)+"px";
}
function view(roll)
{
	document.getElementById("search_results").outerHTML="";
}
function query()
{
	var g=document.getElementById("inp1").value;
	var h=document.getElementById("filter").value;
	if(!validate(h,g))
	{
		alert("Invalid input for " + h);
		return;
	}
	
	confirm(String("Search by "+ String(h) + "  :  " +String(g)));
	del_rev();
}
function validate(a,b)
{
	if(a=="Roll number" && isNaN(b))
	{
		return false;
	}
	if(a=="Year" && (b==NaN || b>2017 && b<1900))
		return false;		
	return true;
}
function create_students()
{
	
}
function del()
{
	document.getElementById("inp1").disabled=true;
	document.getElementById("filter").disabled=true;
	document.getElementById("b1").disabled=true;
}
function del_rev()
{
	document.getElementById("inp1").disabled=false;
	document.getElementById("filter").disabled=false;
	document.getElementById("b1").disabled=false;
}
function fetch_option(n)
{
	confirm(n);
}
function modal1()
{
	document.getElementById("modal_test").modal-"show";
}
$(document).ready(function()
{
	$(".trb").click(function() 
	{
		$("#roll").html($(this).attr("id"));
		$("#modal_test").modal("show");
	});
	$("#view").click(function() 
	{
		$("#modal_test").modal("hide");
		view($("#roll").html());
	});
});