/******/ (() => { // webpackBootstrap
/******/ 	var __webpack_modules__ = ({

/***/ "./app/resources/js/appConfig.js":
/*!***************************************!*\
  !*** ./app/resources/js/appConfig.js ***!
  \***************************************/
/***/ (() => {

"use strict";


toastr.options.positionClass = "toast-bottom-left";
toastr.options.closeButton = true;
toastr.options.showMethod = 'slideDown';
toastr.options.hideMethod = 'slideUp';
//toastr.options.newestOnTop = false;
toastr.options.progressBar = true;
toastr.options.timeOut = 5000;
toastr.options.extendedTimeOut = 1000;
toastr.options.allowHtml = true;
var app = angular.module("youtubeDownload", ['ngAria', 'ngAnimate', 'ngCookies', 'ngMessages', 'ngSanitize', 'ui.bootstrap', 'ngWebsocket', 'angularMoment', 'ngYoutubeEmbed']);
app.config(['$httpProvider', function ($httpProvider) {
  $httpProvider.defaults.headers.common["X-Requested-With"] = 'XMLHttpRequest';
  $httpProvider.defaults.headers.common["Accept"] = 'application/json';
  $httpProvider.defaults.headers.common["Content-Type"] = 'application/json';
  /*    $httpProvider.defaults.headers.common["X-CSRFToken"] = sessionStorage.getItem("csrf_token");
  */
  if (!$httpProvider.defaults.headers.get) {
    $httpProvider.defaults.headers.get = {};
  }
  $httpProvider.defaults.headers.get['If-Modified-Since'] = '0';
  $httpProvider.defaults.headers.get['Cache-Control'] = 'no-cache';
  $httpProvider.defaults.headers.get['Pragma'] = 'no-cache';
}]);
app.run(function (amMoment) {
  amMoment.changeLocale('de');
});
app.filter('joinBy', function () {
  return function (input, delimiter) {
    return (input || []).join(delimiter || ',');
  };
});
app.filter('unsafe', function ($sce) {
  return $sce.trustAsHtml;
});
app.filter('trusted', ['$sce', function ($sce) {
  var div = document.createElement('div');
  return function (text) {
    div.innerHTML = text;
    return $sce.trustAsHtml(div.textContent);
  };
}]);
app.filter('nl2br', function ($sce) {
  return function (msg, is_xhtml) {
    var is_xhtml = is_xhtml || true;
    var breakTag = is_xhtml ? '<br />' : '<br>';
    var msg = (msg + '').replace(/([^>\r\n]?)(\r\n|\n\r|\r|\n)/g, '$1' + breakTag + '$2');
    return $sce.trustAsHtml(msg);
  };
});
app.filter('encodeURIComponent', function ($window) {
  return $window.encodeURIComponent;
});
app.filter('decodeURIComponent', function ($window) {
  return $window.decodeURIComponent;
});
app.filter('decode_utf8', function (e) {
  return decodeURIComponent(escape(s));
});
app.config(function ($interpolateProvider) {
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
app.filter('range', function () {
  return function (input, total) {
    total = parseInt(total);
    for (var i = 0; i < total; i++) {
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
        if (value.charAt(lastspace - 1) === '.' || value.charAt(lastspace - 1) === ',') {
          lastspace = lastspace - 1;
        }
        value = value.substr(0, lastspace);
      }
    }
    return value + (tail || ' …');
  };
});
app.filter("abbreviateNumber", function () {
  return function (number) {
    var SI_SYMBOL = ["", "k", "M", "G", "T", "P", "E"];

    // what tier? (determines SI symbol)
    var tier = Math.log10(Math.abs(number)) / 3 | 0;

    // if zero, we don't need a suffix
    if (tier == 0) return number;

    // get suffix and determine scale
    var suffix = SI_SYMBOL[tier];
    var scale = Math.pow(10, tier * 3);

    // scale the number
    var scaled = number / scale;

    // format number and add suffix
    return scaled.toFixed(1) + suffix;
  };
});
app.filter('durationReadable', function () {
  return function (duration) {
    if (duration === undefined) return;
    var minutes = "0" + Math.floor(duration / 60);
    var seconds = "0" + Math.floor(duration - minutes * 60);
    var hour = "0" + Math.floor(duration / 3600);
    if (hour > 1) duration = hour.substr(-2) + "h " + minutes.substr(-2) + "m " + seconds.substr(-2) + "s";else if (minutes > 1) duration = minutes.substr(-2) + "m " + seconds.substr(-2) + "s";else duration = seconds.substr(-2) + "s";
    return duration;
  };
});

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

/***/ }),

/***/ "./app/resources/js/facialCtrl.js":
/*!****************************************!*\
  !*** ./app/resources/js/facialCtrl.js ***!
  \****************************************/
/***/ (() => {

// NB : Remettre dans l'ordre !!!!

angular.module("youtubeDownload").controller("facialCtrl", ['$scope', '$http', '$interval', function ($scope, $http, $interval) {
  $scope.tags = [];
  $scope.groups = [];
  $scope.currentTags = [];
  $scope.sequenceTags = {};
  $scope.groupTags = {};
  $scope.currentVideo = null;
  $scope.currentGroup = null;
  $scope.load_videos = true;
  $scope.load_sequences = true;
  var modalGroups = new bootstrap.Modal(document.getElementById('modalGroups'));
  $scope.openModalGroups = function () {
    return modalGroups.show();
  };
  $scope.videos = {
    'page_number': 0,
    'number_per_page': 3,
    'total_page': 0,
    'previous': [],
    'current': [],
    'next': []
  };
  $scope.sequences = {
    'page_number': 0,
    'number_per_page': 6,
    'total_page': 0,
    'previous': [],
    'current': [],
    'next': []
  };
  $scope.loadTags = function () {
    $http({
      method: 'POST',
      url: '/api/facials/tags/',
      responseType: 'json',
      headers: {
        "X-CSRFToken": sessionStorage.getItem("csrf_token")
      },
      data: {}
    }).then(function successCallBack(response) {
      $scope.tags = response.data;
    }, function errorCallback(error) {
      console.error(error);
      toastr.error(error.statusText, "Error " + error.status);
    });
  };
  $scope.loadTags();
  $scope.loadGroups = function () {
    $http({
      method: 'POST',
      url: '/api/facials/groups/',
      responseType: 'json',
      headers: {
        "X-CSRFToken": sessionStorage.getItem("csrf_token")
      },
      data: {}
    }).then(function successCallBack(response) {
      $scope.groups = response.data;
      if ($scope.groups.length > 0) {
        $scope.currentGroup = $scope.groups[0];
        angular.forEach($scope.groups, function (group) {
          $scope.groupTags[group.id] = group.tags.map(function (t) {
            return t.value;
          });
        });
      }
    }, function errorCallback(error) {
      console.error(error);
      toastr.error(error.statusText, "Error " + error.status);
    });
  };
  $scope.loadGroups();
  $scope.loadVideos = function () {
    $http({
      method: 'POST',
      url: '/api/facials/videos/',
      responseType: 'json',
      headers: {
        "X-CSRFToken": sessionStorage.getItem("csrf_token")
      },
      data: {
        'page_number': $scope.videos['page_number'],
        'number_per_page': $scope.videos['number_per_page']
      }
    }).then(function successCallBack(response) {
      var rep = response.data;
      $scope.videos['page_number'] = rep.page_number;
      $scope.videos['number_per_page'] = rep.number_per_page;
      $scope.videos['total_page'] = rep.total_page;
      $scope.videos['current'] = rep.data;
      $scope.load_videos = false;
      $scope.gen_nextVideos();
      $scope.currentVideo = rep.data[0];
      $scope.initSequences();
    }, function errorCallback(error) {
      console.error(error);
      toastr.error(error.statusText, "Error " + error.status);
    });
  };
  $scope.loadVideos();
  $scope.onSelectTag = function () {
    if ($scope.currentTags.indexOf($scope.selectedTag) == -1) $scope.currentTags.push($scope.selectedTag);
    $scope.selectedTag = null;
  };
  $scope.onNewTag = function (keyEvent) {
    if (keyEvent.which === 13) {
      if ($scope.tags.map(function (t) {
        return t.value;
      }).indexOf($scope.selectedTag) >= 0) return;
      $http({
        method: 'POST',
        url: '/api/facials/tags/new/',
        responseType: 'json',
        headers: {
          "X-CSRFToken": sessionStorage.getItem("csrf_token")
        },
        data: {
          "tag_value": $scope.selectedTag
        }
      }).then(function successCallBack(response) {
        $scope.tags.push(response.data);
        $scope.currentTags.push(response.data.value);
        $scope.selectedTag = null;
      }, function errorCallback(error) {
        console.error(error);
        toastr.error(error.statusText, "Error " + error.status);
      });
    }
  };
  $scope.onRemoveTag = function (tag) {
    var idx = $scope.tags.indexOf(tag);
    if (idx == -1) return false;
    $http({
      method: 'POST',
      url: '/api/facials/tags/remove/',
      responseType: 'json',
      headers: {
        "X-CSRFToken": sessionStorage.getItem("csrf_token")
      },
      data: {
        "tag_id": tag.id
      }
    }).then(function successCallBack(response) {
      $scope.tags.splice(idx, 1);
    }, function errorCallback(error) {
      console.error(error);
      toastr.error(error.statusText, "Error " + error.status);
    });
    return true;
  };
  $scope.onSelectGroup = function () {
    $scope.currentGroup = $scope.selectedGroup;
  };
  $scope.onNewGroup = function (keyEvent) {
    if (keyEvent.which === 13) {
      if ($scope.groups.map(function (g) {
        return g.value;
      }).indexOf($scope.selectedGroup) >= 0) return;
      $http({
        method: 'POST',
        url: '/api/facials/groups/new/',
        responseType: 'json',
        headers: {
          "X-CSRFToken": sessionStorage.getItem("csrf_token")
        },
        data: {
          "group_value": $scope.selectedGroup
        }
      }).then(function successCallBack(response) {
        $scope.groups.push(response.data);
        $scope.currentGroup = response.data;
        $scope.selectedGroup = null;
      }, function errorCallback(error) {
        console.error(error);
        toastr.error(error.statusText, "Error " + error.status);
      });
    }
  };
  $scope.onRemoveGroup = function (group) {
    var idx = $scope.groups.indexOf(group);
    if (idx == -1) return false;
    if (group.id == $scope.currentGroup.id) $scope.currentGroup = null;
    $http({
      method: 'POST',
      url: '/api/facials/groups/remove/',
      responseType: 'json',
      headers: {
        "X-CSRFToken": sessionStorage.getItem("csrf_token")
      },
      data: {
        "group_id": group.id
      }
    }).then(function successCallBack(response) {
      $scope.groups.splice(idx, 1);
    }, function errorCallback(error) {
      console.error(error);
      toastr.error(error.statusText, "Error " + error.status);
    });
    return true;
  };
  $scope.tagInSequence = function (sequence, tag_value) {
    if ($scope.sequenceTags[sequence.id] == undefined) return false;
    return $scope.sequenceTags[sequence.id].indexOf(tag_value) >= 0;
  };
  $scope.tagInCurrentGroup = function (tag) {
    if ($scope.currentGroup == undefined) return false;
    return $scope.currentGroup.tags.map(function (t) {
      return t.value;
    }).indexOf(tag.value) >= 0;
  };
  $scope.setTagSequence = function (sequence, tag_value) {
    if ($scope.sequenceTags[sequence.id].indexOf(tag_value) >= 0) {
      $scope.sequenceTags[sequence.id].splice($scope.sequenceTags[sequence.id].indexOf(tag_value), 1);
      $scope.xhr_delTag(sequence, tag_value);
    } else {
      $scope.sequenceTags[sequence.id].push(tag_value);
      $scope.xhr_addTag(sequence, tag_value);
    }
  };
  $scope.setTagGroup = function (tag) {
    if ($scope.currentGroup.tags.map(function (t) {
      return t.value;
    }).indexOf(tag.value) >= 0) {
      $scope.currentGroup.tags.splice($scope.currentGroup.tags.map(function (t) {
        return t.value;
      }).indexOf(tag.value), 1);
      $scope.xhr_delGroup($scope.currentGroup, tag.id);
    } else {
      $scope.currentGroup.tags.push(tag);
      $scope.xhr_addGroup($scope.currentGroup, tag.id);
    }
  };
  $scope.setCurrentGroup = function (group) {
    $scope.currentGroup = group;
  };
  $scope.isCurrentGroup = function (group) {
    return $scope.currentGroup == group;
  };

  /////////////////////////////////////////
  //////////////  XHR GROUP & TAGS  ///////
  /////////////////////////////////////////

  $scope.xhr_addTag = function (sequence, tag_value) {
    $http({
      method: 'POST',
      url: '/api/facials/tags/add/',
      responseType: 'json',
      headers: {
        "X-CSRFToken": sessionStorage.getItem("csrf_token")
      },
      data: {
        'sequence_id': sequence.id,
        "tag_value": tag_value
      }
    }).then(function successCallBack(response) {
      var rep = response.data;
    }, function errorCallback(error) {
      console.error(error);
      toastr.error(error.statusText, "Error " + error.status);
    });
  };
  $scope.xhr_delTag = function (sequence, tag_value) {
    $http({
      method: 'POST',
      url: '/api/facials/tags/del/',
      responseType: 'json',
      headers: {
        "X-CSRFToken": sessionStorage.getItem("csrf_token")
      },
      data: {
        'sequence_id': sequence.id,
        'tag_value': tag_value
      }
    }).then(function successCallBack(response) {
      var rep = response.data;
    }, function errorCallback(error) {
      console.error(error);
      toastr.error(error.statusText, "Error " + error.status);
    });
  };
  $scope.xhr_addGroup = function (group, tag_id) {
    $http({
      method: 'POST',
      url: '/api/facials/groups/add/',
      responseType: 'json',
      headers: {
        "X-CSRFToken": sessionStorage.getItem("csrf_token")
      },
      data: {
        'group_id': group.id,
        "tag_id": tag_id
      }
    }).then(function successCallBack(response) {
      var group = response.data;
      $scope.groupTags[group.id] = group.tags.map(function (t) {
        return t.value;
      });
    }, function errorCallback(error) {
      console.error(error);
      toastr.error(error.statusText, "Error " + error.status);
    });
  };
  $scope.xhr_delGroup = function (group, tag_id) {
    $http({
      method: 'POST',
      url: '/api/facials/groups/del/',
      responseType: 'json',
      headers: {
        "X-CSRFToken": sessionStorage.getItem("csrf_token")
      },
      data: {
        'group_id': group.id,
        'tag_id': tag_id
      }
    }).then(function successCallBack(response) {
      var group = response.data;
      $scope.groupTags[group.id] = group.tags.map(function (t) {
        return t.value;
      });
    }, function errorCallback(error) {
      console.error(error);
      toastr.error(error.statusText, "Error " + error.status);
    });
  };

  /////////////////////////////////////////
  //////////////  VIDEOS  /////////////////
  /////////////////////////////////////////

  $scope.setVideo = function (video) {
    $scope.sequences = {
      'page_number': 0,
      'number_per_page': 8,
      'total_page': 0,
      'previous': [],
      'current': [],
      'next': []
    };
    $scope.currentTags = [];
    $scope.sequenceTags = {};
    $scope.load_sequences = true;
    $scope.currentVideo = video;
    $scope.initSequences();
  };
  $scope.nextVideos = function () {
    if ($scope.videos['page_number'] + 1 > $scope.videos['total_page']) return;
    angular.copy($scope.videos['current'], $scope.videos['previous']);
    angular.copy($scope.videos['next'], $scope.videos['current']);
    $scope.videos['page_number']++;
    $scope.gen_nextVideos();
  };
  $scope.previousVideos = function () {
    if ($scope.videos['page_number'] - 1 < 0) return;
    angular.copy($scope.videos['current'], $scope.videos['next']);
    angular.copy($scope.videos['previous'], $scope.videos['current']);
    $scope.videos['page_number']--;
    $scope.gen_prevVideos();
  };
  $scope.removeVideo = function (video) {
    $http({
      method: 'POST',
      url: '/api/facials/videos/remove/',
      responseType: 'json',
      headers: {
        "X-CSRFToken": sessionStorage.getItem("csrf_token")
      },
      data: {
        'video_id': video.id
      }
    }).then(function successCallBack(response) {
      var rep = response.data;
      $scope.loadVideos();
    }, function errorCallback(error) {
      console.error(error);
      toastr.error(error.statusText, "Error " + error.status);
    });
  };
  $scope.gen_nextVideos = function () {
    if ($scope.videos['page_number'] + 1 > $scope.videos['total_page']) {
      $scope.sequences['next'] = [];
      return;
    }
    $http({
      method: 'POST',
      url: '/api/facials/videos/',
      responseType: 'json',
      headers: {
        "X-CSRFToken": sessionStorage.getItem("csrf_token")
      },
      data: {
        'page_number': $scope.videos['page_number'] + 1,
        'number_per_page': $scope.videos['number_per_page']
      }
    }).then(function successCallBack(response) {
      var rep = response.data;
      $scope.videos['next'] = rep.data;
    }, function errorCallback(error) {
      console.error(error);
      toastr.error(error.statusText, "Error " + error.status);
    });
  };
  $scope.gen_prevVideos = function () {
    if ($scope.videos['page_number'] - 1 < 0) {
      $scope.videos['previous'] = [];
      return;
    }
    $http({
      method: 'POST',
      url: '/api/facials/videos/',
      responseType: 'json',
      headers: {
        "X-CSRFToken": sessionStorage.getItem("csrf_token")
      },
      data: {
        'page_number': $scope.videos['page_number'] - 1,
        'number_per_page': $scope.videos['number_per_page']
      }
    }).then(function successCallBack(response) {
      var rep = response.data;
      $scope.videos['previous'] = rep.data;
    }, function errorCallback(error) {
      console.error(error);
      toastr.error(error.statusText, "Error " + error.status);
    });
  };

  /////////////////////////////////////////
  //////////////  SEQUENCES  //////////////
  /////////////////////////////////////////

  $scope.initSequencesTags = function () {
    angular.forEach($scope.sequences, function (listSeq) {
      angular.forEach(listSeq, function (seq) {
        $scope.sequenceTags[seq.id] = seq.tags.map(function (t) {
          return t.value;
        });
        angular.forEach(seq.tags, function (tag) {
          if ($scope.currentTags.indexOf(tag.value) == -1) $scope.currentTags.push(tag.value);
        }, $scope);
      }, $scope);
    });
  };
  $scope.initHandlerSequences = function (sequences) {
    angular.forEach(sequences, function (seq) {
      seq.num_seq = 0;
      seq.max_seq = seq.faces.length;
      seq.image_current = seq.faces[0];
      seq.timer_animate = null;
      seq.getNextImage = function () {
        if (seq.num_seq == seq.max_seq) seq.num_seq = 0;else seq.num_seq += 1;
        seq.image_current = seq.faces[seq.num_seq];
        return;
      };
      seq.getPrevImage = function () {
        if (seq.num_seq == 0) seq.num_seq = seq.max_seq;else seq.num_seq -= 1;
        seq.image_current = seq.faces[seq.num_seq];
        return;
      };
      seq.animate = function () {
        seq.timer_animate = $interval(function () {
          seq.getNextImage();
        }, 200);
      };
      seq.stop = function () {
        $interval.cancel(seq.timer_animate);
      };
    });
  };
  $scope.initSequences = function () {
    $http({
      method: 'POST',
      url: '/api/facials/sequences/',
      responseType: 'json',
      headers: {
        "X-CSRFToken": sessionStorage.getItem("csrf_token")
      },
      data: {
        'video_id': $scope.currentVideo.id,
        'page_number': $scope.sequences['page_number'],
        'number_per_page': $scope.sequences['number_per_page']
      }
    }).then(function successCallBack(response) {
      var rep = response.data;
      $scope.sequences['page_number'] = rep.page_number;
      $scope.sequences['number_per_page'] = rep.number_per_page;
      $scope.sequences['total_page'] = rep.total_page;
      $scope.sequences['current'] = rep.data;
      $scope.initHandlerSequences($scope.sequences['current']);
      $scope.initSequencesTags();
      $scope.load_sequences = false;
      $scope.gen_nextSequences();
    }, function errorCallback(error) {
      console.error(error);
      toastr.error(error.statusText, "Error " + error.status);
    });
  };
  $scope.nextSequences = function () {
    if ($scope.sequences['page_number'] + 1 > $scope.sequences['total_page']) return;
    $scope.initHandlerSequences($scope.sequences['next']);
    angular.copy($scope.sequences['current'], $scope.sequences['previous']);
    angular.copy($scope.sequences['next'], $scope.sequences['current']);
    $scope.initSequencesTags();
    $scope.sequences['page_number']++;
    $scope.gen_nextSequences();
  };
  $scope.previousSequences = function () {
    if ($scope.sequences['page_number'] - 1 < 0) return;
    $scope.initHandlerSequences($scope.sequences['previous']);
    angular.copy($scope.sequences['current'], $scope.sequences['next']);
    angular.copy($scope.sequences['previous'], $scope.sequences['current']);
    $scope.initSequencesTags();
    $scope.sequences['page_number']--;
    $scope.gen_prevSequences();
  };
  $scope.removeSequence = function (sequence) {
    $http({
      method: 'POST',
      url: '/api/facials/sequences/remove/',
      responseType: 'json',
      headers: {
        "X-CSRFToken": sessionStorage.getItem("csrf_token")
      },
      data: {
        'sequence_id': sequence.id
      }
    }).then(function successCallBack(response) {
      var rep = response.data;
      $scope.initSequences();
    }, function errorCallback(error) {
      console.error(error);
      toastr.error(error.statusText, "Error " + error.status);
    });
  };
  $scope.gen_nextSequences = function () {
    if ($scope.sequences['page_number'] + 1 > $scope.sequences['total_page']) {
      $scope.sequences['next'] = [];
      return;
    }
    $http({
      method: 'POST',
      url: '/api/facials/sequences/',
      responseType: 'json',
      headers: {
        "X-CSRFToken": sessionStorage.getItem("csrf_token")
      },
      data: {
        'video_id': $scope.currentVideo.id,
        'page_number': $scope.sequences['page_number'] + 1,
        'number_per_page': $scope.sequences['number_per_page']
      }
    }).then(function successCallBack(response) {
      var rep = response.data;
      $scope.sequences['next'] = rep.data;
      $scope.initSequencesTags();
    }, function errorCallback(error) {
      console.error(error);
      toastr.error(error.statusText, "Error " + error.status);
    });
  };
  $scope.gen_prevSequences = function () {
    if ($scope.sequences['page_number'] - 1 < 0) {
      $scope.sequences['previous'] = [];
      return;
    }
    $http({
      method: 'POST',
      url: '/api/facials/sequences/',
      responseType: 'json',
      headers: {
        "X-CSRFToken": sessionStorage.getItem("csrf_token")
      },
      data: {
        'video_id': $scope.currentVideo.id,
        'page_number': $scope.sequences['page_number'] - 1,
        'number_per_page': $scope.sequences['number_per_page']
      }
    }).then(function successCallBack(response) {
      var rep = response.data;
      $scope.sequences['previous'] = rep.data;
      $scope.initSequencesTags();
    }, function errorCallback(error) {
      console.error(error);
      toastr.error(error.statusText, "Error " + error.status);
    });
  };
}]);

/***/ }),

/***/ "./app/resources/js/historyCtrl.js":
/*!*****************************************!*\
  !*** ./app/resources/js/historyCtrl.js ***!
  \*****************************************/
/***/ (() => {

angular.module("youtubeDownload").controller("historyCtrl", ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {
  $scope.downloaded = [];
  $scope.videos = [];
  $scope.number_per_page = 10;
  $scope.page_number = 1;
  $scope.ytSocket = new WebSocket('wss://' + window.location.host + '/ws/downloads/');
  $scope.ytSocket.onclose = function (e) {
    $scope.error = 'Videos socket closed unexpectedly';
    console.error(e);
    toastr.error('Videos socket closed unexpectedly', e);
    $timeout(function () {
      window.location.reload();
    }, 5000);
  };
  $scope.ytSocket.onerror = function (e) {
    $scope.error = 'Videos socket closed unexpectedly';
    console.error('Videos socket error');
    console.error(e);
    toastr.error('Videos socket error', e);
  };
  $http({
    method: 'POST',
    url: '/api/getHistory/',
    responseType: 'json',
    headers: {
      "X-CSRFToken": sessionStorage.getItem("csrf_token")
    },
    data: {
      'number_per_page': $scope.number_per_page,
      "page_number": $scope.page_number
    }
  }).then(function successCallBack(response) {
    $scope.downloaded = response.data;
    $scope.videos = response.data.map(function (d) {
      return d.video;
    });
  }, function errorCallback(error) {
    console.error(error);
    toastr.error(error.statusText, "Error " + error.status);
  });
  $scope.downloading = function (pathoffile, filename) {
    $http.get(pathoffile, {
      responseType: "arraybuffer"
    }).then(function (response) {
      $scope.filedata = response.data;
      /*		        $scope.ytSocket.send(JSON.stringify({
      		        	"message_type": "download.update",
      		        	"youtube_id": $scope.youtube_id,
      		        	"download_id": $scope.data.download_id
      		        }));*/

      var headers = response.headers();
      headers['Content-Disposition'] = "attachment";
      var blob = new Blob([response.data], {
        type: "octet/stream"
      });
      var link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    });
  };
}]);

/***/ }),

/***/ "./app/resources/js/homeCtrl.js":
/*!**************************************!*\
  !*** ./app/resources/js/homeCtrl.js ***!
  \**************************************/
/***/ (() => {

angular.module("youtubeDownload").controller("homeCtrl", ['$scope', '$window', '$document', '$http', '$timeout', '$interval', '$filter', 'ngYoutubeEmbedService', function ($scope, $window, $document, $http, $timeout, $interval, $filter, ngYoutubeEmbedService) {
  /*
  		navigator.clipboard.readText()
    .then(text => {
      console.log('Pasted content: ', text);
    })
    .catch(err => {
      console.error('Failed to read clipboard contents: ', err);
    });*/

  /*  console.log(window.clipboardData);
  */

  $document.on('scroll', function () {
    // do your things like logging the Y-axis
    /*		    console.log($window.scrollY);
    */
    // or pass this to the scope
    $scope.$apply(function () {
      var elem = $("#next_videos");
      var docViewTop = $window.scrollY;
      var docViewBottom = docViewTop + $(window).height();
      var elemTop = elem.offset().top - elem.height();
      var elemBottom = elemTop + elem.height();
      if (docViewTop <= elemTop && docViewBottom >= elemBottom && $scope.videos['next'].length > 0) $scope.nextVideos();
    });
  });

  /*		$scope.$watch(function () {
      	return $window.scrollY;
  		}, function (scrollY) {
  		    console.log(scrollY);
  		});*/

  var checkitem = function checkitem() {
    var $this;
    $this = $("#carousel_website");
    if ($("#carousel_website .carousel-inner .carousel-item:first").hasClass("active")) {
      $this.children(".carousel-control-prev").hide();
      $this.children(".carousel-control-next").show();
    } else if ($("#carousel_website .carousel-inner .carousel-item:last").hasClass("active")) {
      $this.children(".carousel-control-next").hide();
      $this.children(".carousel-control-prev").show();
    } else {
      $this.children(".carousel-control-next").show();
      $this.children(".carousel-control-prev").show();
    }
  };
  checkitem();
  $("#carousel_website").on("slid.bs.carousel", "", checkitem);
  $scope.website = "youtube";
  $scope.website_patterns = {
    'youtube': "https://www.youtube.com/watch?v=........",
    'dailymotion': "https://www.dailymotion.com/video/....",
    'vimeo': "https://vimeo.com/..........",
    'facebook': "http://www.facebook.com/v/..............",
    'instagram': "https://www.instagram.com/reel/..........",
    'odnoklassniki': "https://ok.ru/video/..........."
  };
  var MAX_QUEUE = 6;
  var MAX_RETRIEVE = 6;
  var MAX_RETRIEVE_SEC = 6;
  $scope.url = "";
  $scope.error = "";
  $scope.debugMsg = "";
  $scope.url_id = "";
  $scope.onInfos = false;
  $scope.onInfosLoading = true;
  $scope.onProcessing = false;
  $scope.onLoadQueue = false;
  $scope.onDownload = {};
  $scope.onFirstLoading = true;
  $scope.onVideosLoading = true;
  $scope.onYoutubeLoading = true;
  $scope.infos = {};
  $scope.data = {};
  $scope.queue = {};
  $scope.videoPlay = null;
  $scope.onQueue = function () {
    return false;
  };
  $scope.lenQueue = function () {
    return Object.keys($scope.queue).length;
  };
  $scope.audioFormat = "best";
  $scope.formatVideo = "best";

  /*		const modalVideoEl = document.getElementById('modalVideo');
  		const modalVideo = new bootstrap.Modal(modalVideoEl);
  		modalVideoEl.addEventListener('show.bs.modal', function (event) {
  			let player = ngYoutubeEmbedService.getPlayerById('videoPlayer');
  			//console.log(player);
  			//player.playVideo();
  		});
  
  		modalVideoEl.addEventListener('hidden.bs.modal', function (event) {
  			let player = ngYoutubeEmbedService.getPlayerById('videoPlayer');
  			$scope.onYoutubeLoading = true;
  			//player.stopVideo();
  		});*/

  $scope.playerReady = function (event) {
    $scope.onYoutubeLoading = false;
    console.log("playerReady");
    console.log(event);
  };
  $scope.playerStateChanged = function (event) {
    console.log("playerStateChanged");
    console.log(event);
  };

  /*		const getHistory = () => {
  			$http({
  			    method: 'POST',
  			    url: '/api/getHistory/',
  			    responseType:'json',
  			    headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
  			    data: {'number_per_page': 6, "page_number": 0}
  			}).then(function successCallBack(response) {
  				$scope.history = response.data;
  			}, function errorCallback(error) {
  			    console.error(error);
  			    toastr.error(error.statusText, "Error "+error.status);
  			});
  		}
  		getHistory();*/

  $scope.videos = {
    'page_number': 0,
    'number_per_page_base': 6,
    'number_per_page': 6,
    'total_page': 0,
    'previous': [],
    'current': [],
    'next': [],
    'next_loading': false,
    'prev_loading': false,
    'filter_order': 'lastDownloaded'
  };
  $scope.nextVideos = function () {
    if ($scope.videos['page_number'] + 1 > $scope.videos['total_page']) return;
    angular.forEach($scope.videos['next'], function (video) {
      $scope.videos['current'].push(video);
    });
    $scope.videos['page_number']++;
    $scope.videos['number_per_page'] += $scope.videos['number_per_page_base'];
    gen_nextVideos();
  };
  $scope.previousVideos = function () {
    if ($scope.videos['page_number'] - 1 < 0) return;
    angular.copy($scope.videos['current'], $scope.videos['next']);
    angular.copy($scope.videos['previous'], $scope.videos['current']);
    $scope.videos['page_number']--;
    gen_prevVideos();
  };
  $scope.formatVideoFilter = function (video) {
    angular.forEach(video.formats, function (format) {
      if (!format.format_note && format.height > 0) format.format_note = format.height + "p";
    });
    var formats = video.formats.filter(function (f) {
      return f.width && f.height;
    });
    if (formats.length == 0) formats = video.formats.filter(function (f) {
      return f.width && f.height;
    });
    if (formats.length == 0) formats = video.formats;
    angular.forEach(formats, function (format) {
      if (!format.format_note) format.format_note = format.format_id;
    });
    formats = formats.sort(function (a, b) {
      x = a.quality;
      y = b.quality;
      return x < y ? -1 : x > y ? 1 : 0;
    });
    var output = [],
      keys = [];
    angular.forEach(formats, function (item) {
      var key = item.format_note;
      if (keys.indexOf(key) === -1) {
        keys.push(key);
        output.push(item);
      }
    });
    video.videoFormat = output[Math.floor(output.length / 2)];
    return output;
  };
  $scope.formatAudioFilter = function (audio) {
    var formats = audio.formats.filter(function (f) {
      return f.format_note == "tiny";
    });
    formats = formats.sort(function (a, b) {
      x = a.quality;
      y = b.quality;
      return x < y ? -1 : x > y ? 1 : 0;
    });
    audio.audioFormat = formats[Math.floor(formats.length / 2)];
    return formats;
  };
  var loadVideos = function loadVideos() {
    $http({
      method: 'POST',
      url: '/api/videos/videos/',
      responseType: 'json',
      headers: {
        "X-CSRFToken": sessionStorage.getItem("csrf_token")
      },
      data: {
        'page_number': $scope.videos['page_number'],
        'number_per_page': $scope.videos['number_per_page'],
        'filter_order': $scope.videos['filter_order']
      }
    }).then(function successCallBack(response) {
      var rep = response.data;
      $scope.videos['total_page'] = rep.total_page;
      $scope.videos['page_number'] = rep.page_number;
      $scope.videos['current'] = rep.data;
      gen_nextVideos();
      if (rep.data.length > 0) $scope.videoPlay = rep.data[0];
      $scope.onVideosLoading = false;
      $scope.onFirstLoading = false;
    }, function errorCallback(error) {
      console.error(error);
      toastr.error(error.statusText, "Error " + error.status);
    });
  };
  loadVideos();
  $scope.loadVideos = loadVideos;
  var reloadVideos = function reloadVideos() {
    $http({
      method: 'POST',
      url: '/api/videos/videos/',
      responseType: 'json',
      headers: {
        "X-CSRFToken": sessionStorage.getItem("csrf_token")
      },
      data: {
        'page_number': 0,
        'number_per_page': $scope.videos['number_per_page'],
        'filter_order': $scope.videos['filter_order']
      }
    }).then(function successCallBack(response) {
      var rep = response.data;
      $scope.videos['total_page'] = rep.total_page;
      $scope.videos['current'] = rep.data;
      gen_nextVideos();
      if (rep.data.length > 0) $scope.videoPlay = rep.data[0];
      $scope.onVideosLoading = false;
    }, function errorCallback(error) {
      console.error(error);
      toastr.error(error.statusText, "Error " + error.status);
    });
  };
  var gen_nextVideos = function gen_nextVideos() {
    if ($scope.videos['page_number'] + 1 > $scope.videos['total_page']) {
      $scope.videos['next'] = [];
      return;
    }
    $scope.videos.next_loading = true;
    $http({
      method: 'POST',
      url: '/api/videos/videos/',
      responseType: 'json',
      headers: {
        "X-CSRFToken": sessionStorage.getItem("csrf_token")
      },
      data: {
        'page_number': $scope.videos['page_number'] + 1,
        'number_per_page': $scope.videos['number_per_page_base'],
        'filter_order': $scope.videos['filter_order']
      }
    }).then(function successCallBack(response) {
      var rep = response.data;
      $scope.videos['next'] = rep.data;
      $scope.videos.next_loading = false;
    }, function errorCallback(error) {
      console.error(error);
      toastr.error(error.statusText, "Error " + error.status);
    });
  };
  var gen_prevVideos = function gen_prevVideos() {
    if ($scope.videos['page_number'] - 1 < 0) {
      $scope.videos['previous'] = [];
      return;
    }
    $http({
      method: 'POST',
      url: '/api/videos/videos/',
      responseType: 'json',
      headers: {
        "X-CSRFToken": sessionStorage.getItem("csrf_token")
      },
      data: {
        'page_number': $scope.videos['page_number'] - 1,
        'number_per_page': $scope.videos['number_per_page_base'],
        'filter_order': $scope.videos['filter_order']
      }
    }).then(function successCallBack(response) {
      var rep = response.data;
      $scope.videos['previous'] = rep.data;
    }, function errorCallback(error) {
      console.error(error);
      toastr.error(error.statusText, "Error " + error.status);
    });
  };
  $scope.showVideo = function (video) {
    $scope.videoPlay = video;
    modalVideo.show();
  };

  /*		const clickToastr = (msg) => {
  			console.log(msg);
  		}
  
  		toastr.options.onclick = (e) => {
  			console.log(this);
  		}
  
  		toastr.info("voila","title", {"data":{"message":"coucou"}});*/

  /***********DOWNLOADER FINALE AJAX***********/

  var prepareBlob = function prepareBlob(data) {
    var filename = $filter("trusted")(data.filename) + "." + data.format_file.ext;
    $scope.queue[data.download_id]['download'] = true;
    $http.get(data.file_path, {
      responseType: "arraybuffer"
    }).then(function (response) {
      if (!$scope.queue[data.download_id]) return;
      $scope.queue[data.download_id]['download'] = false;
      $scope.filedata = response.data;
      var headers = response.headers();
      headers['Content-Disposition'] = "attachment";
      var blob = new Blob([response.data], {
        type: "octet/stream"
      });
      var link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.id = data.download_id;
      link.download = filename;
      document.body.appendChild(link);
      $scope.queue[data.download_id]['status'] = "finished";
    }, function (error) {
      $scope.queue[data.download_id]['download'] = false;
      console.error(error);
      toastr.error(error.statusText, "Error " + error.status);
    });
  };
  $scope.download = function (data) {
    var link = document.getElementById(data.download_id);
    link.click();
  };

  /***********WEB SOCKETS***********/

  var proto = "wss://";
  if (window.location.protocol == "http:") proto = "ws://";
  $scope.ytSocket = new WebSocket(proto + window.location.host + '/ws/downloads/');
  $scope.ytSocket.onmessage = function (e) {
    data = JSON.parse(e.data);
    console.log(data.message_type);
    console.log(data);
    if (data.message_type == "queue.get") {
      if (data.downloading.length > 0) $scope.onLoadQueue = true;else $scope.onLoadQueue = false;
      angular.forEach(data.downloading, function (down) {
        $scope.queue[down.id] = {
          filename: down.filename,
          thumbnail: down.thumbnail,
          url_id: down.url_id,
          _percent_str: down.percent + "%",
          _percent_float: down.percent
        };
        $scope.ytSocket.send(JSON.stringify({
          'message_type': "download.reload",
          'download_id': down.id
        }));
      });
    }
    if (data.message_type == "queue.del") $scope.$apply(function (event) {
      var link = document.getElementById(data.download_id);
      if (link) document.body.removeChild(link);
      if ($scope.queue[data.download_id]) delete $scope.queue[data.download_id];
      if ($scope.queue.length > 0) $scope.onLoadQueue = true;else $scope.onLoadQueue = false;
    });
    if (data.message_type == "download.started") $scope.$apply(function (event) {
      $scope.url = "";
      $scope.onProcessing = false;
      $scope.onInfos = false;
      $scope.onInfosLoading = true;
      $scope.queue[data.download_id] = {
        _percent_str: "0.00 %",
        _percent_float: 0
      };
      $scope.queue[data.download_id] = data;
      $scope.queue[data.download_id]['download'] = false;
      toastr.info("Téléchargement débuté.", data.filename);
    });
    if (data.message_type == "download.debug") $scope.$apply(function (event) {
      if (data.download_id !== undefined) {
        if (!$scope.queue[data.download_id]) $scope.queue[data.download_id] = {
          _percent_str: "0.00 %",
          _percent_float: 0
        };
        $scope.queue[data.download_id] = data;
        $scope.queue[data.download_id]['download'] = false;
        if (data.status == "finished") {
          $scope.queue[data.download_id]['status'] = "prepare";
          prepareBlob(data);
        }
      }
    });
    if (data.message_type == "download.progress") $scope.$apply(function (event) {
      if (data.downloaded_bytes == data.total_bytes) {
        $scope.queue[data.download_id]['status'] = "prepare";
        prepareBlob(data);
        return;
      }
      if (data.download_id !== undefined) $scope.queue[data.download_id] = data;
    });
    if (data.message_type == "download.warning") $scope.$apply(function (event) {
      console.error("download.warning");
      console.error(data);
      toastr.warning(data.content, "Warning");
      if (data.download_id !== undefined) $scope.queue[data.download_id]['error'] = false;
      $scope.queue[data.download_id]['warning'] = true;
      $scope.queue[data.download_id]['content'] = data.content;
    });
    if (data.message_type == "download.error") $scope.$apply(function (event) {
      console.error("download.error");
      console.error(data);
      toastr.warning(data.content, "Error");
      if (data.download_id !== undefined) {
        $scope.queue[data.download_id]['error'] = true;
        $scope.queue[data.download_id]['warning'] = false;
        $scope.queue[data.download_id]['nbRetrieve'] = MAX_RETRIEVE;
        $scope.queue[data.download_id]['content'] = data.content;
        var down_id = data.download_id;
        $interval(function () {
          if (!$scope.queue[down_id]) return;
          if ($scope.queue[down_id]['nbRetrieve'] > 0) $scope.queue[down_id]['nbRetrieve']--;else {
            $scope.ytSocket.send(JSON.stringify({
              'message_type': "download.reload",
              'download_id': down_id
            }));
          }
        }, 1000, MAX_RETRIEVE + 1);
      }
    });
    if (data.message_type == "download.finished") $scope.$apply(function (event) {
      console.log("download.finished");
      console.log(data);
      if (data.download_id !== undefined) $scope.queue[data.download_id] = data;
    });
  };
  $scope.ytSocket.onclose = function (e) {
    $scope.error = 'Videos socket closed unexpectedly';
    console.error(e);
    toastr.error('Videos socket closed unexpectedly', e);
    $timeout(function () {
      window.location.reload();
    }, 5000);
  };
  $scope.ytSocket.onerror = function (e) {
    $scope.error = 'Videos socket closed unexpectedly';
    console.error('Videos socket error');
    console.error(e);
    toastr.error('Videos socket error', e);
  };

  // La connexion est ouverte
  $scope.ytSocket.addEventListener('open', function (event) {
    console.log('Videos socket opened');
    $scope.ytSocket.send(JSON.stringify({
      'message_type': "queue.get"
    }));
    return;
  });

  /******************PATTERNS DOWNLOADS******************/

  var youtubePattern = /^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$/;
  var dailyPattern = /^(?:https?:\/\/)?(?:www\.)?dailymotion.com\/(video|hub)+(\/([^_]+))?[^#]*(#‎video=([^_&]+))?$/;
  var vimeoPattern = /|^(?:https?:\/\/)?(?:www\.)?vimeo.com\/([0-9]+)$/;
  var instaPattern = /|^(?:https?:\/\/)?(?:www\.)?instagram.com\/reel\/([^_&]+)$/;
  var okruPattern = /|^(?:https?:\/\/)?(?:www\.)?ok.ru\/video\/([0-9]+)$/;
  $scope.pattern = youtubePattern + "|" + dailyPattern + "|";
  $scope.pattern += vimeoPattern + "|" + instaPattern + "|" + okruPattern;
  $scope.patterns = {
    'youtube': /youtu(?:.*\/v\/|.*v\=|\.be\/)([A-Za-z0-9_\-]{11})/,
    'dailymotion': /^.+dailymotion.com\/(?:video|swf\/video|embed\/video|hub|swf)\/([A-Za-z0-9_\-]+)/,
    'vimeo': /vimeo.com\/([0-9]*)/i,
    'facebook': /^.+facebook.com\/v\/(.*)/,
    'instagram': /^.+instagram.com\/reel\/([A-Za-z0-9_\-]*)/,
    'odnoklassniki': /^.+ok.ru\/video\/([0-9]*)/
  };
  $scope.submitForm = function (form) {
    console.log("submit");
    console.log(form.url.$valid);
  };
  var checkDomain = function checkDomain() {
    var domain = $scope.website;
    angular.forEach(['youtube', 'dailymotion', 'vimeo', 'instagram', 'odnoklassniki'], function (name) {
      var pattern = $scope.patterns[name];
      if ($scope.url.match(pattern) && $scope.url.match(pattern).length > 1) domain = name;
    });
    if (domain != $scope.website) $scope.website = domain;
    var first = ['youtube', 'dailymotion', 'vimeo'];
    var second = ['facebook', 'instagram', 'odnoklassniki'];
    var carousel_website = document.querySelector('#carousel_website');
    var carousel = new bootstrap.Carousel(carousel_website);
    var index = $('#carousel_website').find('.active').index();
    if (first.indexOf(domain) >= 0) carousel.to(0);else if (second.indexOf(domain) >= 0) carousel.to(1);else carousel.to(2);
    return domain;
  };
  var checkId = function checkId() {
    checkDomain();
    var pattern = $scope.patterns[$scope.website];
    if ($scope.url.match(pattern) && $scope.url.match(pattern).length > 1) {
      $scope.onInfosLoading = true;
      $scope.onInfos = true;
      $scope.url_id = $scope.url.match(pattern)[1];
      loadInfos();
    }
  };
  var loadInfos = function loadInfos() {
    $http({
      method: 'POST',
      url: 'api/videos/infos/',
      responseType: 'json',
      headers: {
        "X-CSRFToken": sessionStorage.getItem("csrf_token")
      },
      data: {
        'url': $scope.url,
        'website': $scope.website
      }
    }).then(function (rep) {
      $scope.onInfosLoading = false;
      /*				let minutes = "0" + Math.floor(rep.data.duration / 60);
      				let seconds = "0" + Math.floor(rep.data.duration - minutes * 60);
      				let hour = "0" + Math.floor(rep.data.duration / 3600);
      				if ( hour > 1 )
      					rep.data.duration = hour.substr(-2) + "h " + minutes.substr(-2) + "m " + seconds.substr(-2)+"s";
      				else if (minutes > 1)
      					rep.data.duration = minutes.substr(-2) + "m " + seconds.substr(-2)+"s";
      				else
      					rep.data.duration = seconds.substr(-2)+ "s";
      
      				rep.data.upload_date = moment.unix(rep.data.upload_date).fromNow();*/

      rep.data.videoFormats = $scope.formatVideoFilter(rep.data);
      $scope.videoFormat = rep.data.videoFormat;
      rep.data.audioFormats = $scope.formatAudioFilter(rep.data);
      $scope.audioFormat = rep.data.audioFormat;
      $scope.infos = rep.data;
    }, function (error) {
      $scope.onInfos = false;
      $scope.onInfosLoading = false;
      console.error(error);
      toastr.error(error.statusText, "Error " + error.status);
    });
  };
  $scope.onChangeUrl = function (form) {
    $scope.onInfos = false;
    $scope.onProcessing = false;
    $scope.onInfosLoading = true;

    /*			if($scope.data.status && $scope.data.status=="finished")
    				$scope.onDownload = false;
    */
    form.url.$error.notFound = false;
    if (form.$valid) checkId();
    return;
  };
  $scope.checkWsState = function () {
    if ($scope.ytSocket.readyState === 3) {
      $scope.ytSocket.close();
      $scope.ytSocket = new WebSocket('wss://' + window.location.host + '/ws/videos/');
      while ($scope.ytSocket.readyState !== 1) {
        console.log($scope.ytSocket.readyState);
        /*		        	var p = new Promise(r => setTimeout(r, 250));
        		        	p.then(() => console.log($scope.ytSocket.readyState));
        */
      }
    }
  };

  $scope.runAudio = function (audioFormat) {
    if (Object.keys($scope.queue).length >= MAX_QUEUE) {
      toastr.warning("Quotas limité à " + MAX_QUEUE + " Téléchargements");
      return;
    }
    $scope.ytSocket.send(JSON.stringify({
      'message_type': "download.start",
      'format_type': "audio",
      'format_file': audioFormat,
      'filename': $scope.infos.title,
      "thumbnail_url": $scope.infos.thumbnail,
      "url": $scope.url,
      "url_id": $scope.url_id,
      "website": $scope.website
    }));
    $timeout(reloadVideos, 3500);
    $scope.onProcessing = true;
    $scope.infos.id = $scope.url_id;
  };
  $scope.addAudio = function (file) {
    if (Object.keys($scope.queue).length >= MAX_QUEUE) {
      toastr.warning("Quotas limité à " + MAX_QUEUE + " Téléchargements");
      return;
    }
    $scope.ytSocket.send(JSON.stringify({
      'message_type': "download.start",
      'format_type': "audio",
      'format_file': file.audioFormat,
      'filename': file.title,
      "thumbnail_url": file.thumbnail.url,
      "url": file.url,
      "url_id": file.url_id,
      "website": file.website
    }));
    $timeout(reloadVideos, 2500);
    $scope.onProcessing = true;
    file.download = false;
  };
  $scope.runVideo = function (videoFormat) {
    if (Object.keys($scope.queue).length >= MAX_QUEUE) {
      toastr.warning("Quotas limité à " + MAX_QUEUE + " Téléchargements");
      return;
    }
    if (!videoFormat.format_note && videoFormat.height > 0) videoFormat.format_note = videoFormat.height + "p";
    videoFormat.format_note = videoFormat.format_note ? videoFormat.format_note : "tv";
    videoFormat.ext = videoFormat.ext ? videoFormat.ext : "mp4";
    $scope.ytSocket.send(JSON.stringify({
      'message_type': "download.start",
      'format_type': "video",
      'format_file': videoFormat,
      'filename': $scope.infos.title,
      "thumbnail_url": $scope.infos.thumbnail,
      "url": $scope.url,
      "url_id": $scope.url_id,
      "website": $scope.website
    }));
    $timeout(reloadVideos, 3500);
    $scope.onProcessing = true;
    $scope.infos.id = $scope.url_id;
  };
  $scope.addVideo = function (file) {
    if (Object.keys($scope.queue).length >= MAX_QUEUE) {
      toastr.warning("Quotas limité à " + MAX_QUEUE + " Téléchargements");
      return;
    }
    if (!file.videoFormat.format_note && file.videoFormat.height > 0) file.videoFormat.format_note = file.videoFormat.height + "p";
    file.videoFormat.format_note = file.videoFormat.format_note ? file.videoFormat.format_note : "tv";
    file.videoFormat.ext = file.videoFormat.ext ? file.videoFormat.ext : "mp4";
    $scope.ytSocket.send(JSON.stringify({
      'message_type': "download.start",
      'format_type': "video",
      'format_file': file.videoFormat,
      'filename': file.title,
      "thumbnail_url": file.thumbnail.url,
      "url": file.url,
      "url_id": file.url_id,
      "website": file.website
    }));
    $timeout(reloadVideos, 2500);
    $scope.onProcessing = true;
    file.download = false;
  };
  $scope.downloadURI = function (data) {
    var filename = data.title + "." + data.format_file.ext;
    var uri = data.file_path;
    var link = document.createElement("a");
    link.download = filename;
    link.href = uri;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };
  $scope.downloadVideo = function (format) {
    var uri = format.url;
    var filename = infos.title + "." + format.ext;
    var link = document.createElement("a");
    link.download = filename;
    link.target = "_blank";
    link.href = uri;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };
  $scope.delQueue = function (download_id, data) {
    data.closing = true;
    $scope.ytSocket.send(JSON.stringify({
      'message_type': "queue.del",
      'download_id': download_id
    }));
  };
}]);

/***/ }),

/***/ "./app/resources/js/loginCtrl.js":
/*!***************************************!*\
  !*** ./app/resources/js/loginCtrl.js ***!
  \***************************************/
/***/ (() => {

angular.module("youtubeDownload").controller("loginCtrl", ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {}]);

/***/ }),

/***/ "./app/resources/js/registerCtrl.js":
/*!******************************************!*\
  !*** ./app/resources/js/registerCtrl.js ***!
  \******************************************/
/***/ (() => {

angular.module("youtubeDownload").controller("facialCtrl", ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {}]);

/***/ }),

/***/ "./app/resources/js/statistiqueCtrl.js":
/*!*********************************************!*\
  !*** ./app/resources/js/statistiqueCtrl.js ***!
  \*********************************************/
/***/ (() => {

angular.module("youtubeDownload").controller("statistiqueCtrl", ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {}]);

/***/ }),

/***/ "./app/resources/js/topCtrl.js":
/*!*************************************!*\
  !*** ./app/resources/js/topCtrl.js ***!
  \*************************************/
/***/ (() => {

angular.module("youtubeDownload").controller("topCtrl", ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {
  $scope.onLoading = {
    queue: true,
    top: true,
    list: true
  };
  $scope.queue = {};
  $scope.youtube_ids = [];
  $scope.download = [];
  $scope.topVideos = [];
  $scope.videos = [];
  $scope.ytSocket = new WebSocket('wss://' + window.location.host + '/ws/downloads/');
  $scope.ytSocket.onclose = function (e) {
    $scope.error = 'Videos socket closed unexpectedly';
    console.error(e);
    toastr.error('Videos socket closed unexpectedly', e);
    $timeout(function () {
      window.location.reload();
    }, 5000);
  };
  $scope.ytSocket.onerror = function (e) {
    $scope.error = 'Videos socket closed unexpectedly';
    console.error('Videos socket error');
    console.error(e);
    toastr.error('Videos socket error', e);
  };
  $http({
    method: 'POST',
    url: '/api/getQueue/',
    headers: {
      "X-CSRFToken": sessionStorage.getItem("csrf_token")
    }
  }).then(function successCallBack(response) {
    $scope.onLoading.queue = false;
    response.data.downloads.forEach(function (d) {
      $scope.queue[d.id] = d;
      if ($scope.youtube_ids.indexOf(d.video.youtube_id) == -1) {
        $scope.youtube_ids.push(d.video.youtube_id);
      }
    });
  }, function errorCallback(error) {
    console.error(error);
    toastr.error(error.statusText, "Error " + error.status);
  });
  $http({
    method: 'POST',
    url: '/api/getTop/',
    headers: {
      "X-CSRFToken": sessionStorage.getItem("csrf_token")
    },
    data: {
      'limit ': 3
    }
  }).then(function successCallBack(response) {
    $scope.onLoading.top = false;
    $scope.topVideos = response.data;
  }, function errorCallback(error) {
    console.error(error);
    toastr.error(error.statusText, "Error " + error.status);
  });
  $http({
    method: 'POST',
    url: '/api/getTop/',
    headers: {
      "X-CSRFToken": sessionStorage.getItem("csrf_token")
    },
    data: {
      'limit': 10
    }
  }).then(function successCallBack(response) {
    $scope.onLoading.list = false;
    console.log($scope.onLoading);
    $scope.videos = response.data;
  }, function errorCallback(error) {
    console.error(error);
    toastr.error(error.statusText, "Error " + error.status);
  });
  console.log($scope.onLoading);
  $scope.addVideo = function (video) {
    $http({
      method: 'POST',
      url: '/api/addQueue/',
      headers: {
        "X-CSRFToken": sessionStorage.getItem("csrf_token")
      },
      data: {
        'youtube_id': video.youtube_id,
        'filename': video.title,
        'format_type': 'video'
      }
    }).then(function successCallBack(response) {
      console.log(response);
      video.download = false;
      video.downloaded = true;
      toastr.success('<a href="/">\
					<p class="text-center text-secondary fs-5">' + response.data.video.title + '</a>', '<p class="text-primary fs-5">Add in yours downloads</p>');
      $scope.ytSocket.send(JSON.stringify({
        'message_type': "download.reload",
        'download_id': response.data.id
      }));
    }, function errorCallback(error) {
      console.error(error);
      toastr.error(error.statusText, "Error " + error.status);
    });
  };
  $scope.addAudio = function (video) {
    $http({
      method: 'POST',
      url: '/api/addQueue/',
      headers: {
        "X-CSRFToken": sessionStorage.getItem("csrf_token")
      },
      data: {
        'youtube_id': video.youtube_id,
        'filename': video.title,
        'format_type': 'audio'
      }
    }).then(function successCallBack(response) {
      console.log(response);
      video.download = false;
      video.downloaded = true;
      toastr.success('<a href="/">\
					<p class="text-center text-secondary fs-5">' + response.data.video.title + '</a>', '<p class="text-primary fs-5">Add in yours downloads</p>');
    }, function errorCallback(error) {
      console.error(error);
      toastr.error(error.statusText, "Error " + error.status);
    });
  };
}]);

/***/ }),

/***/ "./app/resources/js/videoCtrl.js":
/*!***************************************!*\
  !*** ./app/resources/js/videoCtrl.js ***!
  \***************************************/
/***/ (() => {

angular.module("youtubeDownload").controller("videoCtrl", ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {
  $scope.queue = {};
  $http({
    method: 'POST',
    url: '/api/getQueue/',
    headers: {
      "X-CSRFToken": sessionStorage.getItem("csrf_token")
    }
  }).then(function successCallBack(response) {
    response.data.downloads.forEach(function (d) {
      $scope.queue[d.id] = d;
    });
  }, function errorCallback(error) {
    console.error(error);
    toastr.error(error.statusText, "Error " + error.status);
  });
}]);

/***/ }),

