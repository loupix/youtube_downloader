angular.module("youtubeDownload").controller("videoCtrl", ['$scope', '$http', '$timeout', 
	function($scope, $http, $timeout){


		$scope.queue = {};


		$http({
			method: 'POST',
			url:'/api/getQueue/',
			headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
		}).then(function successCallBack(response) {
			response.data.downloads.forEach((d) => {
				$scope.queue[d.id] = d;
			})
		}, function errorCallback(error) {
		    console.error(error);
		    toastr.error(error.statusText, "Error "+error.status);
		});

}]);