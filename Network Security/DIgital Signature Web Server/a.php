<!DOCTYPE html>
<!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
<!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
<!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
<!--[if gt IE 8]><!-->
<html class="no-js">
<!--<![endif]-->
<style>
table, th, td {
    border: 1px solid black;
}
</style>
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
<title>PHP Login Form</title>
<meta name="description" content="">
<meta name="viewport" content="width=device-width">
<link rel="stylesheet" href="css/bootstrap.css">
<link rel="stylesheet" href="css/main.css">
<link rel="stylesheet" href="css/main3.css">

</head>
<!-- NAVBAR
================================================== -->

<body>
<br>
<form action="a.php" method="post" enctype="multipart/form-data">
<div > <input style="height:40px;width:100px" type="submit" value="Home" name="Home" class="btn btn-lg btn-success btn-block"> </div>
</form>
<div class="container">
  <div class="row" style="margin-top:20px">
    <div class="col-xs-12 col-sm-8 col-md-6 col-sm-offset-2 col-md-offset-3">
    <form name="form_login" method="post" action="a.php" role="form">
        <h2 align="center"><B>FACULTY VIEW</B></h2>
          <hr class="colorgraph">
  
  <table BORDER=1 WIDTH="100%">
        <tbody>
    <?php
    Include('connect.php');
   
    session_start();
    $enrol = $_SESSION['enrolment'];
    
    $sql1= "select * from record where role=0" ;
    $result=mysql_query($sql1)or exit("Sql Error".mysql_error());
    $num_rows=mysql_num_rows($result);
    
    if($num_rows>0)
    {
      $i = 1;
      
      while ($row = mysql_fetch_object($result)) {
      	
        echo '<tr> <td height = "50" align = "center"> <input type="submit" name="try'.$i.'" value="'.$row->enrolment.'" id="'.$row->enrolment.'"></td> </tr>';

        //echo '<TD><INPUT TYPE=BUTTON OnClick="submit_btn(this)" NAME="accepted'.$i.'" VALUE="'.$row->enrolment.'"></TD>';

        $i = $i + 1;

      }
    }

    for($i=1;$i<=$num_rows;$i++)
    {
     if(isset($_REQUEST['try'.$i.'']))
     {
      
      if($i == 1)
      {
        $_SESSION['enrolment'] = '2015MCS2523';
      }
      else if($i == 2)
      {
        $_SESSION['enrolment'] = '2015MCS2534';
      }
      else if($i == 3)
      {
        $_SESSION['enrolment'] = '2016MCS2657';
      }
      else if($i == 4)
      {
        $_SESSION['enrolment'] = '2016MCS2679';
      }
      // echo "shruti";
     	
      // echo $_SESSION['enrolment'];
      header("location:info.php");
     }
   }
    ?>
      
    </tbody>
  </table>
  <br><br><br>
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
