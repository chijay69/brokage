//[Dashboard Javascript]

//Project:	CrmX Admin - Responsive Admin Template
//Primary use:   Used only for the main dashboard (index.html)


$(function () {

  'use strict';
	
		
	window.Apex = {
	  chart: {
		foreColor: '#666666',
		toolbar: {
		  show: false
		},
	  },
	  colors: ['#689f38', '#ff8f00'],
	  stroke: {
		width: 3
	  },
	  dataLabels: {
		enabled: false
	  },
	  grid: {
		borderColor: "#f7f7f7",
	  },
	  xaxis: {
		axisTicks: {
		  color: '#cccccc'
		},
		axisBorder: {
		  color: "#cccccc"
		}
	  },
	  fill: {
		type: 'gradient',
		gradient: {
		  gradientToColors: ['#ff8f00', '#689f38']
		},
	  },
	  tooltip: {
		theme: 'dark',
		x: {
		  formatter: function (val) {
			return moment(new Date(val)).format("HH:mm:ss")
		  }
		}
	  },
	  yaxis: {
		decimalsInFloat: 2,
		opposite: true,
		labels: {
		  offsetX: -10
		}
	  }
	};

	var trigoStrength = 3
	var iteration = 11

	function getRandom() {
	  var i = iteration;
	  return (Math.sin(i / trigoStrength) * (i / trigoStrength) + i / trigoStrength + 1) * (trigoStrength * 2)
	}

	function getRangeRandom(yrange) {
	  return Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min
	}

	function generateMinuteWiseTimeSeries(baseval, count, yrange) {
	  var i = 0;
	  var series = [];
	  while (i < count) {
		var x = baseval;
		var y = ((Math.sin(i / trigoStrength) * (i / trigoStrength) + i / trigoStrength + 1) * (trigoStrength * 2))

		series.push([x, y]);
		baseval += 300000;
		i++;
	  }
	  return series;
	}



	function getNewData(baseval, yrange) {
	  var newTime = baseval + 300000;
	  return {
		x: newTime,
		y: Math.floor(Math.random() * (yrange.max - yrange.min + 1)) + yrange.min
	  }
	}

	var optionsColumn = {
	  chart: {
		height: 450,
		type: 'bar',
		animations: {
		  enabled: false
		},
		events: {
		  animationEnd: function (chartCtx, opts) {
			const newData = chartCtx.w.config.series[0].data.slice()
			newData.shift()
			window.setTimeout(function () {
			  chartCtx.updateOptions({
				series: [{
				  data: newData
				}],
				xaxis: {
				  min: chartCtx.minX,
				  max: chartCtx.maxX
				},
				subtitle: {
				  text: parseInt(getRangeRandom({min: 1, max: 20})).toString() + '%',
				}
			  }, false, false)
			}, 300)
		  }
		},
		toolbar: {
		  show: false
		},
		zoom: {
		  enabled: false
		}
	  },
	  dataLabels: {
		enabled: false
	  },
	  stroke: {
		width: 0,
	  },
	  series: [{
		name: 'Load Average',
		data: generateMinuteWiseTimeSeries(new Date("12/12/2021 00:20:00").getTime(), 12, {
		  min: 10,
		  max: 110
		})
	  }],
	  subtitle: {
		text: '20%',
		floating: true,
		align: 'left',
		offsetY: 0,
		style: {
		  fontSize: '22px'
		}
	  },
	  fill: {
		type: 'gradient',
		gradient: {
		  shade: 'dark',
		  type: 'vertical',
		  shadeIntensity: 0.5,
		  inverseColors: false,
		  opacityFrom: 1,
		  opacityTo: 0.8,
		  stops: [0, 100]
		}
	  },
	  xaxis: {
		type: 'datetime',
		range: 2700000
	  },
	  legend: {
		show: true
	  },
	}

	var chartColumn = new ApexCharts(
	  document.querySelector("#columnchart1"),
	  optionsColumn
	);
	chartColumn.render();

	var optionsLine = {
	  chart: {
		height: 350,
		type: 'line',
		stacked: true,
		animations: {
		  enabled: true,
		  easing: 'linear',
		  dynamicAnimation: {
			speed: 1000
		  }
		},
		dropShadow: {
		  enabled: true,
		  opacity: 0.3,
		  blur: 5,
		  left: -7,
		  top: 22
		},
		events: {
		  animationEnd: function (chartCtx) {
			const newData1 = chartCtx.w.config.series[0].data.slice()
			newData1.shift()
			const newData2 = chartCtx.w.config.series[1].data.slice()
			newData2.shift()
			window.setTimeout(function () {
			  chartCtx.updateOptions({
				series: [{
				  data: newData1
				}, {
				  data: newData2
				}],
				subtitle: {
				  text: parseInt(getRandom() * Math.random()).toString(),
				}
			  }, false, false);
			}, 300);
		  }
		},
		toolbar: {
		  show: false
		},
		zoom: {
		  enabled: false
		}
	  },
	  dataLabels: {
		enabled: false
	  },
	  stroke: {
		curve: 'straight',
		width: 5,
	  },
	  grid: {
		padding: {
		  left: 0,
		  right: 0
		}
	  },
	  markers: {
		size: 0,
		hover: {
		  size: 0
		}
	  },
	  series: [{
		name: 'Running',
		data: generateMinuteWiseTimeSeries(new Date("12/12/2019 00:20:00").getTime(), 12, {
		  min: 30,
		  max: 110
		})
	  }, {
		name: 'Waiting',
		data: generateMinuteWiseTimeSeries(new Date("12/12/2019 00:20:00").getTime(), 12, {
		  min: 30,
		  max: 110
		})
	  }],
	  xaxis: {
		type: 'datetime',
		range: 2700000
	  },
	  subtitle: {
		text: '20',
		floating: true,
		align: 'right',
		offsetY: 0,
		style: {
		  fontSize: '22px'
		}
	  },
	  legend: {
		show: true,
		floating: true,
		horizontalAlign: 'left',
		onItemClick: {
		  toggleDataSeries: false
		},
		position: 'top',
		offsetY: -33,
		offsetX: 60
	  },
	};

	
	
	$('.countnm').each(function () {
		$(this).prop('Counter',0).animate({
			Counter: $(this).text()
		}, {
			duration: 5000,
			easing: 'swing',
			step: function (now) {
				$(this).text(Math.ceil(now));
			}
		});
	});
	
	
	
	  
	
}); // End of use strict

