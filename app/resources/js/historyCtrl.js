angular.module("youtubeDownload").controller("historyCtrl", ['$scope', '$http', '$timeout', 
	function($scope, $http, $timeout){


		$scope.downloaded = [];
		$scope.videos = [];
		$scope.number_per_page = 10;
		$scope.page_number = 1;



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
		    url: '/api/getHistory/',
		    responseType:'json',
		    headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
		    data: {'number_per_page': $scope.number_per_page, "page_number": $scope.page_number}
		}).then(function successCallBack(response) {
			$scope.downloaded = response.data;
			$scope.videos = response.data.map((d) => d.video);
		}, function errorCallback(error) {
		    console.error(error);
		    toastr.error(error.statusText, "Error "+error.status);
		});




		$scope.downloading = (pathoffile, filename) => {
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
		        var blob = new Blob([response.data], { type: "octet/stream" });
		        var link = document.createElement('a');
		        link.href = window.URL.createObjectURL(blob); 
		        link.download = filename;
		        document.body.appendChild(link);
		        link.click();
		        document.body.removeChild(link);
		    }); 

		}



}]);