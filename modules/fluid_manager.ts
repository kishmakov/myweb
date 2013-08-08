/// <reference path="tswraps/angularjs/angular.d.ts" />

var app = angular.module('app', []);

app.controller('MyCtrl', function($scope, $window) {
    $scope.greet = function(s: string) {
        $scope.panel = s;
    }

    $scope.panel = 'srk_eq.html';
    $scope.height = function(): number {
        return angular.element($window).height() - 70;
    }
});


app.controller('AnotherCtrl', function($scope) {
    $scope.phrase = 'Bingo!';
});