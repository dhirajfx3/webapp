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
		document.getElementById("personal").style.marginTop="-8px";
		document.getElementById("personal").style.width=document.getElementById("ele2").getBoundingClientRect().width+"px";
	//	document.getElementById("sample").value=(document.getElementById("cont-flu").getBoundingClientRect().bottom-8)+"px";
	}
	else
		document.getElementById("personal").style.display="none";
}
function set_pos()
{
	document.getElementById("body_item").style.marginTop=(document.getElementById("ele2").getBoundingClientRect().bottom+8)+"px";
//	document.getElementById("sample").value=(document.getElementById("ele2").getBoundingClientRect().bottom+8)+"px";
}
function view()
{
	confirm("Sure you want too see?");
}
function validateform()
{
    a = document.forms["form1"]["p1"].value;
    b = document.forms["form1"]["p2"].value;

    if (a!=b)
    {
        alert("Passwords should match.\n");
        return false;
    }
    if (String(a).length < 8)
    {
        alert("Password should have  at least 8 characters.")
        return false;
    }
    return true;
}
$(document).ready(function(){
$(function() {
    $('#modalshow').bind('click', function() {
			$("#myModal").modal("show");
      });
	});
});