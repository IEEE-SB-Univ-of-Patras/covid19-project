<?php 
/*======================================================================================================================*/ 
/*=====================================================PHP==============================================================*/
/*======================================================================================================================*/ 
declare(strict_types=1);
	$array = array(array(),array(),array(),array());
    function CreatePath(string $MainPath, array $ArgsArray) : string {
        /*Two parameters :
        Inputs:
            string MainPath : contains the main path until our python file
            array ArgsArray : contains the args that we want to pass to the python file
        Outputs:
            return          : A string with the FULL Datapath for shell_exec to be executed
         */
        $argString='';
        $Arr_Length = count($ArgsArray);
        for($i=0;$i<$Arr_Length;$i++){
            $argString.= $ArgsArray[$i];
            if($i<$Arr_Length-1){
                $argString.=' ';
            }
        }
        $datapath = $MainPath.$argString;
        return $datapath;
    }
    function ExecutePrediction(string $Datapath) : string{
        /*One Parameter :
        Inputs:
            string Datapath : returned Datapath from CreatePath Function or Datapath of the python program you want to execute
        Output:
            Data string made from all the prints in python exe
        */

        $SIR_return = shell_exec($Datapath);
        return $SIR_return;
    }
    function InitWorldmeterData(string $NameOfFiletoOpen){
    	/*Parameter : File of Real Data
    	Output:
    		initialize global array $array with the real data*/
        $dataFile=fopen('data/'.$NameOfFiletoOpen.'.txt', 'r');
		$i=0;
		$j=0;
		while(!feof($dataFile)){
			$dataEnrty=fgets($dataFile);
			if($dataEnrty== False){
			}
			else if(substr($dataEnrty,0,3) == 'act'){
				$j=0;
			}
			else if(substr($dataEnrty,0,3) == 'cas'){
				$j=3;
			}
			else if(substr($dataEnrty,0,3) == 'dem'){
					$dataEnrty=fgets($dataFile);
					$dataEnrty=fgets($dataFile);
					$population=$dataEnrty;
			}
			else if(substr($dataEnrty,0,3) == 'dea'){
				$j=1;

			}
			else if(substr($dataEnrty,0,3) == 'rec'){
				$j=2;
			}
			else{
				$array[$j][$i]=$dataEnrty;
				$i++;
			}
		}
		fclose($dataFile);
	}
	function InitPredictionData(string $SIR): array{
		/*Parameter the returned string of ExecutePrediction that is a string with all the data taken from python exe with all the print's
			Output:
				An array with all the prediction Data (DataPredictionbyname)
				0--->Total List
				1--->Death List
				2--->R List
				3--->I List
				4--->S List
				5--->New Cases List
				6--->Date List
				7--->Death Rate List
		*/
		$DataPredictionbyname = array(array(),array(),array(),array(),array(),array(),array(),array());
		$DataArray = explode("---",$SIR);
		for($i = 0 ;$i < count($DataPredictionbyname) ; $i++){
			$DataPredictionbyname[$i] = explode(",",$DataArray[$i]);
			$manipulate = explode("[",$DataPredictionbyname[$i][0]);
			$DataPredictionbyname[$i][0] = $manipulate[1];
			$manipulate = explode("]",$DataPredictionbyname[$i][count($DataPredictionbyname[$i]) - 1]);
			$DataPredictionbyname[$i][count($DataPredictionbyname[$i]) - 1] =$manipulate[0] ;
		}
		for($j = 0 ; $j < count($DataPredictionbyname); $j++){
			for($k = 0 ; $k < count($DataPredictionbyname[$j]);$k++){
				if($j !=6){
				$DataPredictionbyname[$j][$k] = intval($DataPredictionbyname[$j][$k]);
				}
			}
		}
		return $DataPredictionbyname;
	}
	function IntToDate(array $Dates): array{
		/*Parameter:The array of Dates in (int) format
			Output:
				Date array in Year-Month-Day format*/
		for($search = 0 ; $search < count($Dates) ; $search ++){
			$Dates[$search]=date("Y-m-d ", intval($Dates[$search]));
		}
		return $Dates;
	}
    if (!empty($_POST)){
    	$RunVar = (substr($_POST["endingDate"] ,8,2)) - (substr($_POST["startinDate"] ,8 ,2)) ; #Difference of starting and ending date 
        $ArgumentArray = array($_POST["country"] , $RunVar );                                   #Array of args to pass in python exe
        $Datapath = CreatePath('python sir_prediction.py 2>&1',$ArgumentArray);                 #Create Path for input in shell exec method
        $SIR_method = ExecutePrediction($Datapath);                                             #Run Python Model
        $ChartData=InitPredictionData($SIR_method);                                             #Make the Array with all the data from python Dictionary
        $ChartData[6] = IntToDate($ChartData[6]);                                               #Convert INT format of Dates to Year-Month-Day Format

        $EncodedTotalListData = json_encode($ChartData[0]);                                     #-----JSON encode for Chart js-----
        $EncodedDeathList = json_encode($ChartData[1]);
        $EncodedRList = json_encode($ChartData[2]);
        $EncodedIList = json_encode($ChartData[3]);
        $EncodedSList = json_encode($ChartData[4]);
        $EncodedNewCasesList = json_encode($ChartData[5]);
        $EncodedDateData = json_encode($ChartData[6]);
        $EncodedDeathRateList = json_encode($ChartData[7]);                                     #-----End of json encode -----
    }
/*=======================================================================================================================*/ 
/*=====================================================/PHP==============================================================*/
/*=======================================================================================================================*/           
?>

<!DOCTYPE html>
<html>
<head>
    <title>Main Site</title>
    <link rel="stylesheet" type="text/css" href="CSS/style.css">
    <link rel="stylesheet" type="text/css" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.9.3/Chart.min.js"></script>
