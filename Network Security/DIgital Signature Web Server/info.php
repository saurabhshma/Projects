<!DOCTYPE html>
<head>
<title>"Student Record"</title>
<link rel="stylesheet" href="css/bootstrap.css">
<link rel="stylesheet" href="css/main.css">
</head>

<body>
<br>
<form action="info.php" method="post" enctype="multipart/form-data">
<div > <input style="height:40px;width:100px" type="submit" value="Home" name="Home" class="btn btn-lg btn-success btn-block"> </div>
</form>
<div class="container">
  <div class="row" style="margin-top:20px">
    <div class="col-xs-12 col-sm-8 col-md-6 col-sm-offset-2 col-md-offset-3">
    <form name="form_login" method="post" action="info.php" role="form">
<?php
	session_start();
	echo "<h2 align=".'center'."> ".$_SESSION['enrolment']."</h2>";
	$enrol = $_SESSION['enrolment'];
?>
    <hr class="colorgraph">
<?php	
	Include('connect.php');
	$sql1= "select * from sem1 where enrolment= '".$enrol."'" ;
	$result=mysql_query($sql1)
	or exit("Sql Error".mysql_error());
	
	$num_rows=mysql_num_rows($result);
	if($num_rows>0)
	{
		$sql2= "select * from sem2 where enrolment= '".$enrol."'" ;
		$result2=mysql_query($sql2)
			or exit("Sql Error".mysql_error());
	
		$num_rows2=mysql_num_rows($result2);
		if($num_rows2 >0)
		{
			echo '<div class="col-xs-6 col-sm-6 col-md-6"> <input type="submit" name="gradeCard" value="Grade Card" class="btn btn-lg btn-success btn-block"> </div>';
			$sql2= "select deg from sem2dc where enrolment= '".$enrol."'" ;
			$result2=mysql_query($sql2)
			or exit("Sql Error".mysql_error());
			$obj = mysql_fetch_object($result2);

			echo '<div class="col-xs-6 col-sm-6 col-md-6"> <input type="submit" name="dc" value="Degree Certificate" class="btn btn-lg btn-primary btn-block"> </div>';
			echo '<br><br><br>';




  
		}
		else
		{
			echo '<div class="col-xs-6 col-sm-6 col-md-12"> <input type="submit" name="gradeCard1" value="Grade Card" class="btn btn-lg btn-success btn-block"> </div>';
		}
	}
	else
	{
		echo "No data available";
	}

	if (isset($_REQUEST['gradeCard1'])) //here give the name of your button on which you would like    //to perform action.
	{
		echo '<br><br><br>';
		echo '<div class="col-xs-6 col-sm-6 col-md-12"> <input type="submit" name="sem1" value="Semster 1" class="btn btn-lg btn-success btn-block"> </div>';
	}
	if (isset($_REQUEST['gradeCard'])) //here give the name of your button on which you would like    //to perform action.
	{
		echo '<br><br><br>';
		echo '<div class="col-xs-6 col-sm-6 col-md-6"> <input type="submit" name="sem1" value="Semster 1" class="btn btn-lg btn-success btn-block"> </div>';
		echo '<div class="col-xs-6 col-sm-6 col-md-6"> <input type="submit" name="sem2" value="Semster 2" class="btn btn-lg btn-success btn-block"> </div>';
	}

	

	if (isset($_REQUEST['sem1']))
	{
		$_SESSION['enrolment'] = $enrol;
		header("location:gridsem1.php");
	}

	if (isset($_REQUEST['sem2']))
	{
		$_SESSION['enrolment'] = $enrol;
		header("location:gridsem2.php");
	}

	if (isset($_REQUEST['dc'])) //here give the name of your button on which you would like    //to perform action.
  {
    system('python signing.py '.$obj->deg.'');
    header("location:signed.pdf");
    //sleep(50);
    //unlink('signed.pdf');
  }
	
?>
 	</form>
    </div>
  </div>
</div>

<br><br>

<?php
if(isset($_REQUEST['Home']))
{
header('location:login.php');
  }
?>

</body>


</html>
