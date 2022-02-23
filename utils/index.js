module.exports.log_exec_time = function logTime(func) {
  const wrapper = function () {
    start = Date.now();
    returnValue = func.apply(this, arguments);
    message = `Calculation took ${(Date.now() - start) / 1000} seconds`;
    console.log(message);
    return returnValue
  }
  return wrapper
}