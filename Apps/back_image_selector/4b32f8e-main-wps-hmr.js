webpackHotUpdateimage_selector("main",{

/***/ "./src/demo/App.js":
/*!*************************!*\
  !*** ./src/demo/App.js ***!
  \*************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "./node_modules/react/index.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _lib__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../lib */ "./src/lib/index.js");
/* harmony import */ var react_grid_gallery__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-grid-gallery */ "./node_modules/react-grid-gallery/lib/Gallery.js");
/* harmony import */ var react_grid_gallery__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react_grid_gallery__WEBPACK_IMPORTED_MODULE_2__);
function _typeof(obj) { "@babel/helpers - typeof"; if (typeof Symbol === "function" && typeof Symbol.iterator === "symbol") { _typeof = function _typeof(obj) { return typeof obj; }; } else { _typeof = function _typeof(obj) { return obj && typeof Symbol === "function" && obj.constructor === Symbol && obj !== Symbol.prototype ? "symbol" : typeof obj; }; } return _typeof(obj); }

function _extends() { _extends = Object.assign || function (target) { for (var i = 1; i < arguments.length; i++) { var source = arguments[i]; for (var key in source) { if (Object.prototype.hasOwnProperty.call(source, key)) { target[key] = source[key]; } } } return target; }; return _extends.apply(this, arguments); }

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function"); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, writable: true, configurable: true } }); if (superClass) _setPrototypeOf(subClass, superClass); }

function _setPrototypeOf(o, p) { _setPrototypeOf = Object.setPrototypeOf || function _setPrototypeOf(o, p) { o.__proto__ = p; return o; }; return _setPrototypeOf(o, p); }

function _createSuper(Derived) { var hasNativeReflectConstruct = _isNativeReflectConstruct(); return function _createSuperInternal() { var Super = _getPrototypeOf(Derived), result; if (hasNativeReflectConstruct) { var NewTarget = _getPrototypeOf(this).constructor; result = Reflect.construct(Super, arguments, NewTarget); } else { result = Super.apply(this, arguments); } return _possibleConstructorReturn(this, result); }; }

function _possibleConstructorReturn(self, call) { if (call && (_typeof(call) === "object" || typeof call === "function")) { return call; } return _assertThisInitialized(self); }

function _assertThisInitialized(self) { if (self === void 0) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return self; }

function _isNativeReflectConstruct() { if (typeof Reflect === "undefined" || !Reflect.construct) return false; if (Reflect.construct.sham) return false; if (typeof Proxy === "function") return true; try { Date.prototype.toString.call(Reflect.construct(Date, [], function () {})); return true; } catch (e) { return false; } }

function _getPrototypeOf(o) { _getPrototypeOf = Object.setPrototypeOf ? Object.getPrototypeOf : function _getPrototypeOf(o) { return o.__proto__ || Object.getPrototypeOf(o); }; return _getPrototypeOf(o); }

/* eslint no-magic-numbers: 0 */




var App = /*#__PURE__*/function (_Component) {
  _inherits(App, _Component);

  var _super = _createSuper(App);

  function App() {
    var _this;

    _classCallCheck(this, App);

    _this = _super.call(this);
    _this.state = {
      value: 'teste1'
    };
    _this.setProps = _this.setProps.bind(_assertThisInitialized(_this));
    return _this;
  }

  _createClass(App, [{
    key: "setProps",
    value: function setProps(newProps) {
      this.setState(newProps);
    }
  }, {
    key: "render",
    value: function render() {
      var IMAGES = [{
        src: "https://c2.staticflickr.com/9/8817/28973449265_07e3aa5d2e_b.jpg",
        thumbnail: "https://c2.staticflickr.com/9/8817/28973449265_07e3aa5d2e_n.jpg",
        thumbnailWidth: 320,
        thumbnailHeight: 174,
        isSelected: true,
        caption: "After Rain (Jeshu John - designerspics.com)"
      }, {
        src: "https://c2.staticflickr.com/9/8356/28897120681_3b2c0f43e0_b.jpg",
        thumbnail: "https://c2.staticflickr.com/9/8356/28897120681_3b2c0f43e0_n.jpg",
        thumbnailWidth: 320,
        thumbnailHeight: 212,
        tags: [{
          value: "Ocean",
          title: "Ocean"
        }, {
          value: "People",
          title: "People"
        }],
        caption: "Boats (Jeshu John - designerspics.com)"
      }, {
        src: "https://c4.staticflickr.com/9/8887/28897124891_98c4fdd82b_b.jpg",
        thumbnail: "https://c4.staticflickr.com/9/8887/28897124891_98c4fdd82b_n.jpg",
        thumbnailWidth: 320,
        thumbnailHeight: 212
      }];
      return /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("div", null, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(_lib__WEBPACK_IMPORTED_MODULE_1__["ImageSelector"], _extends({
        setProps: this.setProps
      }, this.state)));
    }
  }]);

  return App;
}(react__WEBPACK_IMPORTED_MODULE_0__["Component"]);

