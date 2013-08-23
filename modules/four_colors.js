var heap = {
    id: [],
    iid: [],
    h: [],
    size: 0,

    swap: function (i, j) {
        var temp = this.id[i]; this.id[i] = this.id[j]; this.id[j] = temp;
        this.iid[this.id[i]] = i;
        this.iid[this.id[j]] = j;
        temp = this.h[i]; this.h[i] = this.h[j]; this.h[j] = temp;
    },

    shiftUp: function (pos) {
        while (pos > 1 && this.h[pos] < this.h[pos >> 1]) {
            this.swap(pos, pos >> 1);
            pos = pos >> 1;
        }
    },

    shiftDown: function (pos) {
        while (true) {
            var best = pos;

            var t = pos << 1;
            if (t <= this.size && this.h[t] > this.h[best]) {
                best = t;
            }

            t = 1 |(pos << 1);
            if (t <= this.size && this.h[t] > this.h[best]) {
                best = t;
            }

            if (pos == best) {
                break;
            }

            this.swap(best, pos);
            pos = best;
        }
    },

    insert: function (id, h) {
        this.size += 1;
        this.id[this.size] = id;
        this.iid[id] = this.size;
        this.h[this.size] = h;

        this.shiftUp(this.size);
    },

    extract: function () {
        this.swap(1, this.size);
        this.size -= 1;
        this.shiftDown(1);

        return this.id[this.size + 1];
    },

    relax: function (id, newh) {
        var pos = this.iid[id];
        if (pos == 0 || pos > this.size) {
            alert('pos: ' + pos + ', size = ' + this.size);
        }
        var oldh = this.h[pos];
        this.h[pos] = newh;

        oldh < newh ? this.shiftDown(pos) : this.shiftUp(pos);
    },

    show: function () {
        msg = '';

        for (var i = 1; i <= this.size; i++) {
            msg += 'i: ' + this.id[i] + ' ii: ' + ((this.iid[this.id[i]] == i) ? 'y' : 'n') + ' h: ' + this.h[i] + '\n';
        }

        alert(msg);
    }
}

var algorithm = {
    n : 0,

    bitsIn: function (n) {
        if (typeof n != 'number') {
            return -1;
        }

        switch (n) {
            case 0:return 0;
            case 1:case 2:case 4:case 8: return 1;
            case 3:case 5:case 6:case 9:case 10:case 12: return 2;
            case 7:case 11:case 13:case 14: return 3;
            case 15: return 4;
            default: return -1;
        }
    },

    weight: function (i) {
        return w = 100 * this.bitsIn(this.pattern[i]) - this.degree[i] - this.mdegree[i];
    },

    initiate: function (borders, pattern) {
        this.pattern = {};
        this.degree = {};
        this.mdegree = {};
        this.colors = {};
        this.marked = {};
        heap.size = 0;

        for (var i = 0; i < this.n; i++) {
            if (0 == borders[i].length) {
                continue;
            }

            this.pattern[i] = pattern[i];
            this.degree[i] = borders[i].length;
            this.mdegree[i] = 0;

            heap.insert(i, this.weight(i));
        }
    },

    run: function (borders) {
        if (heap.size == 0) {
            return true;
        }

        var id = heap.extract();
        this.marked[id] = true;

        for (var c = 1; c <= 8; c <<= 1) {
            if (!(this.pattern[id] & c)) {
                continue;
            }

            this.colors[id] = c;

            var mask = 15 ^ c;
            var oldPatterns = {};

            for (var j in borders[id]) {
                var nid = borders[id][j];
                if (this.marked[nid]) {
                    continue;
                }
                oldPatterns[nid] = this.pattern[nid];
                this.pattern[nid] &= mask;
                this.mdegree[nid] += 1;
                heap.relax(nid, this.weight(nid));
            }

            if (this.run(borders)) {
                return true;
            }

            for (var nid in oldPatterns) {
                this.pattern[nid] = oldPatterns[nid];
                this.mdegree[nid] -= 1;
                heap.relax(nid, this.weight(nid));
            }
        }

        this.marked[id] = false;
        heap.insert(id, this.weight(id))

        return false;
    },

    strip: function (patterns, borders) {
        var strips = [];
        var mark = {};

        while (true) {
            var added = false;

            for (var i = 0; i < this.n; i++) {
                if (!mark[i] && borders[i].length < this.bitsIn(patterns[i])) {
                    added = true;
                    strips.push({num: i, neighbors: borders[i]});
                    for (var j in borders[i]) {
                        var ii = borders[i][j];
                        borders[ii].splice(borders[ii].indexOf(i), 1);
                    }
                    borders[i] = [];
                    mark[i] = true;
                }
            }

            if (!added) {
                break;
            }
        }

        return strips;
    },

    dress: function (patterns, borders, removed) {
        var m = removed.length;

        for (var i = m - 1; i >= 0; i--) {
            var colors = [1, 2, 4, 8];
            var id = removed[i].num;
            borders[id] = removed[i].neighbors;

            for (var j in borders[id]) {
                var nid = borders[id][j];
                borders[nid].push(id);
                var color = this.colors[nid];
                colors.splice(colors.indexOf(color), 1);
            }

            for (var j in colors) {
                var color = colors[j];
                if (color & patterns[id]) {
                    this.colors[id] = color;
                    break;
                }
            }
        }
    },

    solve: function (borders, patterns) {
        this.n = patterns.length;

        var removed = this.strip(patterns, borders);
        this.initiate(borders, patterns);
        var success = this.run(borders);
        this.dress(patterns, borders, removed);

        var result = {resolution: success ? 'OK' : 'Nope', colorings: []};

        for (var i in patterns) {
            result.colorings.push({num: i, col:this.colors[i]});
        }

        return result;
    }
};

