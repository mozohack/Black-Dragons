<html>  
<head>  
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.3.0/jquery.min.js"></script> 
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link rel="shortcut icon" type="image/png" href="/static/favicon.ico"/>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">

    <link rel="stylesheet" type="text/css" href="main.css">

    
        <title>Student edit</title> 
<script>  
setInterval(  
function()  
{  
$('#content').load('kksuma.php');  
}, 1000);  
</script>  
<style>  
 
</style>  
<title>Auto Load Page in Div using Jquery</title>  
</head>  



<body>  

    <header class="site-header">
      <nav class="navbar navbar-expand-md navbar-dark bg-dark fixed-top sidebarNavigation" data-sidebarClass="navbar-dark bg-dark">
        <div class="container">
           <a class="navbar-brand mr-4" href="home.php">ROAD'S EYE</a>
        <button class="navbar-toggler leftNavbarToggler" type="button" data-toggle="collapse" data-target="#navbarToggle" aria-controls="navbarToggle" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
          <div class="collapse navbar-collapse" id="navbarToggle">
          <div class="navbar-nav mr-auto">
            <a class="nav-item nav-link" href="sumatry.php"><span class="glyphicon glyphicon-user" aria-hidden="true"></span>&nbspTraveller</a>
            <a class="nav-item nav-link" href="track.php"><span class="glyphicon glyphicon-screenshot" aria-hidden="true"></span>&nbspTrack</a>
          </div>
            <!-- Navbar Right Side -->
           <div class="navbar-nav navbar-right">
            <form class="navbar-form navbar-left" role="search" name="reg" method="POST" >
                <div class="form-group">
                    <input type="text" class="form-control" id="numberplate"name="numberplate" value="">
                </div>
                <button  type="button" class="btn btn-default" onclick="run()">Search</button>
            
            
          </div>
        </div>
      </div>
    </nav>

  </header>
<main role="main" class="container">
      <div class="row">
        <div class="col-md-8"> 
<div class="content-section" id="content"> Please wait .. </div>  
</div></div></main> 


</body>  
<html> 