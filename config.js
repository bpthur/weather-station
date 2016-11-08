'use strict';

var config = module.exports = {
  kinesis : {
    region : 'us-east-1'
  },

  producer : {
    stream : 'weather-stream',
    shards : 1,
    waitBetweenDescribeCallsInSeconds : 5
  }
};
