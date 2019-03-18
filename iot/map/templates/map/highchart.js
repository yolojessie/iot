function initialize(adr)
        {           
            //var param = location.search.split("?").
            $.ajax({                                      
                url: "{% url 'map:getData' %}", //用以讀取資料的檔案  
                data: {'address': adr},//param[1],             //參數，若有需要可以傳遞給php檔，例如"id=5&parent=6"
                type: 'GET',
                dataType: 'json',       //資料格式    
                    //success:  getDataSuccesss
            }).done(function(data) {
            	console.log('get Data success!!');
    			console.log(data);
                var val = []; //用以存放光敏電阻值
                var stime = []; //用以存放sample time
                var dataNum = data['lightAddresses'].length; //資料筆數
                for (var i = 0; i<dataNum; i++)
                {
                    val.push(parseInt(data['lightAddresses'][i]['value']));//將每筆光敏值放入陣列val中
                    stime.push(data['lightAddresses'][i]['time'].toString());//將每筆光敏值的時間放入陣列stime中
                }
                console.log(data['lightAddresses']);
                
                //console.log('val[]',val);
                //console.log('stime[]',stime);
                var ads = data['lightAddresses'][0]['address'].toString(); //地址
                $('#'+ads).empty();
                //highcharts 圖表設定
                $('#'+ads).highcharts({//在#con中放入highcharts圖表物件
                    title: {//標題
                        text: '光度變化'
                    },
                    subtitle: {//副標題
                        text: ads
                    },
                    scrollbar: {//使圖表可以捲動
                        enabled: true
                    },
                    chart: {
                        type: 'spline',
                        zoomType: 'x'//使圖表可以zoom
                    },
                    xAxis: {//x軸設定
                        tickInterval: 1,
                        labels: {
                            enabled: true,
                            formatter: function(){//以sample time作為x軸的label
                                return stime[this.value];
                                }
                        }
                    },
                    yAxis: {//y軸設定
                        title: {
                            text: 'light value'
                        }
                    },                  
                    series: [//資料來源
                        {                           
                            name: 'light',
                            data: val                       
                        }
                    ],
                    tooltip: {//按下資料點後顯示的內容
                            formatter: function()
                            {
                                return '<b>' + stime[this.x] + '</b><br><li>'+this.series.name+': <b>' + this.y + '</b></li>';
                            }
                        },
                    plotOptions: {//圖形的設定
                        spline: {
                            lineWidth: 3,
                            states: {
                                hover: {
                                    lineWidth: 5
                                }
                            },
                            marker: {
                                enabled: true
                            }                           
                        }
                    }
                });
                console.log('getDataSuccesss(data)...done');
            })
            .fail(function() {
                alert('連線失敗');
            });
            console.log('initialize(adr)...done');
        }
function getDataSuccesss(data)   //接收成功後要執行的動作
        {   
            console.log('get Data success!!');
			console.log(data);
            var val = []; //用以存放光敏電阻值
            var stime = []; //用以存放sample time
            var dataNum = data.length; //資料筆數
            for (var i = 0; i<dataNum; i++)
            {
                val.push(parseInt(data['lightAddresses'][i]['value']));//將每筆光敏值放入陣列val中
                stime.push(data['lightAddresses'][i]['time'].toString());//將每筆光敏值的時間放入陣列stime中
            }
            var ads = data['lightAddresses'][0]['address'].toString(); //地址
            $('#'+ads).empty();
            //highcharts 圖表設定
            $('#'+ads).highcharts({//在#con中放入highcharts圖表物件
                title: {//標題
                    text: '光度變化'
                },
                subtitle: {//副標題
                    text: ads
                },
                scrollbar: {//使圖表可以捲動
                    enabled: true
                },
                chart: {
                    type: 'spline',
                    zoomType: 'x'//使圖表可以zoom
                },
                xAxis: {//x軸設定
                    tickInterval: 1,
                    labels: {
                        enabled: true,
                        formatter: function(){//以sample time作為x軸的label
                            return stime[this.value];
                            }
                    }
                },
                yAxis: {//y軸設定
                    title: {
                        text: 'light value'
                    }
                },                  
                series: [//資料來源
                    {                           
                        name: 'light',
                        data: val                       
                    }
                ],
                tooltip: {//按下資料點後顯示的內容
                        formatter: function()
                        {
                            return '<b>' + stime[this.x] + '</b><br><li>'+this.series.name+': <b>' + this.y + '</b></li>';
                        }
                    },
                plotOptions: {//圖形的設定
                    spline: {
                        lineWidth: 3,
                        states: {
                            hover: {
                                lineWidth: 5
                            }
                        },
                        marker: {
                            enabled: true
                        }                           
                    }
                }
            });
            console.log('getDataSuccesss(data)...done');
        }