/* harmony default export */ __webpack_exports__["default"] = (App);

/***/ })

})
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9pbWFnZV9zZWxlY3Rvci8uL3NyYy9kZW1vL0FwcC5qcyJdLCJuYW1lcyI6WyJBcHAiLCJzdGF0ZSIsInZhbHVlIiwic2V0UHJvcHMiLCJiaW5kIiwibmV3UHJvcHMiLCJzZXRTdGF0ZSIsIklNQUdFUyIsInNyYyIsInRodW1ibmFpbCIsInRodW1ibmFpbFdpZHRoIiwidGh1bWJuYWlsSGVpZ2h0IiwiaXNTZWxlY3RlZCIsImNhcHRpb24iLCJ0YWdzIiwidGl0bGUiLCJDb21wb25lbnQiXSwibWFwcGluZ3MiOiI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUFBQTtBQUNBO0FBRUE7QUFFQTs7SUFFTUEsRzs7Ozs7QUFFRixpQkFBYztBQUFBOztBQUFBOztBQUNWO0FBQ0EsVUFBS0MsS0FBTCxHQUFhO0FBQ1RDLFdBQUssRUFBRTtBQURFLEtBQWI7QUFHQSxVQUFLQyxRQUFMLEdBQWdCLE1BQUtBLFFBQUwsQ0FBY0MsSUFBZCwrQkFBaEI7QUFMVTtBQU1iOzs7OzZCQUVRQyxRLEVBQVU7QUFDZixXQUFLQyxRQUFMLENBQWNELFFBQWQ7QUFDSDs7OzZCQUVRO0FBQ1QsVUFBTUUsTUFBTSxHQUNkLENBQUM7QUFDRUMsV0FBRyxFQUFFLGlFQURQO0FBRUVDLGlCQUFTLEVBQUUsaUVBRmI7QUFHRUMsc0JBQWMsRUFBRSxHQUhsQjtBQUlFQyx1QkFBZSxFQUFFLEdBSm5CO0FBS0VDLGtCQUFVLEVBQUUsSUFMZDtBQU1FQyxlQUFPLEVBQUU7QUFOWCxPQUFELEVBUUE7QUFDR0wsV0FBRyxFQUFFLGlFQURSO0FBRUdDLGlCQUFTLEVBQUUsaUVBRmQ7QUFHR0Msc0JBQWMsRUFBRSxHQUhuQjtBQUlHQyx1QkFBZSxFQUFFLEdBSnBCO0FBS0dHLFlBQUksRUFBRSxDQUFDO0FBQUNaLGVBQUssRUFBRSxPQUFSO0FBQWlCYSxlQUFLLEVBQUU7QUFBeEIsU0FBRCxFQUFtQztBQUFDYixlQUFLLEVBQUUsUUFBUjtBQUFrQmEsZUFBSyxFQUFFO0FBQXpCLFNBQW5DLENBTFQ7QUFNR0YsZUFBTyxFQUFFO0FBTlosT0FSQSxFQWlCQTtBQUNHTCxXQUFHLEVBQUUsaUVBRFI7QUFFR0MsaUJBQVMsRUFBRSxpRUFGZDtBQUdHQyxzQkFBYyxFQUFFLEdBSG5CO0FBSUdDLHVCQUFlLEVBQUU7QUFKcEIsT0FqQkEsQ0FERTtBQXlCSSwwQkFHSSxxRkFDSSwyREFBQyxrREFBRDtBQUNJLGdCQUFRLEVBQUUsS0FBS1I7QUFEbkIsU0FFUSxLQUFLRixLQUZiLEVBREosQ0FISjtBQVVIOzs7O0VBbERhZSwrQzs7QUFxREhoQixrRUFBZixFIiwiZmlsZSI6IjRiMzJmOGUtbWFpbi13cHMtaG1yLmpzIiwic291cmNlc0NvbnRlbnQiOlsiLyogZXNsaW50IG5vLW1hZ2ljLW51bWJlcnM6IDAgKi9cbmltcG9ydCBSZWFjdCwge0NvbXBvbmVudH0gZnJvbSAncmVhY3QnO1xuXG5pbXBvcnQgeyBJbWFnZVNlbGVjdG9yIH0gZnJvbSAnLi4vbGliJztcblxuaW1wb3J0IHsgR2FsbGVyeX0gZnJvbSAncmVhY3QtZ3JpZC1nYWxsZXJ5JztcblxuY2xhc3MgQXBwIGV4dGVuZHMgQ29tcG9uZW50IHtcblxuICAgIGNvbnN0cnVjdG9yKCkge1xuICAgICAgICBzdXBlcigpO1xuICAgICAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgICAgICAgdmFsdWU6ICd0ZXN0ZTEnXG4gICAgICAgIH07XG4gICAgICAgIHRoaXMuc2V0UHJvcHMgPSB0aGlzLnNldFByb3BzLmJpbmQodGhpcyk7XG4gICAgfVxuXG4gICAgc2V0UHJvcHMobmV3UHJvcHMpIHtcbiAgICAgICAgdGhpcy5zZXRTdGF0ZShuZXdQcm9wcyk7XG4gICAgfVxuXG4gICAgcmVuZGVyKCkge1xuICAgIGNvbnN0IElNQUdFUyA9XG4gIFt7XG4gICAgIHNyYzogXCJodHRwczovL2MyLnN0YXRpY2ZsaWNrci5jb20vOS84ODE3LzI4OTczNDQ5MjY1XzA3ZTNhYTVkMmVfYi5qcGdcIixcbiAgICAgdGh1bWJuYWlsOiBcImh0dHBzOi8vYzIuc3RhdGljZmxpY2tyLmNvbS85Lzg4MTcvMjg5NzM0NDkyNjVfMDdlM2FhNWQyZV9uLmpwZ1wiLFxuICAgICB0aHVtYm5haWxXaWR0aDogMzIwLFxuICAgICB0aHVtYm5haWxIZWlnaHQ6IDE3NCxcbiAgICAgaXNTZWxlY3RlZDogdHJ1ZSxcbiAgICAgY2FwdGlvbjogXCJBZnRlciBSYWluIChKZXNodSBKb2huIC0gZGVzaWduZXJzcGljcy5jb20pXCJcbiAgfSxcbiAge1xuICAgICBzcmM6IFwiaHR0cHM6Ly9jMi5zdGF0aWNmbGlja3IuY29tLzkvODM1Ni8yODg5NzEyMDY4MV8zYjJjMGY0M2UwX2IuanBnXCIsXG4gICAgIHRodW1ibmFpbDogXCJodHRwczovL2MyLnN0YXRpY2ZsaWNrci5jb20vOS84MzU2LzI4ODk3MTIwNjgxXzNiMmMwZjQzZTBfbi5qcGdcIixcbiAgICAgdGh1bWJuYWlsV2lkdGg6IDMyMCxcbiAgICAgdGh1bWJuYWlsSGVpZ2h0OiAyMTIsXG4gICAgIHRhZ3M6IFt7dmFsdWU6IFwiT2NlYW5cIiwgdGl0bGU6IFwiT2NlYW5cIn0sIHt2YWx1ZTogXCJQZW9wbGVcIiwgdGl0bGU6IFwiUGVvcGxlXCJ9XSxcbiAgICAgY2FwdGlvbjogXCJCb2F0cyAoSmVzaHUgSm9obiAtIGRlc2lnbmVyc3BpY3MuY29tKVwiXG4gIH0sXG5cbiAge1xuICAgICBzcmM6IFwiaHR0cHM6Ly9jNC5zdGF0aWNmbGlja3IuY29tLzkvODg4Ny8yODg5NzEyNDg5MV85OGM0ZmRkODJiX2IuanBnXCIsXG4gICAgIHRodW1ibmFpbDogXCJodHRwczovL2M0LnN0YXRpY2ZsaWNrci5jb20vOS84ODg3LzI4ODk3MTI0ODkxXzk4YzRmZGQ4MmJfbi5qcGdcIixcbiAgICAgdGh1bWJuYWlsV2lkdGg6IDMyMCxcbiAgICAgdGh1bWJuYWlsSGVpZ2h0OiAyMTJcbiAgfV1cblxuICAgICAgICByZXR1cm4gKFxuXG5cbiAgICAgICAgICAgIDxkaXY+XG4gICAgICAgICAgICAgICAgPEltYWdlU2VsZWN0b3JcbiAgICAgICAgICAgICAgICAgICAgc2V0UHJvcHM9e3RoaXMuc2V0UHJvcHN9XG4gICAgICAgICAgICAgICAgICAgIHsuLi50aGlzLnN0YXRlfVxuICAgICAgICAgICAgICAgIC8+XG4gICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgKVxuICAgIH1cbn1cblxuZXhwb3J0IGRlZmF1bHQgQXBwO1xuIl0sInNvdXJjZVJvb3QiOiIifQ==