var painterApp = angular.module('painterApp', []);
painterApp.controller('RestrictionsCrtl', function RestrictionCtrl($scope) {

    $scope.restrictions = [
        {name:'France', violet:true, red:false, green:false, yellow:false},
        {name:'Germany', violet:false, red:false, green:true, yellow:false},
        {name:'Russia', violet:false, red:true, green:false, yellow:false}
    ];

    $scope.borderings = [
        {name:'Afghanistan', neighbors: ['China', 'Iran', 'Pakistan', 'Tajikistan', 'Turkmenistan', 'Uzbekistan']},
        {name:'Albania', neighbors: ['Greece', 'Macedonia', 'Montenegro', 'Serbia']},
        {name:'Algeria', neighbors: ['Libya', 'Mali', 'Mauritania', 'Morocco', 'Niger', 'Western Sahara', 'Tunisia']},
        {name:'Angola', neighbors: ['Congo', 'Namibia', 'Republic of Congo', 'Zambia']},
        {name:'Argentina', neighbors: ['Bolivia', 'Brazil', 'Chile', 'Paraguay', 'Uruguay']},
        {name:'Armenia', neighbors: ['Azerbaijan', 'Georgia', 'Iran', 'Turkey']},
        {name:'Australia', neighbors: ['Indonesia', 'New Zeland', 'Papua New Guinea']},
        {name:'Austria', neighbors: ['Czech Republic', 'Hungary', 'Italy','Slovakia', 'Slovenia']},
        {name:'Azerbaijan', neighbors: ['Georgia','Iran', 'Russia', 'Turkey']},
        {name:'Bangladesh', neighbors: ['India','Myanmar']},
        {name:'Belarus', neighbors: ['Latvia', 'Lithuania', 'Poland', 'Russia', 'Ukraine']},
        {name:'Belgium', neighbors: ['France', 'Luxembourg', 'Netherlands', 'United Kingdom']},
        {name:'Belize', neighbors: ['Guatemala', 'Mexico']},
        {name:'Benin', neighbors: ['Burkina Faso', 'Niger', 'Nigeria', 'Togo']},
        {name:'Bhutan', neighbors: ['China', 'India']},
        {name:'Bolivia', neighbors: ['Chile', 'Brazil', 'Paraguay', 'Peru']},
        {name:'Bosnia and Herzegovina', neighbors: ['Croatia', 'Montenegro', 'Serbia']},
        {name:'Botswana', neighbors: ['Namibia', 'South Africa', 'Zimbabwe']},
        {name:'Brazil', neighbors: ['Colombia', 'French Guiana', 'Guyana', 'Paraguay', 'Peru', 'Suriname', 'Uruguay', 'Venezuela']},
        {name:'Bulgaria', neighbors: ['Greece', 'Macedonia', 'Romania', 'Serbia', 'Turkey']},
        {name:'Burkina Faso', neighbors: ['Ghana','Mali', 'Niger', 'Togo']},
        {name:'Burundi', neighbors: ['Congo','Rwanda', 'Tanzania']},
        {name:'Cambodia', neighbors: ['Laos', 'Thailand', 'Vietnam']},
        {name:'Cameroon', neighbors: ['Central African Republic', 'Chad', 'Equatorial Guinea', 'Gabon', 'Nigeria','Republic of Congo']},
        {name:'Canada', neighbors: ['Denmark', 'United States']},
        {name:'Central African Republic', neighbors: ['Chad', 'Congo', 'Republic of Congo', 'Sudan']},
        {name:'Chad', neighbors: ['Libya', 'Niger', 'Nigeria', 'Sudan']},
        {name:'Chile', neighbors: ['Peru']},
        {name:'China', neighbors: ['India', 'Kyrgyzstan', 'Kazakhstan','Laos', 'Mongolia', 'Russia','Myanmar', 'Nepal','North Korea', 'Pakistan', 'Taiwan','Tajikistan','Vietnam']},
        {name:'Colombia', neighbors: ['Ecuador', 'Panama', 'Peru', 'Venezuela']},
        {name:'Congo', neighbors: ['Republic of Congo', 'Rwanda', 'Tanzania', 'Uganda', 'Zambia']},
        {name:'Costa Rica', neighbors: ['Nicaragua', 'Panama']},
        {name:'Croatia', neighbors: ['Hungary', 'Serbia', 'Slovenia']},
        {name:'Cuba', neighbors: ['Haiti', 'Mexico', 'United States']},
        {name:'Cyprus', neighbors: ['Turkey']},
        {name:'Czech Republic', neighbors: ['Germany', 'Poland', 'Slovakia']},
        {name:'Denmark', neighbors: ['Germany', 'Norway','Sweden']},
        {name:'Estonia', neighbors: ['Finland', 'Latvia', 'Russia']},
        {name:'Finland', neighbors: ['Russia', 'Sweden']},
        {name:'France', neighbors: ['Germany', 'Italy', 'Luxembourg', 'Spain', 'Switzerland', 'United Kingdom']},
        {name:'Georgia', neighbors: []},
        {name:'Germany', neighbors: ['Luxembourg', 'Netherlands', 'Poland', 'Switzerland']},
        {name:'Iceland', neighbors: ['United Kingdom']},
        {name:'Italy', neighbors: []},
        {name:'Ivory Coast', neighbors: ['Liberia', 'Mali']},
        {name:'Japan', neighbors: ['North Korea', 'South Korea', 'Russia']},
        {name:'Kazakhstan', neighbors: []},
        {name:'Latvia', neighbors: ['Lithuania', 'Russia']},
        {name:'Lithuania', neighbors: ['Polland', 'Russia']},
        {name:'Mongolia', neighbors: ['Russia']},
        {name:'Netherlands', neighbors: ['United Kingdom']},
        {name:'North Korea', neighbors: ['South Korea']},
        {name:'Norway', neighbors: ['Sweden', 'Russia']},
        {name:'Paraguay', neighbors: []},
        {name:'Poland', neighbors: ['Russia', 'Slovakia', 'Ukraine']},
        {name:'Portugal', neighbors: ['Spain']},
        {name:'Russia', neighbors: ['Ukraine']},
        {name:'South Korea', neighbors: ['South Korea']},
        {name:'Sweden', neighbors: ['Poland']},
        {name:'Uruguay', neighbors: []}
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
    $scope.colorings = [];

    $scope.removeRestriction = function(state) {
        $scope.restricted_states.splice($scope.restricted_states.indexOf(state.name), 1);
        $scope.restrictions.splice($scope.restrictions.indexOf(state), 1);
    };

    $scope.assignColors = function() {
        $scope.selected = '';
        var patterns = $scope.parsePatterns();
        var result = algorithm.solve($scope.all_borders, patterns);

        if (result.resolution != 'OK') {
            $scope.message = 'Couldn\'t find a coloring within provided restrictions.\nTry less restrictions.';
            $scope.resultAs = 'message';
            return;
        }

        $scope.colorings = [];
        var bin = [];
        var n = result.colorings.length;
        var n8 = Math.floor((n + 7) / 8);

        for (var i = 0; i < n8; i++) {
            $scope.colorings.push([]);
        }

        for (var i in result.colorings) {
            var color = '';
            switch (result.colorings[i].col) {
                case 1: color = 'yellow'; break;
                case 2: color = 'green'; break;
                case 4: color = 'red'; break;
                case 8: color = 'violet';
            }
            $scope.colorings[i % n8].push({name:$scope.all_states[result.colorings[i].num], color:color});
        }

        $scope.resultAs = 'results';
    };

    $scope.resultAs = 'message'; // message, results
    $scope.message = 'Color assignment could take some time. Be patient.';
    $scope.selected = '';
});