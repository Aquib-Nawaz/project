function myFunction(id) {
    var id1 = ["add_ta", "add_student", "remove_student"];
    var elem = [];
    for (e of id1)
        document.getElementById(e).style.display = "none"; 
    var x = document.getElementById(id);   
    x.style.display = "block";
    
  }