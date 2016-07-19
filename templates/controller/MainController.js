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
                 +data.startTime+"&endTime="+data.endTime+"&zid="+data.zid+"&type="+data.type);

        },
        observedDemandHeatMap: function(data){
            return $http.get(apiRoot+"observedDemandHeatMap?startDate="+data.startDate
            +"&endDate="+data.endDate+"&startTime="
            +data.startTime+"&endTime="+data.endTime+"&type="+data.type);

        },
        movingPatern: function(data){
            return $http.get(apiRoot+"movingPatern?startDate="+data.startDate
                +"&endDate="+data.endDate+"&startTime="
                +data.startTime+"&endTime="+data.endTime+"&type="+data.type);

        }
    };
}]);

app.controller("myCtrl", function($scope, service,$rootScope,$location,$window) {

    var no_Of_Blocks = 41;
    // city center
    var max_city_lng = 11.65263;
    var min_city_lng = 11.43874;
    var max_city_lat = 48.20775;
    var min_city_lat = 48.063090;
    var max_airport_lat = 48.366514;
    var max_airport_lng = 11.82077;
    var min_airport_lat = 48.337745;
    var min_airport_lng = 11.744986;
    var max_garching1_lat = 48.271000;
    var max_garching1_lng = 11.680500;
    var min_garching1_lat = 48.258949;
    var min_garching1_lng = 11.661000;
    var max_garching2_lat = 48.260631;
    var max_garching2_lng = 11.638151;
    var min_garching2_lat = 48.243044;
    var min_garching2_lng = 11.601713;

    var lat_factor = 0.00360;
    var lng_factor = 0.00535;

    var max_lat = 48.20775;
    var grid_Line_Color = 'black';
    var grid_weight = 0.5;
    c_zone = {'min_lat':0,
        'max_lat':0,
        'min_lng':0,
        'max_lng':0,
        'count':0}

    $scope.carType = {'dn':'DriveNow','cg':'Car2Go','all':'both'};
    function getCZone(maxLat, maxLng, minLat, minLng){
        var tempZone = JSON.parse(JSON.stringify(c_zone))
        tempZone['max_lat'] = maxLat;
        tempZone['max_lng'] = maxLng;
        tempZone['min_lat'] = minLat;
        tempZone['min_lng'] = minLng;
        tempZone['count'] = 0;
        return tempZone;
    }


    $scope.startDataCollection = function(){
        service.startDataCollection().success(function(data){

        })
    }

    $scope.stopDataCollection = function(){
        service.stopDataCollection().success(function(data){

        })
    }



    function getColor(d){
        return d > 80 ? 'red' :
           d > 60  ? 'orange' :
           d > 40  ? 'yellow' :
           d > 20  ? 'cyan' :
                      'blue';
    }



    var map = L.map('mapid').setView([48.1351, 11.5820], 12);
    var baselayer=L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 20,
        id: 'avinashmishra.0hne8kfo',
        accessToken: 'pk.eyJ1IjoiYXZpbmFzaG1pc2hyYSIsImEiOiJjaXEyc3J6aHEwMDRyaHNtMmh4cTI3ZzFtIn0.fBGbQCOCfnOnEoFkKjlScw'
    })
    baselayer.addTo(map);

    var heatMap_grid_layer;
    var heatMap_info;
    var heatMap_legend;
    var heatMap_points_layer;

    var prob_lines_layer;
    var prob_legend;
    var prob_info;
    var prob_marker_layer;
    $scope.clear = function(){
        if(map.hasLayer(heatMap_grid_layer)){
            map.removeLayer(heatMap_grid_layer);
        }
        if(map.hasLayer(heatMap_points_layer)){
            map.removeLayer(heatMap_points_layer);
        }
        if(map.hasLayer(prob_lines_layer)){
            map.removeLayer(prob_lines_layer);
        }
        if(map.hasLayer(prob_marker_layer)){
            map.removeLayer(prob_marker_layer);
        }
        if(heatMap_info != undefined){
            map.removeControl(heatMap_info);
            heatMap_info = undefined;
        }
        if(heatMap_legend != undefined){
            map.removeControl(heatMap_legend);
            heatMap_legend = undefined
        }
        if(prob_info != undefined){
            map.removeControl(prob_info);
            prob_info = undefined;
        }
        if(prob_legend != undefined){
            map.removeControl(prob_legend);
            prob_legend = undefined;
        }


    }
    $scope.movingProbability = function(info){
        $scope.clear();
        service.movingProbability(info).success(function(response){
            $scope.prob_input = response.data;
            $scope.clear();
            list_lines=[]
            $scope.sourceZone = info.zid;
            var source_node = $scope.prob_input[-1];
            var source_lat = source_node['lat'];
            var source_lng = source_node['lng'];
            var max_prob = 0;
            for(var key in $scope.prob_input){
                if(key != -1 ) {
                    var node = $scope.prob_input[key];
                    if (node['prob'] != 0) {
                        list_lines.push({
                            "type": "Feature",
                            "properties": {'zid': key, 'prob': node['prob']},
                            "geometry": {
                                "type": "LineString",
                                "coordinates": [[source_lng, source_lat], [node['lng'], node['lat']]]
                            }
                        })
                        if (max_prob < node['prob']) {
                            max_prob = node['prob'];
                        }
                    }
                }
            }

            function highlightFeature(e) {
                var layer = e.target;

                layer.setStyle({
                    color: 'black',
                    opacity: 0.6
                });

                if (!L.Browser.ie && !L.Browser.opera) {
                    layer.bringToFront();
                }
                prob_info.update(layer.feature.properties);
            }

            function resetHighlight(e) {
                prob_lines_layer.resetStyle(e.target)
                prob_info.update();
            }

            function onEachFeature(feature, layer) {
                layer.on({
                    mouseover: highlightFeature,
                    mouseout: resetHighlight
                });
            }
            var min_allowed_prob = 10;
            var max_allowed_prob = 50;

            max_prob = Math.min(Math.max(max_prob, min_allowed_prob), max_allowed_prob);

            prob_lines_layer = L.geoJson(list_lines,{
                style: function(feature) {
                        return {color: getColor(feature.properties.prob*100/max_prob), weight:5}
                },
                onEachFeature: onEachFeature
            }).addTo(map);

            var list_marker = [];
            for(var key in $scope.prob_input) {
                if (key != -1) {
                    var node = $scope.prob_input[key];
                    if (node['prob'] != 0) {
                        var marker = L.marker([node['lat'], node['lng']],{color:getColor(node['prob']*100/max_prob)});
                        marker.bindPopup("Probability to zone "+key +" is "+node['prob']/100).openPopup();
                        list_marker.push(marker);
                    }
                }
            }
            var source_marker = L.marker([source_lat,source_lng],{color:'black'});
            source_marker.bindPopup("Source Zone :"+$scope.sourceZone);
            list_marker.push(source_marker);
            prob_marker_layer = L.featureGroup(list_marker).addTo(map);
            prob_info = L.control();

            prob_info.onAdd = function (map) {
                this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
                this.update();
                return this._div;
            };

// method that we will use to update the control based on feature properties passed
            prob_info.update = function (props) {
                this._div.innerHTML = '<h4>Probability of moving: </h4>' +  (props ?
                    'From '+$scope.sourceZone+' to '+props.zid+' is <b>'+ props.prob/100 + '</b>'
                        : 'Hover over a line');
            };

            prob_info.addTo(map);

            prob_legend = L.control({position: 'bottomright'});

            prob_legend.onAdd = function (map) {

                var div = L.DomUtil.create('div', 'info legend'),
                    grades = [0, 20, 40, 60, 80],
                    labels = [];

                // loop through our density intervals and generate a label with a colored square for each interval
                for (var i = 0; i < grades.length; i++) {
                    div.innerHTML += (i==0? '<h4> Probabilities</h4>' :' ')+
                        '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
                        Math.floor((grades[i]*max_prob)/100)/100  + (grades[i + 1] ? '&ndash;' + Math.floor((grades[i + 1]*max_prob)/100)/100 + '<br>' : '+');
                }

                return div;
            };
            prob_legend.addTo(map);

        })
        $('#probabilityModal').modal('hide');
    }


    $scope.observedDemandHeatMap = function(info){
        $scope.sourceZone = undefined;
        service.observedDemandHeatMap(info).success(function(response){
            $scope.clear();
            input = response.data;
            var idx =0;
            zones_dict = {}
            var list_rectangles = [];
            var max_zone_count = 0;
            for(var x =0;x<no_Of_Blocks;x++){
                for(var y=0;y<no_Of_Blocks;y++){
                    var newZone = getCZone(min_city_lat + lat_factor*(x+1), min_city_lng + lng_factor*(y+1), min_city_lat + lat_factor *x, min_city_lng + lng_factor *y);
                    zones_dict[idx] = newZone;
                    for (z=0;z<input.length;z++){
                        var lat_orig=input[z]['lat'];
                        var lng_orig=input[z]['lng'];
                        if(lat_orig>newZone['min_lat'] && lat_orig<=newZone['max_lat'] && lng_orig>newZone['min_lng'] && lng_orig<=newZone['max_lng']){
                            input[z]['zid'] = idx;
                            newZone['count'] = newZone['count'] + 1;
                            console.log(x+'is the selected zone');
                        }
                    }
                    if(max_zone_count < newZone['count']){
                        max_zone_count = newZone['count'];
                    }
                    var bounds = [[newZone['max_lat'], newZone['max_lng']], [newZone['min_lat'], newZone['min_lng']]];
                    var rectangle=L.rectangle(bounds, {color: grid_Line_Color, weight: 1,fillOpacity: 0});
                    // heatMap_grid_layer.addData(
                    list_rectangles.push(
                        {
                            "type": "Feature",
                            "properties": {'zid':idx, 'count':newZone['count']},
                            "geometry": {
                                "type": "Polygon",
                                "coordinates": [[
                                    [newZone['max_lng'], newZone['max_lat']],
                                    [newZone['max_lng'], newZone['min_lat']],
                                    [newZone['min_lng'], newZone['min_lat']],
                                    [newZone['min_lng'], newZone['max_lat']]

                                ]]
                            }
                        });

                    idx++;
                }
            }
            //Airport
            newZone = getCZone(max_airport_lat, max_airport_lng, min_airport_lat, min_airport_lng);
            zones_dict[idx] = newZone;
            for (z=0;z<input.length;z++){
                var lat_orig=input[z]['lat'];
                var lng_orig=input[z]['lng'];
                if(lat_orig>newZone['min_lat'] && lat_orig<=newZone['max_lat'] && lng_orig>newZone['min_lng'] && lng_orig<=newZone['max_lng']){
                    input[z]['zid'] = idx;
                    newZone['count'] = newZone['count'] + 1;
                    console.log(x+'is the selected zone');
                }
            }
            var airport_idx = idx;
            list_rectangles.push(
                {
                    "type": "Feature",
                    "properties": {'zid':idx, 'count':newZone['count']},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [newZone['max_lng'], newZone['max_lat']],
                            [newZone['max_lng'], newZone['min_lat']],
                            [newZone['min_lng'], newZone['min_lat']],
                            [newZone['min_lng'], newZone['max_lat']]

                        ]]
                    }
                });
            idx++;
            newZone = getCZone(max_garching1_lat, max_garching1_lng, min_garching1_lat, min_garching1_lng);

            zones_dict[idx] = newZone;
            for (z=0;z<input.length;z++){
                var lat_orig=input[z]['lat'];
                var lng_orig=input[z]['lng'];
                if(lat_orig>newZone['min_lat'] && lat_orig<=newZone['max_lat'] && lng_orig>newZone['min_lng'] && lng_orig<=newZone['max_lng']){
                    input[z]['zid'] = idx;
                    newZone['count'] = newZone['count'] + 1;
                    console.log(x+'is the selected zone');
                }
            }

            list_rectangles.push(
                {
                    "type": "Feature",
                    "properties": {'zid':idx, 'count':newZone['count']},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [newZone['max_lng'], newZone['max_lat']],
                            [newZone['max_lng'], newZone['min_lat']],
                            [newZone['min_lng'], newZone['min_lat']],
                            [newZone['min_lng'], newZone['max_lat']]

                        ]]
                    }
                });
            idx++;


            // Garching 2
            newZone = getCZone(max_garching2_lat, max_garching2_lng, min_garching2_lat, min_garching2_lng);

            zones_dict[idx] = newZone;
            for (z=0;z<input.length;z++){
                var lat_orig=input[z]['lat'];
                var lng_orig=input[z]['lng'];
                if(lat_orig>newZone['min_lat'] && lat_orig<=newZone['max_lat'] && lng_orig>newZone['min_lng'] && lng_orig<=newZone['max_lng']){
                    input[z]['zid'] = idx;
                    newZone['count'] = newZone['count'] + 1;
                    console.log(x+'is the selected zone');
                }
            }

            list_rectangles.push(
                {
                    "type": "Feature",
                    "properties": {'zid':idx, 'count':newZone['count']},
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [newZone['max_lng'], newZone['max_lat']],
                            [newZone['max_lng'], newZone['min_lat']],
                            [newZone['min_lng'], newZone['min_lat']],
                            [newZone['min_lng'], newZone['max_lat']]

                        ]]
                    }
                });

            // for the geoJSON
            var gridStyle = {
                "color": grid_Line_Color,
                "weight": 1,
                "opacity": 0.2
            };
            function highlightFeature(e) {
                var layer = e.target;

                layer.setStyle({
                    weight: 5,
                    color: '#666',
                    opacity: 0.6
                });

                if (!L.Browser.ie && !L.Browser.opera) {
                    layer.bringToFront();
                }
                heatMap_info.update(layer.feature.properties);
            }

            function resetHighlight(e) {
                heatMap_grid_layer.resetStyle(e.target)
                heatMap_info.update();
            }

            function onEachFeature(feature, layer) {
                layer.on({
                    mouseover: highlightFeature,
                    mouseout: resetHighlight
                });
            }

            heatMap_grid_layer = L.geoJson(list_rectangles,{
                style:gridStyle,
                onEachFeature: onEachFeature
            }).addTo(map);


            var no_of_HeatMap_Colors = 5;
            var max_zone_count_allowed = 50;
            var min_zone_count_allowed = 10;
            max_zone_count = Math.min(Math.max(max_zone_count, min_zone_count_allowed), max_zone_count_allowed);

            color_list = ['blue', 'cyan', 'yellow','orange','red'];
            var list_points = []
            for(var x=0;x<input.length;x++){
                zid = input[x]['zid']
                zone = zones_dict[zid]
                var count = 1;
                if(zone != undefined){
                    count = zone['count']
                }
                var percent = count * 100 /max_zone_count;

                var circle = L.circle([input[x]['lat'], input[x]['lng']], 5, {
                    color: getColor(percent),
        //            fillColor: '#f03',
                    fillOpacity: 0.5
                });
                list_points.push(circle);
            }
            heatMap_points_layer = L.featureGroup(list_points).addTo(map);
            heatMap_info = L.control();

            heatMap_info.onAdd = function (map) {
                this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
                this.update();
                return this._div;
            };

