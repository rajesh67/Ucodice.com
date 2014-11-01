Elessar
=======

Draggable multiple range sliders
![elessar draggable range demo](demo.gif)

[![browser support](https://ci.testling.com/quarterto/Elessar.png)
](https://ci.testling.com/quarterto/Elessar)

Installation
------------
Elessar is available via npm and Bower, and as [standalone files](/dist):

```
npm install elessar
```
```
bower install elessar
```

Elessar requires [jQuery](http://jquery.com). If you're using npm or Bower, it's installed as part of this step. If not: a) why not? they're pretty sweet, b) download it, and I assume you're just using `<script>` tags, so just add a `<script>` tag.


Using
-----

Elessar exports as a CommonJS (Node) module, an AMD module, or a browser global:
```javascript
var RangeBar = require('elessar');
```
```javascript
require(['elessar'], function(RangeBar) { ... });
```
```html
<script src="path/to/elessar.js"></script>
```

Create a rangebar with `var rangeBar = new RangeBar` then add `rangeBar.$el` to the DOM somewhere.

Options
-------
```javascript
new RangeBar({
  values: [], // array of value pairs; each pair is the min and max of the range it creates
  readonly: false, // whether this bar is read-only
  min: 0, // value at start of bar
  max: 100, // value at end of bar
  valueFormat: function(a) {return a;}, // formats a value on the bar for output
  valueParse: function(a) {return a;}, // parses an output value for the bar
  snap: 0, // clamps range ends to multiples of this value (in bar units)
  minSize: 0, // smallest allowed range (in bar units)
  maxRanges: Infinity, // maximum number of ranges allowed on the bar
  bgMarks: {
    count: 0, // number of value labels to write in the background of the bar
    interval: Infinity, // provide instead of count to specify the space between labels
    label: id // string or function to write as the text of a label. functions are called with normalised values.
  },
  indicator: null, // pass a function(RangeBar, Indicator, Function?) Value to calculate where to put a current indicator, calling the function whenever you want the position to be recalculated
  allowDelete: false, // set to true to enable double-middle-click-to-delete
  deleteTimeout: 5000, // maximum time in ms between middle clicks
  vertical: false, // if true the rangebar is aligned vertically, and given the class elessar-vertical
  bounds: null, // a function that provides an upper or lower bound when a range is being dragged. call with the range that is being moved, should return an object with an upper or lower key
  htmlLabel: false, // if true, range labels are written as html
  allowSwap: true // swap ranges when dragging past
});
```

API
---
### ``.val()``
Returns array of pairs of min and max values of each range.

```javascript
bar.val(); //=> [[0,20], [34,86]]
```

### ``.val(values)``
Updates the ranges in the bar with the values. Returns the bar, for chaining.
```javascript
bar.val([[0,30], [40,68]]); //=> bar: RangeBar
```

### ``.on('changing' function(values, range))``
Event that triggers constantly as the value changes. Useful for reactively triggering things in your UI. Callback is passed the current values of the ranges and the range element that is changing.

### ``.on('change' function(values, range))``
Event that triggers after the user has finished changing a range. Useful for updating a Backbone model. Callback is passed the current values of the ranges and the range element that has changed.

Licence
-------
[MIT](licence.md)

Flattr
------

If Elessar has made your life easier, consider sending me a small donation.

[![Flattr this](https://api.flattr.com/button/flattr-badge-large.png)](https://flattr.com/submit/auto?user_id=quarterto&url=https%3A%2F%2Fgithub.com%2Fquarterto%2FElessar)
