/**
 * Created by r.agrawal on 30.04.2016.
 */
var app = angular.module("mytunnel", []);

app.factory('service',  ['$http', function($http) {
    var apiRoot = "http://192.168.33.147:8080/api/connection"
    return {
        create: function(connection) {
            // console.log(connection);
            return $http.post(apiRoot, connection);
        },
        edit: function(connection) {
            return $http.put(apiRoot+connection.id, connection);
        },
        findAll: function() {
            return $http.get(apiRoot);
        },
        find: function(connectionId) {
            return $http.get(apiRoot+ '/' + connectionId);
        },
        delete: function(connectionId) {
            return $http.delete(apiRoot + '/' + connectionId);
            // console.log("done");
        },
        startConnection: function(connectionId){
            return $http.post("http://192.168.33.147:8080/connect?id=" + connectionId );
        },
        stopConnection: function(connectionId){
            return $http.put(apiRoot + '/' + connectionId + '/' + stop);
        }
    };
}]);

app.controller("myCtrl", function($scope, service) {
    $scope.currentConnection = {
        isAccessKey:false
    };
    service.findAll().success(function(data){
        $scope.connections = data.objects;
        console.log($scope.connections);
    })
    $scope.save = function(){
        if($scope.currentConnection.id){
            service.edit($scope.currentConnection).success(function(data){
                _.merge($scope.currentConnection, data);
            });
        } else {
            service.create($scope.currentConnection).success(function(data){

                $scope.connections.push(data);
            });
        }
        $('#myModal').modal('hide');
    }

    $scope.editConnection = function(connection) {
        $scope.currentConnection = connection;

    }
    $scope.startConnection = function(connection){
        service.startConnection(connection.id).success(function(data){
            console.log(data);
            // _.merge(connection.isAlive, data);
        });
    }

    $scope.stopConnection = function(connectionId){
        service.stopConnection(connection.id).success(function(data){
            _.merge(connection.isAlive, data);
        });
    }

    $scope.deleteConnection = function(connectionId) {
        service.delete(connectionId)
    }

    $scope.togglePrivateKey = function(){
        $scope.currentConnection.isAccessKey = !$scope.currentConnection.isAccessKey;
    }
});


app.factory('prob_data',['$http',function($http){
    return $http.get('https://xyz.json')
        .success(function(data){
            return data;
        })
        .error(function(err){
            return err;
        });
}]);
app.controller('prob_ctrl',['$scope','prob_data',functions($scope,prob_data){
    prob_data.sucess=(function(data){
    $scope.probability=data;
    })

}])