/***/ "./app/resources/js/vocalCtrl.js":
/*!***************************************!*\
  !*** ./app/resources/js/vocalCtrl.js ***!
  \***************************************/
/***/ (() => {

angular.module("youtubeDownload").controller("vocalCtrl", ['$scope', '$http', '$timeout', function ($scope, $http, $timeout) {}]);

/***/ }),

/***/ "./app/resources/css/style.css":
/*!*************************************!*\
  !*** ./app/resources/css/style.css ***!
  \*************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
// extracted by mini-css-extract-plugin


/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = __webpack_modules__;
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/chunk loaded */
/******/ 	(() => {
/******/ 		var deferred = [];
/******/ 		__webpack_require__.O = (result, chunkIds, fn, priority) => {
/******/ 			if(chunkIds) {
/******/ 				priority = priority || 0;
/******/ 				for(var i = deferred.length; i > 0 && deferred[i - 1][2] > priority; i--) deferred[i] = deferred[i - 1];
/******/ 				deferred[i] = [chunkIds, fn, priority];
/******/ 				return;
/******/ 			}
/******/ 			var notFulfilled = Infinity;
/******/ 			for (var i = 0; i < deferred.length; i++) {
/******/ 				var [chunkIds, fn, priority] = deferred[i];
/******/ 				var fulfilled = true;
/******/ 				for (var j = 0; j < chunkIds.length; j++) {
/******/ 					if ((priority & 1 === 0 || notFulfilled >= priority) && Object.keys(__webpack_require__.O).every((key) => (__webpack_require__.O[key](chunkIds[j])))) {
/******/ 						chunkIds.splice(j--, 1);
/******/ 					} else {
/******/ 						fulfilled = false;
/******/ 						if(priority < notFulfilled) notFulfilled = priority;
/******/ 					}
/******/ 				}
/******/ 				if(fulfilled) {
/******/ 					deferred.splice(i--, 1)
/******/ 					var r = fn();
/******/ 					if (r !== undefined) result = r;
/******/ 				}
/******/ 			}
/******/ 			return result;
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/jsonp chunk loading */
/******/ 	(() => {
/******/ 		// no baseURI
/******/ 		
/******/ 		// object to store loaded and loading chunks
/******/ 		// undefined = chunk not loaded, null = chunk preloaded/prefetched
/******/ 		// [resolve, reject, Promise] = chunk loading, 0 = chunk loaded
/******/ 		var installedChunks = {
/******/ 			"/app": 0,
/******/ 			"app": 0
/******/ 		};
/******/ 		
/******/ 		// no chunk on demand loading
/******/ 		
/******/ 		// no prefetching
/******/ 		
/******/ 		// no preloaded
/******/ 		
/******/ 		// no HMR
/******/ 		
/******/ 		// no HMR manifest
/******/ 		
/******/ 		__webpack_require__.O.j = (chunkId) => (installedChunks[chunkId] === 0);
/******/ 		
/******/ 		// install a JSONP callback for chunk loading
/******/ 		var webpackJsonpCallback = (parentChunkLoadingFunction, data) => {
/******/ 			var [chunkIds, moreModules, runtime] = data;
/******/ 			// add "moreModules" to the modules object,
/******/ 			// then flag all "chunkIds" as loaded and fire callback
/******/ 			var moduleId, chunkId, i = 0;
/******/ 			if(chunkIds.some((id) => (installedChunks[id] !== 0))) {
/******/ 				for(moduleId in moreModules) {
/******/ 					if(__webpack_require__.o(moreModules, moduleId)) {
/******/ 						__webpack_require__.m[moduleId] = moreModules[moduleId];
/******/ 					}
/******/ 				}
/******/ 				if(runtime) var result = runtime(__webpack_require__);
/******/ 			}
/******/ 			if(parentChunkLoadingFunction) parentChunkLoadingFunction(data);
/******/ 			for(;i < chunkIds.length; i++) {
/******/ 				chunkId = chunkIds[i];
/******/ 				if(__webpack_require__.o(installedChunks, chunkId) && installedChunks[chunkId]) {
/******/ 					installedChunks[chunkId][0]();
/******/ 				}
/******/ 				installedChunks[chunkId] = 0;
/******/ 			}
/******/ 			return __webpack_require__.O(result);
/******/ 		}
/******/ 		
/******/ 		var chunkLoadingGlobal = self["webpackChunkyoutube"] = self["webpackChunkyoutube"] || [];
/******/ 		chunkLoadingGlobal.forEach(webpackJsonpCallback.bind(null, 0));
/******/ 		chunkLoadingGlobal.push = webpackJsonpCallback.bind(null, chunkLoadingGlobal.push.bind(chunkLoadingGlobal));
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module depends on other loaded chunks and execution need to be delayed
/******/ 	__webpack_require__.O(undefined, ["app"], () => (__webpack_require__("./app/resources/js/appConfig.js")))
/******/ 	__webpack_require__.O(undefined, ["app"], () => (__webpack_require__("./app/resources/js/homeCtrl.js")))
/******/ 	__webpack_require__.O(undefined, ["app"], () => (__webpack_require__("./app/resources/js/topCtrl.js")))
/******/ 	__webpack_require__.O(undefined, ["app"], () => (__webpack_require__("./app/resources/js/videoCtrl.js")))
/******/ 	__webpack_require__.O(undefined, ["app"], () => (__webpack_require__("./app/resources/js/loginCtrl.js")))
/******/ 	__webpack_require__.O(undefined, ["app"], () => (__webpack_require__("./app/resources/js/registerCtrl.js")))
/******/ 	__webpack_require__.O(undefined, ["app"], () => (__webpack_require__("./app/resources/js/historyCtrl.js")))
/******/ 	__webpack_require__.O(undefined, ["app"], () => (__webpack_require__("./app/resources/js/statistiqueCtrl.js")))
/******/ 	__webpack_require__.O(undefined, ["app"], () => (__webpack_require__("./app/resources/js/facialCtrl.js")))
/******/ 	__webpack_require__.O(undefined, ["app"], () => (__webpack_require__("./app/resources/js/vocalCtrl.js")))
/******/ 	var __webpack_exports__ = __webpack_require__.O(undefined, ["app"], () => (__webpack_require__("./app/resources/css/style.css")))
/******/ 	__webpack_exports__ = __webpack_require__.O(__webpack_exports__);
/******/ 	
/******/ })()
;