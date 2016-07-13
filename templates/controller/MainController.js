/**
 * Created by r.agrawal on 30.04.2016.
 */
var app = angular.module("mytunnel", []);

app.factory('service',  ['$http', function($http) {
    var apiRoot = "http://localhost:9000/"
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

app.controller("myCtrl", function($scope, service) {

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
    $scope.save = function(){
        console.log($scope.currentConnection.name);
    }
});


