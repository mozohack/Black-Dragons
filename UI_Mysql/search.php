<!DOCTYPE html>
<html>  
<head>  
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.3.0/jquery.min.js"></script> 
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">

    <link rel="stylesheet" type="text/css" href="main.css">

    
        <title>STYLE</title> 
 
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
</head>
<body>
<title>SEARCH PAGE</title>  
</head>  



<body>  

    <header class="site-header">
      <nav class="navbar navbar-expand-md navbar-dark bg-dark fixed-top sidebarNavigation" data-sidebarClass="navbar-dark bg-dark">
        <div class="container">
          <a class="navbar-brand mr-4" href="home.php">BLACK DRAGONS</a>
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarToggle" aria-controls="navbarToggle" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarToggle">
            <div class="navbar-nav mr-auto">
              <a class="nav-item nav-link" href="home.php">Home</a>
              <a class="nav-item nav-link" href="about.php">About</a>
            </div>
            <!-- Navbar Right Side -->
            <div class="navbar-nav">
              <!--<p class="nav-item nav-link" > <?php echo $_SESSION['username'] ;?> </p> -->
              <a class="nav-item nav-link" href="login.php?action=logout">Log out</a>
            </div>
          </div>
        </div>
      </nav>

    </header>
<main role="main" class="container">
      <div class="row">
        <div class="col-md-4"> 
<div class="content-section" id="content">
    
<?php

$np = $_GET['var'];
$con = mysqli_connect('localhost','root','','placemain');
if (!$con) {
    die('Could not connect: ' . mysqli_error($con));
}

//mysqli_select_db($con,"ajax_demo");
$sql="SELECT * FROM details WHERE No_Plate='$np' ";
$result = mysqli_query($con,$sql);

echo "<table>";
echo "<tr>";

while($row = mysqli_fetch_array($result)) {

	echo "<tr>";
    echo "<th>FIRST NAME </th><td>" . $row['First_NAME'] . "</td></tr>";
    echo "<tr><th>NUMBER PLATE </th><td>" . $row['No_Plate'] . "</td></tr>";
    echo "<tr><th>Vehicle_type </th><td>" . $row['Vehicle_type'] . "</td></tr>";
    echo "<tr><th>Place </th><td>" . $row['Location'] . "</td></tr>";
    echo "<tr><th>Time  Stamp </th><td>" . $row['Time_stamp'] . "</td></tr>";
    echo "</tr>";

   
}
echo "</table>";
mysqli_close($con);
?>
</div>
</div>
<div class="col-md-8"> 

	
	<div class="content-section" id="googleMap" >

<iframe src="https://www.google.com/maps/d/embed?mid=1QrZ2nlHiC8cCt6WDd8FeH1ThG8rHlQCj" width="640" height="480"></iframe></div>
</div>
</div>



</main>
</body>
</html>