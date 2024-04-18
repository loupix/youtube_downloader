	
angular.module("youtubeDownload").controller("homeCtrl", ['$scope', '$window', '$document', '$http', '$timeout', 
	'$interval', '$filter', 'ngYoutubeEmbedService',
	function($scope, $window, $document, $http, $timeout, $interval, $filter, ngYoutubeEmbedService){

	

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

		$document.on('scroll', function() {
		    // do your things like logging the Y-axis
/*		    console.log($window.scrollY);
*/
		   // or pass this to the scope
		    $scope.$apply(function() {

		    	let elem = $("#next_videos");

		    	let docViewTop = $window.scrollY;
		    	let docViewBottom = docViewTop + $(window).height();

		    	let elemTop = elem.offset().top - elem.height();
		    	let elemBottom = elemTop + elem.height();

		    	if(docViewTop <= elemTop && docViewBottom >= elemBottom && $scope.videos['next'].length>0) $scope.nextVideos();

		    })
		});



/*		$scope.$watch(function () {
    	return $window.scrollY;
		}, function (scrollY) {
		    console.log(scrollY);
		});*/



		const checkitem = () => {
		  let $this;
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







		$scope.website="youtube";
		$scope.website_patterns={
			'youtube':"https://www.youtube.com/watch?v=........",
			'dailymotion':"https://www.dailymotion.com/video/....",
			'vimeo':"https://vimeo.com/..........",
			'facebook':"http://www.facebook.com/v/..............",
			'instagram':"https://www.instagram.com/reel/..........",
			'odnoklassniki':"https://ok.ru/video/...........",
		};

		const MAX_QUEUE = 6;
		const MAX_RETRIEVE = 6;
		const MAX_RETRIEVE_SEC = 6;

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
		$scope.onQueue = () => {return false;};
		$scope.lenQueue = () => {return Object.keys($scope.queue).length;}

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


		$scope.playerReady = (event) => {
			$scope.onYoutubeLoading = false;
			console.log("playerReady");
			console.log(event);
		}



		$scope.playerStateChanged = (event) => {
			console.log("playerStateChanged");
			console.log(event);
		}









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










		$scope.videos = {'page_number':0, 'number_per_page_base':6, 'number_per_page':6, 'total_page':0, 
			'previous':[], 'current':[], 'next':[], 'next_loading':false, 'prev_loading':false, 'filter_order':'lastDownloaded'}



		$scope.nextVideos = function(){
			if($scope.videos['page_number']+1 > $scope.videos['total_page'])
				return;

			angular.forEach($scope.videos['next'], (video) => {
				$scope.videos['current'].push(video);
			})
			$scope.videos['page_number']++;
			$scope.videos['number_per_page'] += $scope.videos['number_per_page_base'];
			gen_nextVideos();
		};


		$scope.previousVideos = function(){
			if($scope.videos['page_number']-1 < 0)
				return;

			angular.copy($scope.videos['current'], $scope.videos['next']);
			angular.copy($scope.videos['previous'], $scope.videos['current']);
			$scope.videos['page_number']--;
			gen_prevVideos();
		};



		$scope.formatVideoFilter = (video) => {
			angular.forEach(video.formats, (format) => {
				if(!format.format_note && format.height>0)
					format.format_note = format.height+"p";
			});

			let formats = video.formats.filter((f) => {return f.width && f.height})
			if(formats.length==0)
				formats = video.formats.filter((f) => {return f.width && f.height})
			if(formats.length==0)
				formats = video.formats

			angular.forEach(formats, (format) => {
				if(!format.format_note)
					format.format_note = format.format_id;
			})

			formats = formats.sort((a,b) => {
				x = a.quality;y = b.quality;
				return ((x < y) ? -1 : ((x > y) ? 1 : 0));
			});


			let output = [], keys = [];
			angular.forEach(formats, function(item) {
				let key = item.format_note;
				if(keys.indexOf(key) === -1) {
					keys.push(key);
					output.push(item);
				}
			});
			video.videoFormat = output[Math.floor(output.length/2)];
			return output;
		}



		$scope.formatAudioFilter = (audio) => {
			let formats = audio.formats.filter((f) => {return f.format_note=="tiny"})
			formats = formats.sort((a,b) => {
				x = a.quality;y = b.quality;
				return ((x < y) ? -1 : ((x > y) ? 1 : 0));
			});

			audio.audioFormat = formats[Math.floor(formats.length/2)];
			return formats;
		}



		const loadVideos = () => {
			$http({
			    method: 'POST',
			    url: '/api/videos/videos/',
			    responseType:'json',
			    headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
			    data: {'page_number':$scope.videos['page_number'],
			    	'number_per_page':$scope.videos['number_per_page'],
			    	'filter_order':$scope.videos['filter_order']}
			}).then(function successCallBack(response) {
				let rep = response.data;
				$scope.videos['total_page'] = rep.total_page;
				$scope.videos['page_number'] = rep.page_number;
				$scope.videos['current'] = rep.data;
				gen_nextVideos();
				if(rep.data.length>0)
					$scope.videoPlay = rep.data[0]
				$scope.onVideosLoading = false;
				$scope.onFirstLoading = false;
			}, function errorCallback(error) {
			    console.error(error);
			    toastr.error(error.statusText, "Error "+error.status);
			});


		}
		loadVideos();
		$scope.loadVideos = loadVideos;



		const reloadVideos = () => {
			$http({
			    method: 'POST',
			    url: '/api/videos/videos/',
			    responseType:'json',
			    headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
			    data: {'page_number':0,
			    	'number_per_page':$scope.videos['number_per_page'],
			    	'filter_order':$scope.videos['filter_order'],}
			}).then(function successCallBack(response) {
				let rep = response.data;
				$scope.videos['total_page'] = rep.total_page;
				$scope.videos['current'] = rep.data;
				gen_nextVideos();
				if(rep.data.length>0)
					$scope.videoPlay = rep.data[0]
				$scope.onVideosLoading = false;
			}, function errorCallback(error) {
			    console.error(error);
			    toastr.error(error.statusText, "Error "+error.status);
			});
		}






		const gen_nextVideos = function(){
			if($scope.videos['page_number']+1 > $scope.videos['total_page']){
				$scope.videos['next'] = [];
				return;
			}

			$scope.videos.next_loading = true;

			$http({
			    method: 'POST',
			    url: '/api/videos/videos/',
			    responseType:'json',
			    headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
			    data: {'page_number':$scope.videos['page_number']+1,
			    	'number_per_page':$scope.videos['number_per_page_base'],
			    	'filter_order':$scope.videos['filter_order']}
			}).then(function successCallBack(response) {
				let rep = response.data;
				$scope.videos['next'] = rep.data;
				$scope.videos.next_loading = false;
			}, function errorCallback(error) {
			    console.error(error);
			    toastr.error(error.statusText, "Error "+error.status);
			});
		}





		const gen_prevVideos = function(){
			if($scope.videos['page_number']-1 < 0){
				$scope.videos['previous'] = [];
				return;
			}

			$http({
			    method: 'POST',
			    url: '/api/videos/videos/',
			    responseType:'json',
			    headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
			    data: {'page_number':$scope.videos['page_number']-1,
			    	'number_per_page':$scope.videos['number_per_page_base'],
			    	'filter_order':$scope.videos['filter_order']}
			}).then(function successCallBack(response) {
				let rep = response.data;
				$scope.videos['previous'] = rep.data
			}, function errorCallback(error) {
			    console.error(error);
			    toastr.error(error.statusText, "Error "+error.status);
			});
		}







		$scope.showVideo = (video) => {
			$scope.videoPlay = video;
			modalVideo.show();
		}


/*		const clickToastr = (msg) => {
			console.log(msg);
		}

		toastr.options.onclick = (e) => {
			console.log(this);
		}

		toastr.info("voila","title", {"data":{"message":"coucou"}});*/















	/***********DOWNLOADER FINALE AJAX***********/




		const prepareBlob = (data) => {
			let filename = $filter("trusted")(data.filename)+"."+data.format_file.ext;
			$scope.queue[data.download_id]['download'] = true;
			$http.get(data.file_path, {
			    responseType: "arraybuffer"
			}).then(function (response) {
				if(!$scope.queue[data.download_id]) return;
					$scope.queue[data.download_id]['download'] = false;
			    $scope.filedata = response.data;

			    let headers = response.headers(); 
			    headers['Content-Disposition'] = "attachment";
			    let blob = new Blob([response.data], { type: "octet/stream" });
			    let link = document.createElement('a');
			    link.href = window.URL.createObjectURL(blob);
			    link.id = data.download_id;
			    link.download = filename;
			    document.body.appendChild(link);

			    $scope.queue[data.download_id]['status'] = "finished"

			}, (error) => {
				$scope.queue[data.download_id]['download'] = false;
				console.error(error);
			  toastr.error(error.statusText, "Error "+error.status);
			}); 
		}



		$scope.download = (data) => {
			let link = document.getElementById(data.download_id);
			link.click();
		}

















/***********WEB SOCKETS***********/








		let proto = "wss://"
		if(window.location.protocol=="http:")
			proto = "ws://";

		$scope.ytSocket = new WebSocket(
            proto
            + window.location.host
            + '/ws/downloads/'
        );


		$scope.ytSocket.onmessage = (e) => {
            data = JSON.parse(e.data);
/*            console.log(data.message_type)
            console.log(data)
*/            if(data.message_type == "queue.get"){
            	if(data.downloading.length>0)
            		$scope.onLoadQueue = true;
            	else
            		$scope.onLoadQueue = false;
            	angular.forEach(data.downloading, (down) => {
            		$scope.queue[down.id] = {
            			filename: down.filename,
            			thumbnail: down.thumbnail,
            			url_id: down.url_id,
            			_percent_str: down.percent+"%",
            			_percent_float: down.percent,
            		};

            		$scope.ytSocket.send(JSON.stringify({
									'message_type': "download.reload",
									'download_id': down.id
								}));
							})
            }


            if(data.message_type == "queue.del")
            	$scope.$apply((event) =>{
            		let link = document.getElementById(data.download_id);
            		if(link) document.body.removeChild(link);
            		if($scope.queue[data.download_id])
            			delete $scope.queue[data.download_id]

            		if($scope.queue.length>0)
	            		$scope.onLoadQueue = true;
	            	else
	            		$scope.onLoadQueue = false;

            	});
           	

            

            if(data.message_type == "download.started")
	            $scope.$apply((event) =>{
	            	$scope.url = "";
            		$scope.onProcessing=false;
            		$scope.onInfos=false;
            		$scope.onInfosLoading=true;
            		$scope.queue[data.download_id] = {
          					_percent_str: "0.00 %",
          					_percent_float: 0
          				}

            		$scope.queue[data.download_id] = data;
            		$scope.queue[data.download_id]['download'] = false;

            		toastr.info("Téléchargement débuté.", data.filename)
	            });


            if(data.message_type == "download.debug")
            	$scope.$apply((event) =>{
            		if(data.download_id !== undefined){
            			if(!$scope.queue[data.download_id])
            				$scope.queue[data.download_id] = {
            					_percent_str: "0.00 %",
            					_percent_float: 0
            				}

	            		$scope.queue[data.download_id] = data;
	            		$scope.queue[data.download_id]['download'] = false;

	            		if(data.status=="finished"){
	            			$scope.queue[data.download_id]['status'] = "prepare";
	            			prepareBlob(data);
	            		}

            		}
            	});

           if(data.message_type == "download.progress")
	            $scope.$apply((event) =>{
	            	if(data.downloaded_bytes == data.total_bytes){
	            		$scope.queue[data.download_id]['status'] = "prepare";
	            		prepareBlob(data);
	            		return;
	            	}
            		if(data.download_id !== undefined)
	            		$scope.queue[data.download_id] = data;
	            });

	          if(data.message_type == "download.warning")
	            $scope.$apply((event) =>{
	            	console.error("download.warning");
	            	console.error(data);
	            	toastr.warning(data.content, "Warning");
            		if(data.download_id !== undefined)
	            		$scope.queue[data.download_id]['error'] = false;
	            		$scope.queue[data.download_id]['warning'] = true;
	            		$scope.queue[data.download_id]['content'] = data.content;
	            });

	          if(data.message_type == "download.error")
	            $scope.$apply((event) =>{
	            	console.error("download.error");
	            	console.error(data);
	            	toastr.warning(data.content, "Error");
            		if(data.download_id !== undefined){
	            		$scope.queue[data.download_id]['error'] = true;
	            		$scope.queue[data.download_id]['warning'] = false;
	            		$scope.queue[data.download_id]['nbRetrieve'] = MAX_RETRIEVE;
	            		$scope.queue[data.download_id]['content'] = data.content;

	            		let down_id = data.download_id

	            		$interval(() => {
	            			if(!$scope.queue[down_id])
	            				return;

	            			if($scope.queue[down_id]['nbRetrieve']>0)
		            			$scope.queue[down_id]['nbRetrieve']--;
	            			else{
	            				$scope.ytSocket.send(JSON.stringify({
												'message_type': "download.reload",
												'download_id': down_id
											}));
	            			}
	            		}, 1000, MAX_RETRIEVE+1);
	            	}

	            });

	          if(data.message_type == "download.finished")
	            $scope.$apply((event) =>{
	            	console.log("download.finished")
	            	console.log(data)
	            	if(data.download_id !== undefined)
	            		$scope.queue[data.download_id] = data;
	            });



        };

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

        // La connexion est ouverte
		$scope.ytSocket.addEventListener('open', (event) => {
			console.log('Videos socket opened');
			$scope.ytSocket.send(JSON.stringify({'message_type':"queue.get"}));
			return;
		});





















/******************PATTERNS DOWNLOADS******************/










		let youtubePattern = /^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$/
		let dailyPattern = /^(?:https?:\/\/)?(?:www\.)?dailymotion.com\/(video|hub)+(\/([^_]+))?[^#]*(#‎video=([^_&]+))?$/
		let vimeoPattern =	/|^(?:https?:\/\/)?(?:www\.)?vimeo.com\/([0-9]+)$/
		let instaPattern =	/|^(?:https?:\/\/)?(?:www\.)?instagram.com\/reel\/([^_&]+)$/
		let okruPattern =	/|^(?:https?:\/\/)?(?:www\.)?ok.ru\/video\/([0-9]+)$/
		$scope.pattern = youtubePattern + "|" + dailyPattern + "|" 
		$scope.pattern += vimeoPattern+ "|" + instaPattern+ "|" + okruPattern;



		$scope.patterns = {
			'youtube':/youtu(?:.*\/v\/|.*v\=|\.be\/)([A-Za-z0-9_\-]{11})/,
			'dailymotion':/^.+dailymotion.com\/(?:video|swf\/video|embed\/video|hub|swf)\/([A-Za-z0-9_\-]+)/,
			'vimeo':/vimeo.com\/([0-9]*)/i,
			'facebook':/^.+facebook.com\/v\/(.*)/,
			'instagram':/^.+instagram.com\/reel\/([A-Za-z0-9_\-]*)/,
			'odnoklassniki':/^.+ok.ru\/video\/([0-9]*)/,
		}


		$scope.submitForm = (form) => {
			console.log("submit")
			console.log(form.url.$valid)
		};



		const checkDomain = () => {
			let domain = $scope.website;
			angular.forEach(['youtube','dailymotion','vimeo','instagram','odnoklassniki'], (name) =>{
				let pattern = $scope.patterns[name];
				if($scope.url.match(pattern) && $scope.url.match(pattern).length > 1)
					domain = name;
			});
			if(domain != $scope.website) $scope.website = domain;

			let first = ['youtube','dailymotion','vimeo'];
			let second = ['facebook','instagram','odnoklassniki'];

			let carousel_website = document.querySelector('#carousel_website');
			let carousel = new bootstrap.Carousel(carousel_website);

			let index = $('#carousel_website').find('.active').index();


			if(first.indexOf(domain) >=0)
				carousel.to(0);
			else if(second.indexOf(domain) >=0)
				carousel.to(1);
			else
				carousel.to(2);

			return domain;
		}

		const checkId = () => {
			checkDomain();
			let pattern = $scope.patterns[$scope.website];
			if($scope.url.match(pattern) && $scope.url.match(pattern).length > 1){
				$scope.onInfosLoading = true;
				$scope.onInfos = true;
				$scope.url_id = $scope.url.match(pattern)[1];
				loadInfos();
			}

		}

		const loadInfos = () => {
			$http({
				method: 'POST',
				url: 'api/videos/infos/',
				responseType:'json',
		    headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
		    data: {'url':$scope.url, 'website':$scope.website}

			}).then((rep) => {
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
				$scope.videoFormat = rep.data.videoFormat
				rep.data.audioFormats = $scope.formatAudioFilter(rep.data);
				$scope.audioFormat = rep.data.audioFormat

				$scope.infos = rep.data;

			}, (error) => {
				$scope.onInfos = false;
				$scope.onInfosLoading = false;
				console.error(error);
		    toastr.error(error.statusText, "Error "+error.status);
			});
		}

		$scope.onChangeUrl = (form) => {


			$scope.onInfos = false;
			$scope.onProcessing = false;
			$scope.onInfosLoading = true;

/*			if($scope.data.status && $scope.data.status=="finished")
				$scope.onDownload = false;
*/
			form.url.$error.notFound = false;

			if(form.$valid) checkId();

			return
		}


		$scope.checkWsState = () => {
			if ( $scope.ytSocket.readyState === 3 ) {
				$scope.ytSocket.close();
				$scope.ytSocket = new WebSocket(
		            'wss://'
		            + window.location.host
		            + '/ws/videos/'
		        );
		        while ($scope.ytSocket.readyState !== 1) {
		        	console.log($scope.ytSocket.readyState);
/*		        	var p = new Promise(r => setTimeout(r, 250));
		        	p.then(() => console.log($scope.ytSocket.readyState));
*/		        }
		    }
		}


		$scope.runAudio = (audioFormat) => {

			if(Object.keys($scope.queue).length>=MAX_QUEUE){
				toastr.warning("Quotas limité à "+MAX_QUEUE+" Téléchargements");
				return;
			}

			$scope.ytSocket.send(JSON.stringify({
				'message_type': "download.start",
				'format_type': "audio",
				'format_file': audioFormat,
				'filename': $scope.infos.title,
				"thumbnail_url":$scope.infos.thumbnail,
				"url": $scope.url,
				"url_id": $scope.url_id,
				"website": $scope.website,
			}));
			$timeout(reloadVideos, 3500);
			$scope.onProcessing=true;
			$scope.infos.id = $scope.url_id;
		}



		$scope.addAudio = (file) => {

			if(Object.keys($scope.queue).length>=MAX_QUEUE){
				toastr.warning("Quotas limité à "+MAX_QUEUE+" Téléchargements");
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
			$scope.onProcessing=true;
			file.download=false;
		}


		$scope.runVideo = (videoFormat) => {

			if(Object.keys($scope.queue).length>=MAX_QUEUE){
				toastr.warning("Quotas limité à "+MAX_QUEUE+" Téléchargements");
				return;
			}

			if(!videoFormat.format_note && videoFormat.height>0)
				videoFormat.format_note = videoFormat.height+"p";

			videoFormat.format_note = videoFormat.format_note ? videoFormat.format_note : "tv";
			videoFormat.ext = videoFormat.ext ? videoFormat.ext : "mp4";
			$scope.ytSocket.send(JSON.stringify({
				'message_type': "download.start",
				'format_type': "video",
				'format_file': videoFormat,
				'filename': $scope.infos.title,
				"thumbnail_url":$scope.infos.thumbnail,
				"url": $scope.url,
				"url_id": $scope.url_id,
				"website": $scope.website,
			}));
			$timeout(reloadVideos, 3500);
			$scope.onProcessing=true;
			$scope.infos.id = $scope.url_id;
		}


		$scope.addVideo = (file) => {

			if(Object.keys($scope.queue).length>=MAX_QUEUE){
				toastr.warning("Quotas limité à "+MAX_QUEUE+" Téléchargements");
				return;
			}

			if(!file.videoFormat.format_note && file.videoFormat.height>0)
				file.videoFormat.format_note = file.videoFormat.height+"p";

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
			$scope.onProcessing=true;
			file.download=false;
		}











		$scope.downloadURI = (data) => {
			let filename = data.title+"."+data.format_file.ext;
			let uri = data.file_path;
			let link = document.createElement("a");
			link.download = filename;
			link.href = uri;
			document.body.appendChild(link);
			link.click();
			document.body.removeChild(link);
		}








		$scope.downloadVideo = (format) => {
			let uri = format.url;
			let filename = infos.title+"."+format.ext;
			let link = document.createElement("a");
			link.download = filename;
			link.target="_blank";
			link.href = uri;
			document.body.appendChild(link);
			link.click();
			document.body.removeChild(link);
		}





		$scope.delQueue = (download_id, data) => {
			data.closing=true;
			$scope.ytSocket.send(JSON.stringify({
				'message_type': "queue.del",
				'download_id': download_id
			}));
		}


}]);