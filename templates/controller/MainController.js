/**
 * Created by r.agrawal on 30.04.2016.
 */
var app = angular.module("mytunnel", [

]);

app.factory('service',  ['$http', function($http) {
    var apiRoot = "http://localhost:9000/"
    this.info = {};
    return {
        startDataCollection: function(){
            return $http.post(apiRoot+"startDataCollection/"+5)
        },
        stopDataCollection: function(){
            return $http.post(apiRoot+"stopDataCollection")
        },
        movingProbability: function(data){
             return $http.get(apiRoot+"movingProbability?startDate="+data.startDate
                 +"&endDate="+data.endDate+"&startTime="
                 +data.startTime+"&endTime="+data.endTime+"&zid="+data.zid);

        },
        observedDemandHeatMap: function(data){
            return $http.get(apiRoot+"heatMap?startDate="+data.startDate
            +"&endDate="+data.endDate+"&startTime="
            +data.startTime+"&endTime="+data.endTime);

        },
        bookingPatern: function(data){
            return $http.get(apiRoot+"bookingPatern?startDate="+data.startDate
                +"&endDate="+data.endDate+"&startTime="
                +data.startTime+"&endTime="+data.endTime);

        }
    };
}]);

app.controller("myCtrl", function($scope, service,$rootScope,$location,$window) {

    $scope.startDataCollection = function(){
        service.startDataCollection().success(function(data){

        })
    }

    $scope.stopDataCollection = function(){
        service.stopDataCollection().success(function(data){

        })
    }

    $scope.movingProbability = function(info){

        service.movingProbability(info).success(function(data){

        })
        $('#probabilityModal').modal('hide');
    }

    $scope.observedDemandHeatMap = function(info){

        service.observedDemandHeatMap(info).success(function(data){

       })
        $('#observedDemandHeatMap').modal('hide');
    }


    $scope.bookingPatern = function(info){
        service.bookingPatern(info).success(function(data){

        })
        $('#bookingPatern').modal('hide');
    }




    var mymap = L.map('mapid').setView([48.1351, 11.5820], 12);
    var baselayer=L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 20,
        id: 'avinashmishra.0hne8kfo',
        accessToken: 'pk.eyJ1IjoiYXZpbmFzaG1pc2hyYSIsImEiOiJjaXEyc3J6aHEwMDRyaHNtMmh4cTI3ZzFtIn0.fBGbQCOCfnOnEoFkKjlScw'
    })
    baselayer.addTo(mymap);
    
    var no_Of_Blocks = 41;
// city center
    var max_city_lng = 11.65263;
    var min_city_lng = 11.43874;
    var max_city_lat = 48.20775;
    var min_city_lat = 48.063090;

    var lat_factor = 0.00360;
    var lng_factor = 0.00535;

    var max_lat = 48.20775;
    zones_dict = {}
    zone = {'min_lat':0,
        'max_lat':0,
        'min_lng':0,
        'max_lng':0,
        'count':0}
    var grid_Line_Color = 'black';
    var grid_weight = 0.5;
//
//    Airport
    var max_airport_lat = 48.366514;
    var max_airport_lng = 11.82077;
    var min_airport_lat = 48.337745;
    var min_airport_lng = 11.744986;
    //airport grid commented
    // for (i=0;i<9;i++){
    //     var car_coordinates = [
    //         {lat: 48.366514-lat_factor*i, lng: 11.744986},
    //         {lat: 48.366514-lat_factor*i, lng: 11.82077}
    //
    //     ];
    //     var polygon = L.polygon([car_coordinates
    //     ],{
    //         color: '#cc99ff',
    //         fillColor: '#ffffff',
    //         fillOpacity: 0.3
    //     }).addTo(mymap);
    // }
    // for (i=0;i<15;i++){
    //     var car_coordinates = [
    //         {lat: 48.366514, lng: 11.744986+0.00541*i},
    //         {lat: 48.337745, lng: 11.744986+0.00541*i}
    //
    //     ];
    //     var polygon = L.polygon([car_coordinates
    //     ],{
    //         color: '#cc99ff',
    //         fillColor: '#ffffff',
    //         fillOpacity: 0.3
    //     }).addTo(mymap);
    // }

    var input=[{'lat': 48.065283,'lng': 11.443477,'zid':-1},
        {'lat': 48.067628,'lng':11.546044,'zid':-1 },
        {'lat': 48.067241,'lng':11.547678,'zid':-1 },
        {'lat': 48.06601,'lng':11.549174,'zid':-1 },
        {'lat': 48.067271,'lng':11.547525,'zid':-1 }

    ];

