//https://stackoverflow.com/questions/18229022/how-to-show-current-time-in-java$
(function () {
    function checkTime(i) {
        return (i < 10) ? "0" + i : i;
    }

    function startTime() {
        var today = new Date(),
            h = checkTime(today.getHours()),
            m = checkTime(today.getMinutes()),
            s = checkTime(today.getSeconds());
        str = "&thinsp;" + h + ":" + m + ":" + s + "&thinsp;";
        document.getElementById('time').innerHTML = str;
        t = setTimeout(function () {
            startTime()
        }, 500);
    }
    startTime();
})();

