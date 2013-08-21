var helper = {
    numberOfBits: function (n) {
        if (typeof num !== 'number') {
            return -1;
        }

        switch (n) {
            case 0:
                return 0;
            case 1:case 2:case 4:case 8:
                return 1;
            case 3:case 5:case 6:case 9:case 10:case 12:
                return 2;
            case 7:case 11:case 13:case 14:
                return 3;
            case 15:
                return 4;
        }
    }
}

var painterApp = angular.module('painterApp', []);
painterApp.controller('RestrictionsCrtl', function RestrictionCtrl($scope) {

    $scope.restrictions = [
        {name:'France', violet:true, red:false, green:false, yellow:false},
        {name:'Germany', violet:false, red:false, green:true, yellow:false},
        {name:'Russia', violet:false, red:true, green:false, yellow:false}
    ];

    $scope.borderings = [
        {name:'Argentina', neighbors: ['Bolivia', 'Brazil', 'Chile', 'Falkland Islands', 'Paraguay', 'Uruguay']},
        {name:'Iceland', neighbors: ['Denmark']},
        {name:'Ireland', neighbors: ['United Kingdom']},
        {name:'France', neighbors: ['Germany', 'Italy', 'Luxembourg', 'Spain', 'Switzerland', 'United Kingdom']},
        {name:'Russia', neighbors: ['Azerbaijan', 'Belarus', 'China', 'Estonia', 'Finland', 'Georgia', 'Japan', 'Kazakhstan', 'Latvia', 'Lithuania', 'Mongolia', 'North Korea', 'Poland']}
    ];

    $scope.parseAll = function () {
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

    $scope.parseRestricted = function () {
        var res = [];
        for (var i in $scope.restrictions) {
            var restriction = $scope.restrictions[i];
            res.push(restriction['name'])
        }

        return res.sort();
    };

    $scope.addRestriction = function (name) {
        $scope.chosen_states = [];
        $scope.selected = '';
        $scope.restricted_states.push(name);
        $scope.restrictions.push({name:name, violet:true, red:true, green:true, yellow:true});
    };

    $scope.parseBorderings = function () {
        var edges = new Array();
        for (var i in $scope.all_states) {
            edges[i] = new Array();
        }

        for (var nb in $scope.borderings) {
            var one = $scope.borderings[nb];
            var onei = $scope.all_states.indexOf(one['name']);

            for (var nn in one.neighbors) {
                var twoi = $scope.all_states.indexOf(one.neighbors[nn]);
                edges[onei].push(twoi);
                edges[twoi].push(onei);
            }
        }

        return edges;
    };

    $scope.parsePatterns = function () {
        var res = [];
        for (var i in $scope.all_states) {
            res[i] = 15;
        }

        for (var i in $scope.restrictions) {
            var restriction = $scope.restrictions[i];
            var index = $scope.all_states.indexOf(restriction['name']);
            var pattern = 0;
            pattern += restriction['violet'] ? 8 : 0;
            pattern += restriction['red']    ? 4 : 0;
            pattern += restriction['green']  ? 2 : 0;
            pattern += restriction['yellow'] ? 1 : 0;
            res[index] = pattern;
        }

        var msg = '';

        for (var i in $scope.all_states) {
            msg +=  $scope.all_states[i] + ' = ' + res[i] + ((i % 3) == 2 ? '\n' : ', ');
        }

        alert(msg);

        return res;
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
            if (result.length >= 8) {
                break;
            }
        }

        if (result.length == 1) {
            $scope.addRestriction(result[0]);
            return;
        }

        $scope.chosen_states = result;
    };

    $scope.all_states = $scope.parseAll();
    $scope.restricted_states = $scope.parseRestricted();
    $scope.chosen_states = [];
    $scope.all_borders = $scope.parseBorderings();

    $scope.removeRestriction = function(state) {
        $scope.restricted_states.splice($scope.restricted_states.indexOf(state.name), 1);
        $scope.restrictions.splice($scope.restrictions.indexOf(state), 1);
    };

    $scope.assignColors = function() {
        $scope.message = 'Please wait ...';
        $scope.resultAs = 'message';

        var patterns = $scope.parsePatterns();

//        alert($scope.all_states.length);

        $scope.resultAs = 'results';
    };

    $scope.fire = function (msg) {
        alert(msg);
    };

    $scope.resultAs = ''; // message, results
    $scope.message = '';
    $scope.selected = '';
});