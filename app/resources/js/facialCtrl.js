// NB : Remettre dans l'ordre !!!!


angular.module("youtubeDownload").controller("facialCtrl", ['$scope', '$http', '$interval', 
	function($scope, $http, $interval){
		$scope.tags = []
		$scope.groups = []
		$scope.currentTags = []
		$scope.sequenceTags = {}
		$scope.groupTags = {}


		$scope.currentVideo = null;
		$scope.currentGroup = null;

		$scope.load_videos = true;
		$scope.load_sequences = true;


		const modalGroups = new bootstrap.Modal(document.getElementById('modalGroups'));
		$scope.openModalGroups = () => {return modalGroups.show();}


		$scope.videos = {'page_number':0, 'number_per_page':3, 'total_page':0, 
			'previous':[], 'current':[], 'next':[]}

		$scope.sequences = {'page_number':0, 'number_per_page':6, 'total_page':0, 
			'previous':[], 'current':[], 'next':[]}



		$scope.loadTags = () => {
			$http({
			    method: 'POST',
			    url: '/api/facials/tags/',
			    responseType:'json',
			    headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
			    data: {}
			}).then(function successCallBack(response) {
				$scope.tags = response.data;
			}, function errorCallback(error) {
			    console.error(error);
			    toastr.error(error.statusText, "Error "+error.status);
			});
		};
		$scope.loadTags();



		$scope.loadGroups = () => {
			$http({
			    method: 'POST',
			    url: '/api/facials/groups/',
			    responseType:'json',
			    headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
			    data: {}
			}).then(function successCallBack(response) {
				$scope.groups = response.data;
				if($scope.groups.length>0){
					$scope.currentGroup = $scope.groups[0];
					angular.forEach($scope.groups, (group) =>{
						$scope.groupTags[group.id] = group.tags.map((t) => {return t.value});
					});
				}
			}, function errorCallback(error) {
			    console.error(error);
			    toastr.error(error.statusText, "Error "+error.status);
			});
		};
		$scope.loadGroups();





		$scope.loadVideos = () => {
			$http({
			    method: 'POST',
			    url: '/api/facials/videos/',
			    responseType:'json',
			    headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
			    data: {'page_number':$scope.videos['page_number'],
			    	'number_per_page':$scope.videos['number_per_page'],}
			}).then(function successCallBack(response) {
				let rep = response.data;
				$scope.videos['page_number'] = rep.page_number
				$scope.videos['number_per_page'] = rep.number_per_page
				$scope.videos['total_page'] = rep.total_page
				$scope.videos['current'] = rep.data

				$scope.load_videos = false;
				$scope.gen_nextVideos();
				$scope.currentVideo = rep.data[0];
				$scope.initSequences()

			}, function errorCallback(error) {
			    console.error(error);
			    toastr.error(error.statusText, "Error "+error.status);
			});
		}
		$scope.loadVideos();













		$scope.onSelectTag = function(){
			if($scope.currentTags.indexOf($scope.selectedTag)==-1)
				$scope.currentTags.push($scope.selectedTag);
			$scope.selectedTag = null;
		}



		$scope.onNewTag = (keyEvent) => {
			if (keyEvent.which === 13){

				if($scope.tags.map((t) => {return t.value}).indexOf($scope.selectedTag) >= 0)
					return;


				$http({
				    method: 'POST',
				    url: '/api/facials/tags/new/',
				    responseType:'json',
				    headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
				    data: {"tag_value":$scope.selectedTag}
				}).then(function successCallBack(response) {
					$scope.tags.push(response.data);
					$scope.currentTags.push(response.data.value);
					$scope.selectedTag = null;
				}, function errorCallback(error) {
				    console.error(error);
				    toastr.error(error.statusText, "Error "+error.status);
				});
			}
		};




		$scope.onRemoveTag = (tag) => {
			let idx = $scope.tags.indexOf(tag);
			if(idx == -1)
				return false;

			$http({
			    method: 'POST',
			    url: '/api/facials/tags/remove/',
			    responseType:'json',
			    headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
			    data: {"tag_id":tag.id}
			}).then(function successCallBack(response) {
				$scope.tags.splice(idx, 1);
			}, function errorCallback(error) {
			    console.error(error);
			    toastr.error(error.statusText, "Error "+error.status);
			});
			return true;
		}














		$scope.onSelectGroup = () => {$scope.currentGroup = $scope.selectedGroup;}



		$scope.onNewGroup = (keyEvent) => {
			if (keyEvent.which === 13){

				if($scope.groups.map((g) => {return g.value}).indexOf($scope.selectedGroup) >= 0)
					return;


				$http({
				    method: 'POST',
				    url: '/api/facials/groups/new/',
				    responseType:'json',
				    headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
				    data: {"group_value":$scope.selectedGroup}
				}).then(function successCallBack(response) {
					$scope.groups.push(response.data);
					$scope.currentGroup = response.data;
					$scope.selectedGroup = null;
				}, function errorCallback(error) {
				    console.error(error);
				    toastr.error(error.statusText, "Error "+error.status);
				});
			}
		};



		$scope.onRemoveGroup = (group) => {
			let idx = $scope.groups.indexOf(group);
			if(idx == -1)
				return false;

			if(group.id == $scope.currentGroup.id)
				$scope.currentGroup = null;

			$http({
			    method: 'POST',
			    url: '/api/facials/groups/remove/',
			    responseType:'json',
			    headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
			    data: {"group_id":group.id}
			}).then(function successCallBack(response) {
				$scope.groups.splice(idx, 1);
			}, function errorCallback(error) {
			    console.error(error);
			    toastr.error(error.statusText, "Error "+error.status);
			});
			return true;
		}















		$scope.tagInSequence = (sequence, tag_value) => {
			if($scope.sequenceTags[sequence.id]==undefined)
				return false;
			return $scope.sequenceTags[sequence.id].indexOf(tag_value) >= 0
		}


		$scope.tagInCurrentGroup = (tag) => {
			if($scope.currentGroup==undefined)
				return false;
			return $scope.currentGroup.tags.map((t)=>{return t.value}).indexOf(tag.value) >= 0
		}










		$scope.setTagSequence = (sequence, tag_value) => {
			if($scope.sequenceTags[sequence.id].indexOf(tag_value) >= 0){
				$scope.sequenceTags[sequence.id].splice($scope.sequenceTags[sequence.id].indexOf(tag_value), 1)
				$scope.xhr_delTag(sequence, tag_value);
			}else{
				$scope.sequenceTags[sequence.id].push(tag_value);
				$scope.xhr_addTag(sequence, tag_value);
			}
		}



		$scope.setTagGroup = (tag) => {
			if($scope.currentGroup.tags.map((t)=>{return t.value}).indexOf(tag.value) >= 0){
				$scope.currentGroup.tags.splice($scope.currentGroup.tags.map((t)=>{return t.value}).indexOf(tag.value) , 1)
				$scope.xhr_delGroup($scope.currentGroup, tag.id);
			}else{
				$scope.currentGroup.tags.push(tag);
				$scope.xhr_addGroup($scope.currentGroup, tag.id);
			}
		}



		$scope.setCurrentGroup = (group) => {$scope.currentGroup = group;}
		$scope.isCurrentGroup = (group) => {return $scope.currentGroup == group;}



















		/////////////////////////////////////////
		//////////////  XHR GROUP & TAGS  ///////
		/////////////////////////////////////////





		$scope.xhr_addTag = (sequence, tag_value) => {
			$http({
			    method: 'POST',
			    url: '/api/facials/tags/add/',
			    responseType:'json',
			    headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
			    data: {'sequence_id':sequence.id,"tag_value":tag_value}
			}).then(function successCallBack(response) {
				let rep = response.data;
				

			}, function errorCallback(error) {
			    console.error(error);
			    toastr.error(error.statusText, "Error "+error.status);
			});
		}



		$scope.xhr_delTag = (sequence, tag_value) => {
			$http({
			    method: 'POST',
			    url: '/api/facials/tags/del/',
			    responseType:'json',
			    headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
			    data: {'sequence_id':sequence.id,'tag_value':tag_value}
			}).then(function successCallBack(response) {
				let rep = response.data;
				

			}, function errorCallback(error) {
			    console.error(error);
			    toastr.error(error.statusText, "Error "+error.status);
			});
		}










		$scope.xhr_addGroup = (group, tag_id) => {
			$http({
			    method: 'POST',
			    url: '/api/facials/groups/add/',
			    responseType:'json',
			    headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
			    data: {'group_id':group.id,"tag_id":tag_id}
			}).then(function successCallBack(response) {
				let group = response.data;
				$scope.groupTags[group.id] = group.tags.map((t) => {return t.value});
			}, function errorCallback(error) {
			    console.error(error);
			    toastr.error(error.statusText, "Error "+error.status);
			});
		}



		$scope.xhr_delGroup = (group, tag_id) => {
			$http({
			    method: 'POST',
			    url: '/api/facials/groups/del/',
			    responseType:'json',
			    headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
			    data: {'group_id':group.id,'tag_id':tag_id}
			}).then(function successCallBack(response) {
				let group = response.data;
				$scope.groupTags[group.id] = group.tags.map((t) => {return t.value});
			}, function errorCallback(error) {
			    console.error(error);
			    toastr.error(error.statusText, "Error "+error.status);
			});
		}




















		/////////////////////////////////////////
		//////////////  VIDEOS  /////////////////
		/////////////////////////////////////////














		$scope.setVideo = function(video){
			$scope.sequences = {'page_number':0, 'number_per_page':8, 'total_page':0, 
				'previous':[], 'current':[], 'next':[]}
			$scope.currentTags = [];
			$scope.sequenceTags = {};
			$scope.load_sequences = true;
			$scope.currentVideo = video;
			$scope.initSequences();
		}



		$scope.nextVideos = function(){
			if($scope.videos['page_number']+1 > $scope.videos['total_page'])
				return;

			angular.copy($scope.videos['current'], $scope.videos['previous']);
			angular.copy($scope.videos['next'], $scope.videos['current']);
			$scope.videos['page_number']++;
			$scope.gen_nextVideos();
		};


		$scope.previousVideos = function(){
			if($scope.videos['page_number']-1 < 0)
				return;

			angular.copy($scope.videos['current'], $scope.videos['next']);
			angular.copy($scope.videos['previous'], $scope.videos['current']);
			$scope.videos['page_number']--;
			$scope.gen_prevVideos();
		};



		$scope.removeVideo = (video) => {
			$http({
			    method: 'POST',
			    url: '/api/facials/videos/remove/',
			    responseType:'json',
			    headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
			    data: {'video_id':video.id}
			}).then(function successCallBack(response) {
				let rep = response.data;
				$scope.loadVideos();
			}, function errorCallback(error) {
			    console.error(error);
			    toastr.error(error.statusText, "Error "+error.status);
			});
		}




		$scope.gen_nextVideos = function(){
			if($scope.videos['page_number']+1 > $scope.videos['total_page']){
				$scope.sequences['next'] = [];
				return;
			}

			$http({
			    method: 'POST',
			    url: '/api/facials/videos/',
			    responseType:'json',
			    headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
			    data: {'page_number':$scope.videos['page_number']+1,
			    	'number_per_page':$scope.videos['number_per_page']}
			}).then(function successCallBack(response) {
				let rep = response.data;
				$scope.videos['next'] = rep.data
			}, function errorCallback(error) {
			    console.error(error);
			    toastr.error(error.statusText, "Error "+error.status);
			});
		}





		$scope.gen_prevVideos = function(){
			if($scope.videos['page_number']-1 < 0){
				$scope.videos['previous'] = [];
				return;
			}

			$http({
			    method: 'POST',
			    url: '/api/facials/videos/',
			    responseType:'json',
			    headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
			    data: {'page_number':$scope.videos['page_number']-1,
			    	'number_per_page':$scope.videos['number_per_page']}
			}).then(function successCallBack(response) {
				let rep = response.data;
				$scope.videos['previous'] = rep.data
			}, function errorCallback(error) {
			    console.error(error);
			    toastr.error(error.statusText, "Error "+error.status);
			});
		}





























		/////////////////////////////////////////
		//////////////  SEQUENCES  //////////////
		/////////////////////////////////////////






		$scope.initSequencesTags = () =>{
			angular.forEach($scope.sequences, (listSeq) =>{
				angular.forEach(listSeq, (seq) =>{
					$scope.sequenceTags[seq.id] = seq.tags.map((t) => {return t.value});
					angular.forEach(seq.tags, (tag) => {
						if($scope.currentTags.indexOf(tag.value)==-1)
							$scope.currentTags.push(tag.value)
					}, $scope)
				}, $scope);
			});
		}



		$scope.initHandlerSequences = (sequences) => {
			angular.forEach(sequences, (seq) =>{
				seq.num_seq = 0;
				seq.max_seq = seq.faces.length;
				seq.image_current = seq.faces[0];
				seq.timer_animate = null;
				seq.getNextImage = () => {
					if(seq.num_seq==seq.max_seq)
						seq.num_seq=0;
					else
						seq.num_seq+=1;
					seq.image_current = seq.faces[seq.num_seq];
					return;
				}
				seq.getPrevImage = () => {
					if(seq.num_seq==0)
						seq.num_seq=seq.max_seq;
					else
						seq.num_seq-=1;
					seq.image_current = seq.faces[seq.num_seq];
					return;
				}
				seq.animate = () => {
					seq.timer_animate = $interval(() => {
						seq.getNextImage();
					}, 200);
				}
				seq.stop = () => {
					$interval.cancel(seq.timer_animate);
				}
			});
		}




		$scope.initSequences = function(){
			$http({
			    method: 'POST',
			    url: '/api/facials/sequences/',
			    responseType:'json',
			    headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
			    data: {'video_id':$scope.currentVideo.id,
			    	'page_number':$scope.sequences['page_number'],
			    	'number_per_page':$scope.sequences['number_per_page']}
			}).then(function successCallBack(response) {
				let rep = response.data;
				$scope.sequences['page_number'] = rep.page_number
				$scope.sequences['number_per_page'] = rep.number_per_page
				$scope.sequences['total_page'] = rep.total_page

				$scope.sequences['current'] = rep.data;
				$scope.initHandlerSequences($scope.sequences['current']);
				$scope.initSequencesTags();
				$scope.load_sequences = false;
				$scope.gen_nextSequences();

			}, function errorCallback(error) {
			    console.error(error);
			    toastr.error(error.statusText, "Error "+error.status);
			});
		}




		$scope.nextSequences = function(){
			if($scope.sequences['page_number']+1 > $scope.sequences['total_page'])
				return;

			$scope.initHandlerSequences($scope.sequences['next']);
			angular.copy($scope.sequences['current'], $scope.sequences['previous']);
			angular.copy($scope.sequences['next'], $scope.sequences['current']);
			$scope.initSequencesTags();

			$scope.sequences['page_number']++;
			$scope.gen_nextSequences();
		};


		$scope.previousSequences = function(){
			if($scope.sequences['page_number']-1 < 0)
				return;
			
			$scope.initHandlerSequences($scope.sequences['previous']);
			angular.copy($scope.sequences['current'], $scope.sequences['next']);
			angular.copy($scope.sequences['previous'], $scope.sequences['current']);
			$scope.initSequencesTags();

			$scope.sequences['page_number']--;
			$scope.gen_prevSequences();
		};



		$scope.removeSequence = (sequence) => {
			$http({
			    method: 'POST',
			    url: '/api/facials/sequences/remove/',
			    responseType:'json',
			    headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
			    data: {'sequence_id':sequence.id}
			}).then(function successCallBack(response) {
				let rep = response.data;
				$scope.initSequences();
			}, function errorCallback(error) {
			    console.error(error);
			    toastr.error(error.statusText, "Error "+error.status);
			});
		}



		$scope.gen_nextSequences = function(){
			if($scope.sequences['page_number']+1 > $scope.sequences['total_page']){
				$scope.sequences['next'] = []
				return;
			}

			$http({
			    method: 'POST',
			    url: '/api/facials/sequences/',
			    responseType:'json',
			    headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
			    data: {'video_id':$scope.currentVideo.id,
			    	'page_number':$scope.sequences['page_number']+1,
			    	'number_per_page':$scope.sequences['number_per_page']}
			}).then(function successCallBack(response) {
				let rep = response.data;
				$scope.sequences['next'] = rep.data
				$scope.initSequencesTags();
			}, function errorCallback(error) {
			    console.error(error);
			    toastr.error(error.statusText, "Error "+error.status);
			});
		}





		$scope.gen_prevSequences = function(){
			if($scope.sequences['page_number']-1 < 0){
				$scope.sequences['previous'] = [];
				return;
			}
			
			$http({
			    method: 'POST',
			    url: '/api/facials/sequences/',
			    responseType:'json',
			    headers:{"X-CSRFToken":sessionStorage.getItem("csrf_token")},
			    data: {'video_id':$scope.currentVideo.id,
			    	'page_number':$scope.sequences['page_number']-1,
			    	'number_per_page':$scope.sequences['number_per_page']}
			}).then(function successCallBack(response) {
				let rep = response.data;
				$scope.sequences['previous'] = rep.data
				$scope.initSequencesTags();
			}, function errorCallback(error) {
			    console.error(error);
			    toastr.error(error.statusText, "Error "+error.status);
			});
		}


}]);