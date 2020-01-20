var words = sortByFrequency(["two", "two", "seven", "seven", "seven", "seven", "seven", "seven", "seven", "three", "three", "three", "eight", "eight", "eight", "eight", "eight", "eight", "eight", "eight", "five", "five", "five", "five", "five", "four", "four", "four", "four", "nine", "nine", "nine", "nine", "nine", "nine", "nine", "nine", "nine", "one", "ten", "ten", "ten", "ten", "ten", "ten", "ten", "ten", "ten", "ten", "six", "six", "six", "six", "six", "six"])
    .map(function (d, i) {
        return { text: d, size: -i };
    });

var fontName = "Impact",
    width = 960,
    height = 500;

var cTemp = document.createElement('canvas');
var ctx = cTemp.getContext('2d');
ctx.font = "100px " + fontName;

var fRatio = Math.min(width, height) / ctx.measureText(words[0].text).width;
var fontScale = d3.scaleLinear()
        .domain([
            d3.min(words, function (d) { return d.size; }),
            d3.max(words, function (d) { return d.size; })
        ])
        .range([20, 100 * fRatio / 2]);
var colour = d3.scaleOrdinal(d3.schemeCategory20);

d3.layout.cloud()
    .size([width, height])
    .words(words)
    .rotate(function () { return ~~(Math.random() * 2) * 90; })
    .font(fontName)
    .fontSize(function (d) { return fontScale(d.size) })
    .on("end", draw)
    .start();

function draw(words, bounds) {
    var bWidth = bounds[1].x - bounds[0].x;
    var bHeight = bounds[1].y - bounds[0].y;
    var bMidX = bounds[0].x + bWidth / 2;
    var bMidY = bounds[0].y + bHeight / 2;
    var bDeltaX = width / 2 - bounds[0].x + bWidth / 2;
    var bDeltaY = height / 2 - bounds[0].y + bHeight / 2;
    var bScale = bounds ? Math.min(width / bWidth, height / bHeight) : 1;

    var svg = d3.select(".cloud").append("svg")
        .attr("width", width)
        .attr("height", height);

    svg.append("g")
        .attr("transform", "translate(" + [bWidth >> 1, bHeight >> 1] + ") scale(" + bScale + ")")
        .selectAll("text")
        .data(words)
        .enter().append("text")
        .style("font-size", function (d) { return d.size + "px"; })
        .style("font-family", fontName)
        .style("fill", function (d, i) { return colour(i); })
        .attr("text-anchor", "middle")
        .transition()
        .duration(500)
        .attr("transform", function (d) {
            return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .text(function (d) { return d.text; });
};

function sortByFrequency(arr) {
    var f = {};
    arr.forEach(function (i) { f[i] = 0; });
    var u = arr.filter(function (i) { return ++f[i] === 1; });
    return u.sort(function (a, b) { return f[b] - f[a]; });
}