// method that we will use to update the control based on feature properties passed
            heatMap_info.update = function (props) {
                this._div.innerHTML = '<h4>Booked Cars: '+input.length+'</h4>' +  (props ?
                    '<b>zone no.' + props.zid + '</b><br />' + props.count + ' cars booked '
                        : 'Hover over a zone');
            };

            heatMap_info.addTo(map);
            heatMap_legend = L.control({position: 'bottomright'});

            heatMap_legend.onAdd = function (map) {

                var div = L.DomUtil.create('div', 'info legend'),
                    grades = [0, 20, 40, 60, 80],
                    labels = [];

                // loop through our density intervals and generate a label with a colored square for each interval
                for (var i = 0; i < grades.length; i++) {
                    div.innerHTML += (i==0? '<h4> No. of Cars</h4>' :' ')+
                        '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
                        Math.floor((grades[i]*max_zone_count)/100)  + (grades[i + 1] ? '&ndash;' + Math.floor((grades[i + 1]*max_zone_count)/100) + '<br>' : '+');
                }

                return div;
            };
            heatMap_legend.addTo(map);
       })
        $('#observedDemandHeatMapModal').modal('hide');

    }


    $scope.bookingPatern = function(info){
        $scope.sourceZone = undefined;
        service.movingPatern(info).success(function(data){

        })
        $('#bookingPatternModal').modal('hide');
    }



//Garching 1



});