</head>
<body>
    <div class="outerDiv">
        <div class="header">
            <h1 class="title1">Covid-19 SIR Model </h1>
        </div>
        <div class="navBar">
            <!-- Horizontal Navigation Bar-->
            <label><a href="prediction.php">Prediction</a></label>
	 		<label><a href="comparison.php">Comparison</a></label>
	 		<label><a href="infectivity.php"> Infectivity</a></label>
	 		<label><a href="customscenario.php">Custon Scenario</a></label>
	 		<label><a href="about.php">About</a></label>
	 		<label>More</label>
        </div>
        <div class="sideBar">
            <!-- Vertical Sidebar Bar-->
            <h4>Prediction</h4>
            <h4>Comparison</h4>
            <h4>Infectivity</h4>
            <h4>More</h4>
        </div>
        <form action="index.php" method="post">
            <div class="content">
                <div class="form">
                    <label>Country</label>
                    <select name="country">
						<script language="javascript" type="text/javascript">
							var ListOfCountries = ["world","without China","Afghanistan","Albania","Algeria","Andorra","Angola","Anguilla","Antigua and Barbuda","Argentina",
                "Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda",
                "Bhutan","Bolivia","Bosnia and Herzegovina","Botswana","Brazil","British Virgin Islands","Brunei ","Bulgaria","Burkina Faso","Burundi","CAR",
                "Cabo Verde","Cambodia","Cameroon","Canada","Caribbean Netherlands","Cayman Islands","Chad","Channel Islands","Chile","China","Colombia","Congo",
                "Costa Rica","Croatia","Cuba","Cura&ccedil;ao","Cyprus","Czechia","DRC","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt",
                "El Salvador","Equatorial Guinea","Eritrea","Estonia","Eswatini","Ethiopia","Faeroe Islands","Falkland Islands","Fiji","Finland","France",
                "French Guiana","French Polynesia","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guadeloupe","Guatemala",
                "Guinea","Guinea-Bissau","Guyana","Haiti","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Isle of Man",
                "Israel","Italy","Ivory Coast","Jamaica","Japan","Jordan","Kazakhstan","Kenya","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Liberia","Libya",
                "Liechtenstein","Lithuania","Luxembourg","Macao","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Martinique","Mauritania","Mauritius",
                "Mayotte","Mexico","Moldova","Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Myanmar","Namibia","Nepal","Netherlands",
                "New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","North Macedonia","Norway","Oman","Pakistan","Palestine","Panama","Papua New Guinea",
                "Paraguay","Peru","Philippines","Poland","Portugal","Qatar","R&eacute;union","Romania","Russia","Rwanda","S. Korea","Saint Kitts and Nevis",
                "Saint Lucia","Saint Martin","Saint Pierre Miquelon","San Marino","Sao Tome and Principe","Saudi Arabia","Senegal","Serbia","Seychelles",
                "Sierra Leone","Singapore","Sint Maarten","Slovakia","Slovenia","Somalia","South Africa","South Sudan","Spain","Sri Lanka","St. Barth",
                "St. Vincent Grenadines","Sudan","Suriname","Sweden","Switzerland","Syria","Taiwan","Tanzania","Thailand","Timor-Leste","Togo",
                "Trinidad and Tobago","Tunisia","Turkey","Turks and Caicos","UAE","UK","USA","Uganda","Ukraine","Uruguay","Uzbekistan","Vatican City",
                "Venezuela","Vietnam","Western Sahara","Zambia","Zimbabwe"]
							for(var d=0;d<=ListOfCountries.length-1;d++){
								document.write("<option value="+ ListOfCountries[d] +">"+ ListOfCountries[d] +"</option>");}
						</script>
		 			</select>
                </div>
                <div class="form">
                    <label>Starting Date</label>
                    <input type="date" name="startinDate">
                </div>
                <div class="form">
                    <label>Ending Date</label>
                    <input type="date" name="endingDate">
                </div>
                <div class="Button">
                    <input type="submit" name="submit" onclick = "" value="Submit">
                </div>
            </div>
        </form>
    </div>
    <div style="height: 600px;width: 700px;">
    	<canvas id="myChart"></canvas>
    </div>
    <script>
    	/*=======================================================================================================================*/ 
    	/*==================================================JavaScript Chart JS==================================================*/ 
    	/*=======================================================================================================================*/ 
    	let myChart = document.getElementById('myChart').getContext('2d'); /*Take the position that canvas will be diplayed*/
    	let SIR_PredictionChart = new Chart(myChart,{                      /*Make a Chart object*/
    		type:'line',
    		data:{
    			labels:<?php echo $EncodedDateData; ?>,                    /*labels takes the converted Dates */
    			datasets:[{                                                /*Datasets take the json encoded Prediction Data from the upper php code */
    				label:'Total',
    				fill: false,
    				data:<?php echo $EncodedTotalListData ;?>,
    				backgroundColor : 'blue',
    				borderColor:'blue'
    			},
    			{
    				label:'Deaths',
    				fill: false,
    				data:<?php echo $EncodedDeathList ;?>,
    				backgroundColor : 'red' ,
    				borderColor:'red'
    			},
    			{
    				label:'New Cases',
    				fill: false,
    				data:<?php echo $EncodedNewCasesList ;?>,
    				backgroundColor : 'black' ,
    				borderColor:'black'
    			},
    			{
    				label:'Death Rate',
    				fill: false,
    				data:<?php echo $EncodedDeathRateList ;?>,
    				backgroundColor : 'lightblue' ,
    				borderColor:'lightblue'
    			},
    			]
    		},
    		options:{                                                      /*Graphics*/
    			title:{
    				display:true,
    				text:"Prediction"
    			}
    		}
    	});
    </script>
</body>
</html>