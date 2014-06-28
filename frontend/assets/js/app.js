// Make sure jQuery plays nice with Angular
jQuery.noConflict();

/*
*   UPDATE THIS WITH YOUR INFO!
*   base_url = Base url for the API
*   title = The name you want for the admin panel
*   twitter = The Twitter username for the queue (without the "@")
*/
var config = {
    base_url: "",
    title: "Twitter Queue",
    twitter: ""
}

/*
*   Angular app for the admin panel
*/
var app = angular.module("queueapp", []);

function QueueController($scope, $window, $http) {
    $scope.base_url = config.base_url;
    $scope.title = config.title;
    $scope.twitter = config.twitter;

    $scope.newTweet = "";
    $scope.tweets = [];

    $scope.checkLength = function () {
        if ($scope.newTweet.length > 140) {
            return false;
        }
        return true;
    }

    $scope.submitTweet = function () {
        if ($scope.newTweet.trim() == ""){
            return;
        }
        if ($scope.newTweet.trim().length > 140) {
            jQuery("#warningModal").modal("show");
            return;
        }
        $scope.addTweet();
    }

    $scope.addTweet = function () {
        var tweetText = $scope.urlEncode($scope.newTweet.trim())
        $http.post($scope.base_url+"add?tweet="+tweetText, {}).success(function (response) {
            if (response.tweet) {
                $scope.tweets.push(response.tweet);
                $scope.newTweet = "";
                //jQuery("audio")[0].play();
            }
            else {
                console.log(response);
            }
        }).error(function (error) {
            console.log(error);
        })
    }

    $scope.deleteTweet = function (tweet) {
        var tweets = $scope.tweets;
        $http.delete($scope.base_url+"remove?id="+tweet.id, {}).success(function (response) {
            if (response.tweet) {
                for (var i = 0; i < tweets.length; i++) {
                    if (tweets[i].order == tweet.order) {
                        tweets.splice(i,1);
                        break;
                    }
                }
            }
        })
    }
    $scope.escalateTweet = function (tweet) {
        $http.post($scope.base_url+"move?from=" + tweet.order)
        $scope.getTweets();
    }

    $scope.getFirstTweet = function () {
        var tweets = $scope.tweets;
        var lowest = {id:"-1",content:"",order:"-1"};
        for (var i = 0; i < tweets.length; i++) {
            if (lowest.order == "-1" || Number(tweets[i].order) < Number(lowest.order)) {
                lowest = tweets[i];
            }
        }
        return lowest;
    }

    $scope.getTweets = function () {
        $http.get($scope.base_url+"all").success(function (response) {
            console.log(response);
            $scope.tweets = response.tweets;
        }).error(function (error){
            console.log(error);
        });
    }

    $scope.urlEncode = function (str) {
        return encodeURIComponent(str);
    }

    $scope.getTweets();
}
