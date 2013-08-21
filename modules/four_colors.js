var painterApp = angular.module('painterApp', []);
painterApp.controller('RestrictionsCrtl', function RestrictionCtrl($scope) {
    $scope.restricted_states = [
        {name:'France', violet:true, red:false, green:false, yellow:false},
        {name:'Germany', violet:false, red:false, green:true, yellow:false},
        {name:'Russia', violet:false, red:true, green:false, yellow:false}
    ];

    $scope.borderings = [
        {state:'Argentina', neighbors: ['Bolivia', 'Brazil', 'Chile', 'Falkland Islands', 'Paraguay', 'Uruguay']},
        {state:'France', neighbors: ['Germany', 'Italy', 'Luxembourg', 'Spain', 'Switzerland', 'United Kingdom']}
    ];

    $scope.removeRestriction = function(state) {
        $scope.restricted_states.splice($scope.restricted_states.indexOf(state), 1);
    };

    $scope.addRestriction = function() {
        $scope.restricted_states.push({name:'Argentina', violet:false, red:true, green:true, yellow:false});

    }
});
