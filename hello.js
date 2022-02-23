logTime = require('./utils').log_exec_time

const fib = function fib(n) {
  if (n < 2) return n;
  return fib(n - 1) + fib(n - 2);
};

const timedFib = logTime(fib);

const sayHello = function sayHello() {
  console.log(Math.floor(Date.now() / 1000) + ' - Hello world:)');
}

const handleInput = function handleInput(data) {
  n = parseInt(data.toString())
  console.log(`fib(${n}) = ${timedFib(n)}`)
}

process.stdin.on('data', handleInput);
setInterval(sayHello, 3000)