//    debugger;
    var idx =0;
    for(var x =0;x<no_Of_Blocks;x++){
        for(var y=0;y<no_Of_Blocks;y++){
            var tempZone = JSON.parse(JSON.stringify(zone))
            tempZone['max_lat'] = min_city_lat + lat_factor*(x+1);
            tempZone['max_lng'] = min_city_lng + lng_factor*(y+1);
            tempZone['min_lat'] = min_city_lat + lat_factor *x;
            tempZone['min_lng'] = min_city_lng + lng_factor *y;
            tempZone['count'] = 0;
            zones_dict[idx] = tempZone;

            var bounds = [[tempZone['max_lat'], tempZone['max_lng']], [tempZone['min_lat'], tempZone['min_lng']]];
            var rectangle=L.rectangle(bounds, {color: grid_Line_Color, weight: 1,fillOpacity: 0}).addTo(mymap);
            idx++;
        }
    }
    var tempZone = JSON.parse(JSON.stringify(zone))
    tempZone['max_lat'] = max_airport_lat;
    tempZone['max_lng'] = max_airport_lng;
    tempZone['min_lat'] = min_airport_lat;
    tempZone['min_lng'] = min_airport_lng;
    tempZone['count'] = 0;
    zones_dict[idx] = tempZone;
    var bounds = [[tempZone['max_lat'], tempZone['max_lng']], [tempZone['min_lat'], tempZone['min_lng']]];
    var rectangle=L.rectangle(bounds, {color: grid_Line_Color, weight: 1,fillOpacity: 0}).addTo(mymap);
    // idx++;
    // var tempZone = JSON.parse(JSON.stringify(zone))
    // tempZone['max_lat'] = min_city_lat + lat_factor*(x+1);
    // tempZone['max_lng'] = min_city_lng + lng_factor*(y+1);
    // tempZone['min_lat'] = min_city_lat + lat_factor *x;
    // tempZone['min_lng'] = min_city_lng + lng_factor *y;
    // tempZone['count'] = 0;
    // zones_dict[idx] = tempZone;
    // var bounds = [[tempZone['max_lat'], tempZone['max_lng']], [tempZone['min_lat'], tempZone['min_lng']]];
    // var rectangle=L.rectangle(bounds, {color: grid_Line_Color, weight: 1,fillOpacity: 0}).addTo(mymap);
    console.log(Object.keys(zones_dict).length);
    for (var x=0;x<Object.keys(zones_dict).length;x++){
        var cur_zone = zones_dict[x];
        for (z=0;z<input.length;z++){
            var lat_orig=input[z]['lat'];
            var lng_orig=input[z]['lng'];
            if(lat_orig>cur_zone['min_lat'] && lat_orig<=cur_zone['max_lat'] && lng_orig>cur_zone['min_lng'] && lng_orig<=cur_zone['max_lng']){
                input[z]['zid'] = x;
                cur_zone['count'] = cur_zone['count'] + 1;
                console.log(x+'is the selected zone');
            }
        }
    }
    var no_of_HeatMap_Colors = 4;
    var max_zone_count = 0;
    for (var x=0;x<Object.keys(zones_dict).length;x++) {
        if(max_zone_count < zones_dict[x]['count']){
            max_zone_count = zones_dict[x]['count'];
        }
    }
    color_list = ['green','yellow','orange','red'];


    console.log(zones_dict);
    console.log(input);

    for(var x=0;x<input.length;x++){
        zid = input[x]['zid']
        var count = zones_dict[zid]['count']
        percent = count * 100 /max_zone_count;
        if(percent <25){
            color = color_list[0];
        }else if(percent <50){
            color = color_list[1];
        }else if(percent <75){
            color = color_list[2];
        }else{
            color = color_list[3];
        }
        var circle = L.circle([input[x]['lat'], input[x]['lng']], 5, {
            color: color,
//            fillColor: '#f03',
            fillOpacity: 0.5
        }).addTo(mymap);
    }



});