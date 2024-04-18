angular.module("youtubeDownload").controller("topCtrl", ['$scope', '$http', '$timeout', 
	function($scope, $http, $timeout){

		$scope.onLoading = {queue:true, top:true, list:true};

		$scope.queue = {};
		$scope.youtube_ids = [];
		$scope.download = [];

		$scope.topVideos = [];
		$scope.videos = [];


		$scope.ytSocket = new WebSocket(
            'wss://'
            + window.location.host
            + '/ws/downloads/'
        );

        $scope.ytSocket.onclose = (e) => {
        	$scope.error = 'Videos socket closed unexpectedly';
        	console.error(e);
        	toastr.error('Videos socket closed unexpectedly', e);
        	$timeout(() => {window.location.reload()}, 5000);
        };

        $scope.ytSocket.onerror = (e) => {
        	$scope.error = 'Videos socket closed unexpectedly';
            console.error('Videos socket error');
            console.error(e);
            toastr.error('Videos socket error', e)
        };



		$http({
			method: 'POST',
			url:'/api/getQueue/',
			headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
		}).then(function successCallBack(response) {
			$scope.onLoading.queue = false;
			response.data.downloads.forEach((d) => {
				$scope.queue[d.id] = d;
				if($scope.youtube_ids.indexOf(d.video.youtube_id) == -1){
					$scope.youtube_ids.push(d.video.youtube_id)
				}

			})
		}, function errorCallback(error) {
		    console.error(error);
		    toastr.error(error.statusText, "Error "+error.status);
		});


		$http({
			method: 'POST',
			url:'/api/getTop/',
			headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
			data: {'limit ':3}
		}).then(function successCallBack(response) {
			$scope.onLoading.top = false;
			$scope.topVideos = response.data;
		}, function errorCallback(error) {
		    console.error(error);
		    toastr.error(error.statusText, "Error "+error.status);
		});



		$http({
			method: 'POST',
			url:'/api/getTop/',
			headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
			data: {'limit':10}
		}).then(function successCallBack(response) {
			$scope.onLoading.list = false;
			console.log($scope.onLoading);

			$scope.videos = response.data;
		}, function errorCallback(error) {
		    console.error(error);
		    toastr.error(error.statusText, "Error "+error.status);
		});




		console.log($scope.onLoading);


		$scope.addVideo = (video) => {
			$http({
				method: 'POST',
				url:'/api/addQueue/',
				headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
				data:{'youtube_id':video.youtube_id, 'filename':video.title, 'format_type':'video'}
			}).then(function successCallBack(response) {
				console.log(response);
				video.download=false;
				video.downloaded=true;
				toastr.success('<a href="/">\
					<p class="text-center text-secondary fs-5">'+response.data.video.title+'</a>', 
					'<p class="text-primary fs-5">Add in yours downloads</p>');
				$scope.ytSocket.send(JSON.stringify({
					'message_type': "download.reload",
					'download_id': response.data.id
				}));
			}, function errorCallback(error) {
			    console.error(error);
			    toastr.error(error.statusText, "Error "+error.status);
			});
		}


		$scope.addAudio = (video) => {
			$http({
				method: 'POST',
				url:'/api/addQueue/',
				headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
				data:{'youtube_id':video.youtube_id, 'filename':video.title, 'format_type':'audio'}
			}).then(function successCallBack(response) {
				console.log(response);
				video.download=false;
				video.downloaded=true;
				toastr.success('<a href="/">\
					<p class="text-center text-secondary fs-5">'+response.data.video.title+'</a>', 
					'<p class="text-primary fs-5">Add in yours downloads</p>');
			}, function errorCallback(error) {
			    console.error(error);
			    toastr.error(error.statusText, "Error "+error.status);
			});
		}

}]);