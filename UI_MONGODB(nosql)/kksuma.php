<!DOCTYPE html>
<html>
<head>
    
<style>
table {
    width: 100%;
    border-collapse: collapse;
}

table, td, th {
    border: 1px solid black;
    padding: 5px;
}

th {text-align: left;}
</style>
<script>
    var div = document.getElementById("dom-target");
    var myData = div.textContent;

    function run() {
        
        var str=document.forms["reg"]["numberplate"].value;
        window.location="map.php?var="+myData;
     
}

$(document).ready(function(){
$("input").click(function(){
        $(this).next().show();
        $(this).next().hide();
    });

});

</script>

</head>
<body>

<div id="dom-target" ">
    <?php 
      require 'C:/xampp/php/vendor/autoload.php';
    $m = new MongoDB\Client("mongodb://192.168.43.104:27017/");

    $db = $m->ajdb;
   $collection = $db->numplate;
   $cursor = $collection->find();

echo "<table>";
echo "<tr>";
echo "<th> FIRST NAME </th> <th>NUMBER PLATE </th><th>Vehicle_type </th><th>Place </th> <th>Time  Stamp</th>";
echo"</tr>";
foreach ($cursor as $row) {

    echo "<tr>";
    echo "<th>" . $row['name'] . "</th> <th>". $row['number plate'] ."</th> <th>". $row['vehicle type'] ."</th> <th>". $row['place'] ."</th> <th>". $row['Time stamp'] ."</th>";
    echo "</tr>";
   $output = $row['name'];
}
echo "</table>";
  
?>
</div>
</body>
</html>