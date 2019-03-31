
<!DOCTYPE html>
<html>
<head>

</head>
  <body>
    
    <?php 
      


$con = mysqli_connect('localhost','root','','placemain');
if (!$con) {
    die('Could not connect: ' . mysqli_error($con));
}

//mysqli_select_db($con,"ajax_demo");
$sql="SELECT * FROM helmet ";
$result = mysqli_query($con,$sql);


while($row = mysqli_fetch_array($result)) {

  echo $row['image'] ;
   $kk= $row['image'] ;

    echo "<img src=".$kk.">";
}
  
mysqli_close($con);
?>
  </body>
  </html>