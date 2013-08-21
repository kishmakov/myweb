var painterApp = angular.module('painterApp', []);
painterApp.controller('RestrictionsCrtl', function RestrictionCtrl($scope) {

    $scope.restrictions = [
        {name:'France', violet:true, red:false, green:false, yellow:false},
        {name:'Germany', violet:false, red:false, green:true, yellow:false},
        {name:'Russia', violet:false, red:true, green:false, yellow:false}
    ];

    $scope.borderings = [
        {name:'Argentina', neighbors: ['Bolivia', 'Brazil', 'Chile', 'Falkland Islands', 'Paraguay', 'Uruguay']},
        {name:'France', neighbors: ['Germany', 'Italy', 'Luxembourg', 'Spain', 'Switzerland', 'United Kingdom']}
    ];

    $scope.parseStates = function() {
        var names = {};
        for (var nb in $scope.borderings) {
            var bordering = $scope.borderings[nb];
            names[bordering['name']] = true;
            for (var nn in bordering.neighbors) {
                names[bordering.neighbors[nn]] = true;
            }
        }

        var res = [];
        for (var name in names) {
            res.push(name);
        }

        return res.sort();
    };

    $scope.parseRestrictions = function() {
        var res = [];
        for (var i in $scope.restrictions) {
            var restriction = $scope.restrictions[i];
            res.push(restriction['name'])
        }

        return res.sort();
    };

    $scope.search = function (prefix) {
        var result = [];

        if (prefix === '') {
            $scope.chosen_states = result;
            return;
        }

        var lprefix = prefix.toLowerCase();

        for (var i in $scope.all_states) {
            var current = $scope.all_states[i];
            if ($scope.restricted_states.indexOf(current) >= 0) {
                continue;
            }

            var lcurrent = current.toLowerCase();

            if (lcurrent.indexOf(lprefix) != 0) {
                continue;
            }

            result.push(current);
        }

        $scope.chosen_states = result;
    };

    $scope.addRestriction = function (name) {
        $scope.chosen_states = [];
        $scope.selected = '';
        $scope.restricted_states.push(name);
        $scope.restrictions.push({name:name, violet:true, red:true, green:true, yellow:true});
    };

    $scope.all_states = $scope.parseStates();
    $scope.restricted_states = $scope.parseRestrictions();
    $scope.chosen_states = [];

    $scope.removeRestriction = function(state) {
        $scope.restricted_states.splice($scope.restricted_states.indexOf(state.name), 1);
        $scope.restrictions.splice($scope.restrictions.indexOf(state), 1);
    };

    $scope.assignColors = function() {
        $scope.message = 'Please wait ...';
        $scope.resultAs = 'message';

        alert($scope.all_states.length);

        $scope.resultAs = 'results';
    };

    $scope.fire = function (msg) {
        alert(msg);
    };

    $scope.resultAs = ''; // message, results
    $scope.message = '';
    $scope.selected = '';
});