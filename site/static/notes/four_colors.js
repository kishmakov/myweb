var heap = {
    id: [],
    iid: [], // inverse keys index
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
        var oldh = this.h[pos];
        this.h[pos] = newh;

        oldh < newh ? this.shiftDown(pos) : this.shiftUp(pos);
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

            for (var i = 0; i < patterns.length; i++) {
                var loose = borders[i].length < this.bitsIn(patterns[i]);
                var excluded = this.bitsIn(patterns[i]) == 0;
                if (!mark[i] && (loose || excluded)) {
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

            if (patterns[id] == 0) {
                this.colors[id] = 0;
                continue;
            }

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
        {name:'Cuba', neighbors: ['Haiti', 'Jamaica', 'Mexico', 'United States']},
        {name:'Cyprus', neighbors: ['Turkey']},
        {name:'Czech Republic', neighbors: ['Germany', 'Poland', 'Slovakia']},
        {name:'Denmark', neighbors: ['Germany', 'Sweden']},
        {name:'Djibouti', neighbors: ['Eritrea', 'Ethiopia', 'Somalia', 'Yemen']},
        {name:'Dominican Republic', neighbors: ['Haiti']},
        {name:'Ecuador', neighbors: ['Peru']},
        {name:'Egypt', neighbors: ['Libya', 'Sudan', 'Israel']},
        {name:'El Salvador', neighbors: ['Guatemala', 'Honduras']},
        {name:'Equatorial Guinea', neighbors: ['Gabon']},
        {name:'Eritrea', neighbors: ['Ethiopia', 'Sudan']},
        {name:'Estonia', neighbors: ['Finland', 'Latvia', 'Russia']},
        {name:'Ethiopia', neighbors: ['Kenya', 'Somalia','Sudan']},
        {name:'Finland', neighbors: ['Russia', 'Sweden']},
        {name:'France', neighbors: ['Germany', 'Italy', 'Luxembourg', 'Spain', 'Switzerland', 'United Kingdom']},
        {name:'Gabon', neighbors: ['Republic of Congo']},
        {name:'Georgia', neighbors: ['Turkey']},
        {name:'Germany', neighbors: ['Luxembourg', 'Netherlands', 'Poland', 'Switzerland']},
        {name:'Ghana', neighbors: ['Ivory Coast', 'Togo']},
        {name:'Greece', neighbors: ['Macedonia', 'Turkey']},
        {name:'Guatemala', neighbors: ['Mexico', 'Honduras']},
        {name:'Guinea', neighbors: ['Guinea-Bissau', 'Ivory Coast', 'Liberia', 'Mali', 'Sierra Leone', 'Senegal']},
        {name:'Guinea-Bissau', neighbors: ['Senegal']},
        {name:'Guyana', neighbors: ['Suriname', 'Venezuela']},
        {name:'Haiti', neighbors: ['Jamaica']},
        {name:'Honduras', neighbors: ['Nicaragua']},
        {name:'Hungary', neighbors: ['Serbia', 'Slovakia', 'Slovenia', 'Romania', 'Ukraine']},
        {name:'Iceland', neighbors: ['United Kingdom']},
        {name:'India', neighbors: ['Myanmar', 'Nepal', 'Pakistan', 'Sri Lanka']},
        {name:'Indonesia', neighbors: ['Malaysia', 'Philippines', 'Papua New Guinea']},
        {name:'Iran', neighbors: ['Iraq', 'Oman', 'Pakistan', 'Turkey', 'Turkmenistan', 'Quatar', 'U.A.E.']},
        {name:'Iraq', neighbors: ['Jordan', 'Kuwait', 'Saudi Arabia', 'Syria', 'Turkey']},
        {name:'Ireland', neighbors: ['United Kingdom']},
        {name:'Israel', neighbors: ['Jordan', 'Lebanon', 'Syria']},
        {name:'Italy', neighbors: ['Slovenia', 'Switzerland', 'Tunisia']},
        {name:'Ivory Coast', neighbors: ['Liberia', 'Mali']},
        {name:'Japan', neighbors: ['Russia', 'South Korea']},
        {name:'Jordan', neighbors: ['Saudi Arabia', 'Syria']},
        {name:'Kazakhstan', neighbors: ['Kyrgyzstan', 'Russia', 'Turkmenistan', 'Uzbekistan']},
        {name:'Kenya', neighbors: ['Somalia', 'Tanzania', 'Uganda']},
        {name:'Kuwait', neighbors: ['Saudi Arabia']},
        {name:'Kuwait', neighbors: ['Tajikistan', 'Uzbekistan']},
        {name:'Laos', neighbors: ['Myanmar', 'Thailand', 'Vietnam']},
        {name:'Latvia', neighbors: ['Lithuania', 'Russia']},
        {name:'Lebanon', neighbors: ['Syria']},
        {name:'Lesotho', neighbors: ['South Africa']},
        {name:'Liberia', neighbors: ['Sierra Leone']},
        {name:'Libya', neighbors: ['Niger', 'Sudan', 'Tunisia']},
        {name:'Lithuania', neighbors: ['Poland', 'Russia']},
        {name:'Macedonia', neighbors: ['Serbia']},
        {name:'Madagascar', neighbors: ['Mozambique']},
        {name:'Malawi', neighbors: ['Mozambique', 'Tanzania', 'Zambia']},
        {name:'Malaysia', neighbors: ['Thailand']},
        {name:'Mali', neighbors: ['Mauritania', 'Niger', 'Senegal']},
        {name:'Mauritania', neighbors: ['Senegal', 'Western Sahara']},
        {name:'Mexico', neighbors: ['United States']},
        {name:'Moldova', neighbors: ['Romania', 'Ukraine']},
        {name:'Mongolia', neighbors: ['Russia']},
        {name:'Montenegro', neighbors: ['Serbia']},
        {name:'Morocco', neighbors: ['Spain', 'Western Sahara']},
        {name:'Mozambique', neighbors: ['South Africa', 'Swaziland', 'Tanzania', 'Zambia', 'Zimbabwe']},
        {name:'Myanmar', neighbors: ['Thailand']},
        {name:'Namibia', neighbors: ['South Africa', 'Zambia']},
        {name:'Netherlands', neighbors: ['United Kingdom']},
        {name:'Niger', neighbors: ['Nigeria']},
        {name:'North Korea', neighbors: ['Russia', 'South Korea']},
        {name:'Norway', neighbors: ['Sweden', 'Russia']},
        {name:'Oman', neighbors: ['Saudi Arabia', 'U.A.E.', 'Yemen']},
        {name:'Philippines', neighbors: ['Taiwan', 'Vietnam']},
        {name:'Poland', neighbors: ['Russia', 'Slovakia', 'Ukraine']},
        {name:'Portugal', neighbors: ['Spain']},
        {name:'Quatar', neighbors: ['Saudi Arabia']},
        {name:'Romania', neighbors: ['Serbia', 'Ukraine']},
        {name:'Russia', neighbors: ['Ukraine']},
        {name:'Rwanda', neighbors: ['Tanzania', 'Uganda']},
        {name:'Saudi Arabia', neighbors: ['U.A.E.', 'Yemen']},
        {name:'Slovakia', neighbors: ['Ukraine']},
        {name:'Somalia', neighbors: ['Yemen']},
        {name:'South Africa', neighbors: ['Swaziland', 'Zimbabwe']},
        {name:'Sudan', neighbors: ['Uganda']},
        {name:'Syria', neighbors: ['Turkey']},
        {name:'Tajikistan', neighbors: ['Uzbekistan']},
        {name:'Tanzania', neighbors: ['Uganda']},
        {name:'Turkmenistan', neighbors: ['Uzbekistan']},
        {name:'Zambia', neighbors: ['Zimbabwe']}
    ];

    $scope.isocodes = [
        'AF', 'AL', 'DZ', 'AO', 'AR', 'AM', 'AU', 'AT', 'AZ', 'BD', 'BY', 'BE', 'BZ',
        'BJ', 'BT', 'BO', 'BA', 'BW', 'BR', 'BG', 'BF', 'BI', 'KH', 'CM', 'CA', 'CF',
        'TD', 'CL', 'CN', 'CO', 'CD', 'CR', 'HR', 'CU', 'CY', 'CZ', 'DK', 'DJ', 'DO',
        'EC', 'EG', 'SV', 'GQ', 'ER', 'EE', 'ET', 'FI', 'FR', 'GF', 'GA', 'GE', 'DE',
        'GH', 'GR', 'GT', 'GN', 'GW', 'GY', 'HT', 'HN', 'HU', 'IS', 'IN', 'ID', 'IR',
        'IQ', 'IE', 'IL', 'IT', 'CI', 'JM', 'JP', 'JO', 'KZ', 'KE', 'KW', 'KG', 'LA',
        'LV', 'LB', 'LS', 'LR', 'LY', 'LT', 'LU', 'MK', 'MG', 'MW', 'MY', 'ML', 'MR',
        'MX', 'MD', 'MN', 'ME', 'MA', 'MZ', 'MM', 'NA', 'NP', 'NL', 'NZ', 'NI', 'NE',
        'NG', 'KP', 'NO', 'OM', 'PK', 'PA', 'PG', 'PY', 'PE', 'PH', 'PL', 'PT', 'QA',
        'CG', 'RO', 'RU', 'RW', 'SA', 'SN', 'CS', 'SL', 'SK', 'SI', 'SO', 'ZA', 'KR',
        'ES', 'LK', 'SD', 'SR', 'SZ', 'SE', 'CH', 'SY', 'TW', 'TJ', 'TZ', 'TH', 'TG',
        'TN', 'TR', 'TM', 'AE', 'UG', 'UA', 'GB', 'US', 'UY', 'UZ', 'VE', 'VN', 'EH',
        'YE', 'ZM', 'ZW'
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
    $scope.color_groups = [];

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
        $scope.color_groups = [[], [], [], [], []]; // no, 1, 2, 4, 8


        var bin = [];
        var n = result.colorings.length;
        var nbins = Math.floor((n + 5) / 6);

        for (var i = 0; i < nbins; i++) {
            $scope.colorings.push([]);
        }

        for (var i in result.colorings) {
            var color = '';
            var group = 0;
            switch (result.colorings[i].col) {
                case 1: color = 'yellow'; group = 1; break;
                case 2: color = 'green'; group = 2; break;
                case 4: color = 'red'; group = 3; break;
                case 8: color = 'violet'; group = 4;
            }
            $scope.colorings[i % nbins].push({name:$scope.all_states[result.colorings[i].num], color:color});
            $scope.color_groups[group].push($scope.isocodes[i]);
        }

        $scope.resultAs = 'results';
    };

    $scope.resultAs = 'message'; // message, results
    $scope.message = 'With this tool you could produce proper colorings of political map with 4 colors.';
    $scope.message += 'Use left panel to set restrictions: chose countries and possible colors for them.';
    $scope.message += 'If there are no possible colors chosen for particular country, it would be excluded from graph.';
    $scope.message += 'Color assignment could take some time. Please, be patient.';
    $scope.selected = '';
});