(function() {

	'use strict';

	angular.module('WordFrequencyApp', [])
	
	.controller('WordFrequencyController', [
		'$scope',
		'$log',
		'$http',
		'$timeout',
		function($scope, $log, $http, $timeout) {
			$scope.getResults = function() {
				var userInput = $scope.input_url;

				$http.post('/start', {'url': userInput})
				.success(function(results) {
					$log.info(results);
					getWordCount(results);
				}).error(function(error) {
					$log.error(error);
				});

				function getWordCount(jobId) {
					var timeout = '';
					var pooler = function() {
						$http.get('/results/' + jobId)
						.success(function(data, status) {
							if (status === 202) {
								$log.info(data, status);
							} else if (status === 200) {
								$log.info(data);
								$scope.wordcounts = data;
								$timeout.cancel(timeout);
								return false;
							}

							timeout = $timeout(pooler, 2000);
						});
					};
					pooler();
				};
			};
		}
	]);

}());
