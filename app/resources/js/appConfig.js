'use strict';




toastr.options.positionClass = "toast-bottom-left";
toastr.options.closeButton = true;
toastr.options.showMethod = 'slideDown';
toastr.options.hideMethod = 'slideUp';
//toastr.options.newestOnTop = false;
toastr.options.progressBar = true;
toastr.options.timeOut = 5000;
toastr.options.extendedTimeOut = 1000;
toastr.options.allowHtml = true;




let app = angular.module("youtubeDownload", ['ngAria', 'ngAnimate', 'ngCookies', 'ngMessages',
    'ngSanitize', 'ui.bootstrap', 'ngWebsocket','angularMoment','ngYoutubeEmbed']);



app.config(['$httpProvider', function($httpProvider) {
	$httpProvider.defaults.headers.common["X-Requested-With"] =  'XMLHttpRequest';
	$httpProvider.defaults.headers.common["Accept"] =  'application/json';
    $httpProvider.defaults.headers.common["Content-Type"] =  'application/json';
/*    $httpProvider.defaults.headers.common["X-CSRFToken"] = sessionStorage.getItem("csrf_token");
*/
	if (!$httpProvider.defaults.headers.get) {
        $httpProvider.defaults.headers.get = {};    
    }  

	$httpProvider.defaults.headers.get['If-Modified-Since'] = '0';
	$httpProvider.defaults.headers.get['Cache-Control'] = 'no-cache';
    $httpProvider.defaults.headers.get['Pragma'] = 'no-cache';


}]);



app.run(function(amMoment) {
    amMoment.changeLocale('de');
});


app.filter('joinBy', function () {
    return function (input,delimiter) {
        return (input || []).join(delimiter || ',');
    };
});

app.filter('unsafe', function($sce) { return $sce.trustAsHtml; });

app.filter('trusted', ['$sce', function($sce) {
    var div = document.createElement('div');
    return function(text) {
        div.innerHTML = text;
        return $sce.trustAsHtml(div.textContent);
    };
}]);

app.filter('nl2br', function($sce){
    return function(msg,is_xhtml) { 
        var is_xhtml = is_xhtml || true;
        var breakTag = (is_xhtml) ? '<br />' : '<br>';
        var msg = (msg + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1'+ breakTag +'$2');
        return $sce.trustAsHtml(msg);
    }
});

app.filter('encodeURIComponent', function($window) {
    return $window.encodeURIComponent;
});


app.filter('decodeURIComponent', function($window) {
    return $window.decodeURIComponent;
});


app.filter('decode_utf8', function(e) {
    return decodeURIComponent(escape(s));
});


app.config(function($interpolateProvider) {
	$interpolateProvider.startSymbol('{[{');
	$interpolateProvider.endSymbol('}]}');
});


/*app.config(['$mdAriaProvider', function($mdAriaProvider) {
   // Globally disables all ARIA warnings.
   $mdAriaProvider.disableWarnings();
}]);*/


app.filter('join', function () {
    return function join(array, separator, prop) {
        if (!Array.isArray(array)) {
			return array; // if not array return original - can also throw error
        }

        return (!!prop ? array.map(function (item) {
            return item[prop];
        }) : array).join(separator);
    };
});



app.filter('range', function() {
  return function(input, total) {
    total = parseInt(total);

    for (var i=0; i<total; i++) {
      input.push(i);
    }

    return input;
  };
});

app.filter('cut', function () {
    return function (value, wordwise, max, tail) {
        if (!value) return '';

        max = parseInt(max, 10);
        if (!max) return value;
        if (value.length <= max) return value;

        value = value.substr(0, max);
        if (wordwise) {
            var lastspace = value.lastIndexOf(' ');
            if (lastspace !== -1) {
              //Also remove . and , so its gives a cleaner result.
              if (value.charAt(lastspace-1) === '.' || value.charAt(lastspace-1) === ',') {
                lastspace = lastspace - 1;
              }
              value = value.substr(0, lastspace);
            }
        }

        return value + (tail || ' …');
    };
});



app.filter("abbreviateNumber", () => {
    
    return function(number){
        let SI_SYMBOL = ["", "k", "M", "G", "T", "P", "E"];

        // what tier? (determines SI symbol)
        var tier = Math.log10(Math.abs(number)) / 3 | 0;

        // if zero, we don't need a suffix
        if(tier == 0) return number;

        // get suffix and determine scale
        var suffix = SI_SYMBOL[tier];
        var scale = Math.pow(10, tier * 3);

        // scale the number
        var scaled = number / scale;

        // format number and add suffix
        return scaled.toFixed(1) + suffix;
    }

});



app.filter('durationReadable', () => {
    return function(duration){
        if(duration === undefined) return;
        let minutes = "0" + Math.floor(duration / 60);
        let seconds = "0" + Math.floor(duration - minutes * 60);
        let hour = "0" + Math.floor(duration / 3600);
        if ( hour > 1 )
            duration = hour.substr(-2) + "h " + minutes.substr(-2) + "m " + seconds.substr(-2)+"s";
        else if (minutes > 1)
            duration = minutes.substr(-2) + "m " + seconds.substr(-2)+"s";
        else
            duration = seconds.substr(-2)+ "s";
        return duration;
    }
})




/*app.controller('ModalCtrl', ModalCtrl); 
app.service('ModalEditor', ModalEditor); 

function ModalEditor($http,$uibModal,$rootScope){
    var service = {};
    service.openModal = openModal;

    function openModal(){

        $uibModal.open({
            templateUrl : 'modalTemplate.html',     //modal template
            controller  : [ '$uibModalInstance','$rootScope','$scope', ModalCtrl ] // pass the controller associated with the modal

        });

    }

    return service;
}

function ModalCtrl($uibModalInstance ,$rootScope,$scope){
    //define functions used by the modal

    $scope.ok = function(){
        $uibModalInstance.close()
    }

    $scope.cancel = function(){
        $uibModalInstance.close()
    }

}*/









