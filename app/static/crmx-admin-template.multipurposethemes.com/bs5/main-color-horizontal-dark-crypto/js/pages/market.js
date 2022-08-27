//[Data Table Javascript]

//Project:	CrmX Admin - Responsive Admin Template
//Primary use:   Used only for the Data Table

$(function () {
    "use strict";

	$('#market-data').DataTable({
      'paging'      : false,
      'lengthChange': true,
      'searching'   : true,
      'ordering'    : true,
      'info'        : true,
      'autoWidth'   : false
    });
	
    if ($('.table-market').length) {
			setRandomClass();
			setInterval(function () {
				setRandomClass();
			},1000);
			function setRandomClass() {
				var tbody = $(".table-market table tbody");
				var items = tbody.find("tr");
				var number = items.length;
				var random1 = Math.floor((Math.random() * number));
				var random2 = Math.floor((Math.random() * number));
				items.removeClass("bg-light");
				items.eq(random1).addClass("bg-light");
				items.eq(random2).addClass("bg-light");
			}
		}
	
		/*--- Sparkline charts - mini charts ---*/ 
		function sparkline_charts() {
			$('.sparklines').sparkline('html');
		}
		if ($('.sparklines').length) {
			sparkline_charts();
		} 
	
	
  }); // End of use strict