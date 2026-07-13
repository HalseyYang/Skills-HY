/* editor.js —— 编辑器主逻辑（C 混合式可视化编辑器）
 * 依赖：serializer.js (HCEditorSerializer)、editor.css
 *
 * 架构：
 *   - 外层文档：编辑器外壳（工具栏/面板/手柄），覆盖原页面
 *   - iframe（固定尺寸）：渲染用户的 PPT/网页，vw/vh 在此正确解析
 *   - 单位换算：iframe 内拖动的 px → 写回 vh/vw（保自适应）
 *
 * 核心状态：state.changes = { 'hc-id': { type, value } }
 *   保存时交给 serializer.applyPatches 增量替换
 */
(function (global) {
  'use strict';

  var DESIGN_W = 1280, DESIGN_H = 720; // 16:9 设计基准（PPT）——同时也是换算 vw/vh 的基准

  var HCEditor = {
    state: {
      originalHtml: '',     // 进入编辑时的原始快照（安全底线）
      taggedHtml: '',       // 打标后的 HTML（编辑基准）
      idMap: {},            // hc-id 映射
      docType: 'ppt',       // 'ppt' | 'webpage'
      currentSlide: 0,
      totalSlides: 1,
      selectedId: null,
      changes: {},          // 改动清单
      history: [],          // 撤销栈：每项是 {id, before, after} 的 DOM 快照引用
      historyIdx: -1,
      fileHandle: null,     // File System Access 句柄
      filename: 'edited',
    },

    /* ════════ 入口 ════════ */

    // autoEnter：页面加载后自动调用，从 #hce-source 的 data-source 读取 base64 编码的原始 PPT
    // base64 存储 100% 可靠，不受 GLSL/script/特殊字符影响
    autoEnter: function (config) {
      var src = document.getElementById('hce-source');
      if (!src) {
        alert('未找到 #hce-source，无法进入编辑');
        return;
      }
      var b64 = src.getAttribute('data-source');
      if (!b64) {
        alert('#hce-source 没有 data-source 数据');
        return;
      }
      // base64 解码 → UTF-8 字符串
      var html = decodeURIComponent(escape(atob(b64)));
      this.state.filename = (config && config.filename) || 'edited';
      this.enter(html);
    },

    enter: function (originalHtml) {
      // 清理可能残留的旧编辑器外壳（重复 enter 时避免叠加）
      var oldRoot = document.querySelector('.hce-root');
      if (oldRoot) oldRoot.remove();
      var oldHandles = document.querySelectorAll('.hce-handle');
      for (var h = 0; h < oldHandles.length; h++) oldHandles[h].remove();
      // 隐藏原始 PPT 的显示（编辑器外壳接管整个视口）
      var src = document.getElementById('hce-source');
      if (src) src.style.display = 'none';

      this.state.originalHtml = originalHtml;
      this.state.docType = this._detectType(originalHtml);
      var r = global.HCEditorSerializer.injectIds(originalHtml);
      this.state.taggedHtml = r.html;
      this.state.idMap = r.idMap;
      this.state.changes = {};
      this.state.history = [];
      this.state.historyIdx = -1;
      this.state.currentSlide = 0;
      this.state.selectedId = null;
      this._renderShell();
      this._renderCanvas();
    },

    _detectType: function (html) {
      return /id\s*=\s*["']deck["']|class\s*=\s*["'][^"']*\bslide\b/.test(html) ? 'ppt' : 'webpage';
    },

    /* ════════ 外壳渲染 ════════ */

    _renderShell: function () {
      var self = this;
      var root = document.querySelector('.hce-root');
      if (!root) {
        root = document.createElement('div');
        root.className = 'hce-root';
        document.body.appendChild(root);
      }
      root.className = 'hce-root active';
      root.innerHTML =
        '<div class="hce-toolbar">' +
          '<div class="hce-page-nav">' +
            '<button id="hce-prev">◀</button>' +
            '<span class="hce-page-info" id="hce-page-info">1 / 1</span>' +
            '<button id="hce-next">▶</button>' +
          '</div>' +
          '<div style="display:flex;align-items:center">' +
            '<span class="hce-filename" id="hce-filename">' + this.state.filename + '</span>' +
            '<span class="hce-status">Ctrl+S 导出 · Ctrl+Z 撤销</span>' +
          '</div>' +
          '<div>' +
            '<button class="hce-btn-preview" id="hce-preview">▶ 全屏预览</button>' +
            '<button class="hce-btn-save" id="hce-save">⬇ 导出纯净版</button>' +
          '</div>' +
        '</div>' +
        '<div class="hce-middle">' +
          '<div class="hce-canvas-wrap">' +
            '<div class="hce-iframe-wrap"><iframe class="hce-iframe" id="hce-iframe"></iframe></div>' +
            '<div class="hce-hint">单击选中 · 双击改字 · 拖本体移位置 · 右侧面板改字号/颜色/尺寸</div>' +
          '</div>' +
          '<div class="hce-panel" id="hce-panel">' +
            '<div class="hce-panel-empty"><span class="icon">✎</span>点击画布中的<br>任意元素开始编辑</div>' +
          '</div>' +
        '</div>';
      document.getElementById('hce-prev').onclick = function () { self._goSlide(-1); };
      document.getElementById('hce-next').onclick = function () { self._goSlide(1); };
      document.getElementById('hce-save').onclick = function () { self.export(); };
      document.getElementById('hce-preview').onclick = function () { self.preview(); };
    },

    _cssPath: function () {
      return 'editor.css';
    },

    /* ════════ 画布渲染（固定 iframe） ════════ */

    _renderCanvas: function () {
      var self = this;
      var iframe = document.getElementById('hce-iframe');
      var isPpt = this.state.docType === 'ppt';
      if (isPpt) {
        // 自适应：算出可用空间，保持 16:9 最大化
        var availW = window.innerWidth - 260 - 80; // 减去面板260 + padding
        var availH = window.innerHeight - 48 - 80; // 减去工具栏48 + padding
        var w = Math.min(availW, availH * 16 / 9);
        var h = w * 9 / 16;
        iframe.width = Math.round(w);
        iframe.height = Math.round(h);
      } else {
        iframe.width = 800;
        iframe.height = 600;
      }
      iframe.srcdoc = this.state.taggedHtml;
      iframe.onload = function () {
        self._setupSlideCount();
        self._freezeForEditing();
        self._injectIframeStyles();
        self._bindSelection();
        self._bindDragMove();
        self._bindHandleResize();
        // 在 iframe 内也绑一份快捷键转发，避免 iframe 抢焦点后外层收不到
        self._bindIframeShortcuts();
        // 存初始快照（撤销的兜底：回到这个状态）
        self.state.baseSnapshot = {
          bodyHtml: self._iframeDoc().body.innerHTML,
          changes: {}
        };
      };
    },

    _setupSlideCount: function () {
      var doc = this._iframeDoc();
      if (this.state.docType === 'ppt') {
        var slides = doc.querySelectorAll('#deck .slide, .slide');
        this.state.totalSlides = slides.length;
      } else {
        this.state.totalSlides = 1;
      }
      this._updatePageInfo();
    },

    _updatePageInfo: function () {
      var info = document.getElementById('hce-page-info');
      if (info) info.textContent = (this.state.currentSlide + 1) + ' / ' + this.state.totalSlides;
      var prev = document.getElementById('hce-prev');
      var next = document.getElementById('hce-next');
      if (prev) prev.disabled = this.state.currentSlide <= 0;
      if (next) next.disabled = this.state.currentSlide >= this.state.totalSlides - 1;
      if (this.state.docType !== 'ppt') {
        var nav = document.querySelector('.hce-page-nav');
        if (nav) nav.style.visibility = 'hidden';
      }
    },

    _freezeForEditing: function () {
      var doc = this._iframeDoc();
      // 锁住 deck 在当前页
      var deck = doc.querySelector('#deck');
      if (deck) {
        deck.style.transition = 'none';
        deck.style.transform = 'translateX(' + (-this.state.currentSlide * 100) + 'vw)';
      }
      // data-anim 元素钉在终态
      var anims = doc.querySelectorAll('[data-anim]');
      for (var i = 0; i < anims.length; i++) {
        anims[i].style.opacity = '1';
        anims[i].style.transform = 'none';
      }
      // 阻止 iframe 内的翻页脚本，但只在「没有编辑文字时」拦——
      // 否则会掐断 contenteditable 的方向键光标移动
      var blocker = doc.createElement('script');
      blocker.textContent =
        'document.addEventListener("keydown",function(e){' +
          'var ae=document.activeElement;' +
          'if(ae && ae.isContentEditable) return;' + // 编辑文字时放行方向键
          'if(["ArrowLeft","ArrowRight","PageUp","PageDown"," "].indexOf(e.key)>=0){e.stopImmediatePropagation();e.preventDefault();}' +
        '},true);';
      doc.body.appendChild(blocker);
    },

    _injectIframeStyles: function () {
      var doc = this._iframeDoc();
      var style = doc.createElement('style');
      style.textContent =
        '.hce-selected{outline:2px dashed #5B7BFF !important;outline-offset:2px;cursor:move}' +
        '.hce-selected[contenteditable=true]{cursor:text !important}';
      doc.head.appendChild(style);
    },

    // iframe 内快捷键转发：避免 iframe 抢焦点后外层收不到 Ctrl+S/Z
    _bindIframeShortcuts: function () {
      var win = this._iframeWin();
      win.addEventListener('keydown', function (e) {
        if (e.ctrlKey && (e.key === 's' || e.key === 'S')) {
          e.preventDefault();
          HCEditor.export();
          return;
        }
        // Ctrl+Z 在编辑文字时让 contenteditable 自己用，不转发
        var ae = win.document.activeElement;
        var editing = ae && ae.isContentEditable;
        if (e.ctrlKey && (e.key === 'z' || e.key === 'Z') && !editing) {
          e.preventDefault();
          if (e.shiftKey) HCEditor.redo(); else HCEditor.undo();
          return;
        }
      });
    },

    _goSlide: function (delta) {
      var n = this.state.currentSlide + delta;
      if (n < 0 || n >= this.state.totalSlides) return;
      this._deselect();
      this.state.currentSlide = n;
      var deck = this._iframeDoc().querySelector('#deck');
      if (deck) deck.style.transform = 'translateX(' + (-n * 100) + 'vw)';
      this._updatePageInfo();
    },

    _iframeDoc: function () {
      return document.getElementById('hce-iframe').contentDocument;
    },
    _iframeWin: function () {
      return document.getElementById('hce-iframe').contentWindow;
    },

    /* ════════ 选中交互 ════════ */

    _bindSelection: function () {
      var self = this;
      var doc = this._iframeDoc();
      doc.addEventListener('click', function (e) {
        // 点空白取消选中
        if (e.target === doc.body || e.target === doc.documentElement) {
          self._deselect();
          return;
        }
        var el = self._closestEditable(e.target);
        if (el) {
          e.preventDefault();
          self._select(el);
        }
      });
      doc.addEventListener('dblclick', function (e) {
        var el = self._closestEditable(e.target);
        if (el) {
          e.preventDefault();
          self._editText(el);
        }
      });
    },

    // 找最近的带 hc-id 的祖先（排除 body/html 等容器，避免选中整页）
    _closestEditable: function (node) {
      var SKIP = { HTML: 1, HEAD: 1, BODY: 1, SCRIPT: 1, STYLE: 1, LINK: 1, META: 1 };
      var el = node;
      while (el && el.nodeType === 1) {
        if (SKIP[el.tagName]) return null;
        var id = el.getAttribute && el.getAttribute('data-hc-id');
        if (id) return el;
        el = el.parentElement;
      }
      return null;
    },

    _editText: function (el) {
      var self = this;
      var doc = this._iframeDoc();
      var beforeText = el.textContent; // 改前文字
      this._select(el);
      el.setAttribute('contenteditable', 'true');
      // 关键：不主动设全选。只 focus，浏览器会把光标自然放在双击位置，
      // 双击默认选中那个词，用户可用方向键移动光标改单个字。
      el.focus();
      var finished = false;
      var finish = function () {
        if (finished) return;
        finished = true;
        el.removeAttribute('contenteditable');
        el.removeEventListener('blur', finish);
        el.removeEventListener('keydown', guardKeys, true);
        var id = el.getAttribute('data-hc-id');
        var newText = el.textContent;
        if (newText !== beforeText) {
          self._recordChange(id, { type: 'text', value: newText });
        }
      };
      // 编辑文字时，拦截可能干扰的按键，让方向键等走原生光标行为
      var guardKeys = function (e) {
        if (e.ctrlKey || e.metaKey) return; // 放行 Ctrl 组合
        e.stopPropagation(); // 阻止冒泡到 iframe 的其他监听
      };
      el.addEventListener('keydown', guardKeys, true);
      el.addEventListener('blur', finish);
    },

    _select: function (el) {
      this._deselect();
      this.state.selectedId = el.getAttribute('data-hc-id');
      el.classList.add('hce-selected');
      this._renderPanel(el);
      this._showHandles(el);
    },

    _deselect: function () {
      if (this.state.selectedId) {
        var prev = this._iframeDoc().querySelector('.hce-selected');
        if (prev) {
          prev.classList.remove('hce-selected');
          prev.removeAttribute('contenteditable');
        }
      }
      this._hideHandles();
      this.state.selectedId = null;
      this._renderEmptyPanel();
    },

    /* ════════ 手柄（8 向） ════════ */

    // 手柄已弃用（改为面板数值+滑动条改尺寸）。保留为空操作，选中只靠虚线框(.hce-selected)。
    _showHandles: function (el) {
      /* no-op：选中反馈由 .hce-selected 虚线框提供 */
    },

    _hideHandles: function () {
      /* no-op */
    },

    /* ════════ 单位换算 ════════ */

    // 换算基准用 iframe 的实际显示尺寸（自适应后可能不是 DESIGN 值）
    _basisW: function () {
      var f = document.getElementById('hce-iframe');
      return f ? (parseFloat(f.width) || DESIGN_W) : DESIGN_W;
    },
    _basisH: function () {
      var f = document.getElementById('hce-iframe');
      return f ? (parseFloat(f.height) || DESIGN_H) : DESIGN_H;
    },
    _pxToVh: function (px) { return Math.round((px / this._basisH() * 100) * 100) / 100; },
    _pxToVw: function (px) { return Math.round((px / this._basisW() * 100) * 100) / 100; },
    _vhToPx: function (vh) { return vh * this._basisH() / 100; },
    _vwToPx: function (vw) { return vw * this._basisW() / 100; },

    /* ════════ 拖拽移动 ════════ */

    _bindDragMove: function () {
      var self = this;
      var win = this._iframeWin();
      var doc = this._iframeDoc();
      var dragging = false, el = null, startX = 0, startY = 0, startMT = 0, startML = 0;

      doc.addEventListener('mousedown', function (e) {
        if (e.target.classList && e.target.classList.contains('hce-handle')) return;
        var selected = doc.querySelector('.hce-selected');
        if (!selected) return;
        if (selected.getAttribute('contenteditable') === 'true') return; // 编辑文字时不拖
        dragging = true;
        el = selected;
        startX = e.clientX; startY = e.clientY;
        var cs = win.getComputedStyle(el);
        startMT = parseFloat(cs.marginTop) || 0;
        startML = parseFloat(cs.marginLeft) || 0;
        e.preventDefault();
      });

      win.addEventListener('mousemove', function (e) {
        if (!dragging) return;
        var dx = e.clientX - startX;
        var dy = e.clientY - startY;
        el.style.marginTop = (startMT + dy) + 'px';
        el.style.marginLeft = (startML + dx) + 'px';
        self._showHandles(el);
        // 只更新数字框（位置字段无滑动条，避免往 range 传带单位字符串报错）
        self._updatePanelField('marginTop', self._pxToVh(startMT + dy));
        self._updatePanelField('marginLeft', self._pxToVw(startML + dx));
      });

      win.addEventListener('mouseup', function () {
        if (!dragging) return;
        dragging = false;
        var id = el.getAttribute('data-hc-id');
        var cs = win.getComputedStyle(el);
        var mt = self._pxToVh(parseFloat(cs.marginTop) || 0);
        var ml = self._pxToVw(parseFloat(cs.marginLeft) || 0);
        self._recordStyleChange(id, 'margin-top', mt + 'vh');
        self._recordStyleChange(id, 'margin-left', ml + 'vw');
      });
    },

    /* ════════ 手柄 resize ════════ */

    // 手柄 resize 已弃用（改为面板数值+滑动条改尺寸）。保留为空方法。
    _bindHandleResize: function () {
      /* no-op */
    },

    /* ════════ 属性面板 C ════════ */

    _renderPanel: function (el) {
      var self = this;
      var cs = this._iframeWin().getComputedStyle(el);
      var isPpt = this.state.docType === 'ppt';
      var getColor = function () {
        var m = cs.color && cs.color.match(/\d+/g);
        if (!m || m.length < 3) return '#000000';
        return '#' + m.slice(0, 3).map(function (n) { return parseInt(n).toString(16).padStart(2, '0'); }).join('');
      };
      var fontWeight = parseInt(cs.fontWeight) || 400;

      // 字段定义：key=面板字段, css=CSS属性, unit=显示单位, rel=换算到相对单位(vh/vw/无),
      //          slider=是否带滑动条, sMin/sMax/sStep=滑动条参数(相对单位范围)
      var F = {
        marginTop:    { css:'marginTop',     unit:isPpt?'vh':'px', rel:isPpt?'vh':'',  slider:false },
        marginLeft:   { css:'marginLeft',    unit:isPpt?'vw':'px', rel:isPpt?'vw':'',  slider:false },
        fontSize:     { css:'fontSize',      unit:isPpt?'vw':'px', rel:isPpt?'vw':'',  slider:true, sMin:1, sMax:15, sStep:0.1 },
        width:        { css:'width',         unit:isPpt?'vw':'px', rel:isPpt?'vw':'',  slider:true, sMin:5, sMax:100, sStep:0.5 },
        height:       { css:'height',        unit:isPpt?'vh':'px', rel:isPpt?'vh':'',  slider:true, sMin:2, sMax:100, sStep:0.5 },
        lineHeight:   { css:'lineHeight',    unit:'',    rel:'',  slider:false },
        letterSpacing:{ css:'letterSpacing', unit:'px',  rel:'',  slider:false }
      };

      // 从 computed style 取值，转成面板显示值(相对单位)
      function dispVal(key) {
        var f = F[key], v = cs[f.css];
        if (!v || v.indexOf('%') >= 0) return '';
        var px = parseFloat(v); if (!px && px !== 0) return '';
        if (f.rel === 'vh') return self._pxToVh(px);
        if (f.rel === 'vw') return self._pxToVw(px);
        return px;
      }
      // 生成一行：label + 数字输入(只数字) + 只读单位 + (可选)滑动条
      function row(key, label) {
        var f = F[key], val = dispVal(key);
        var html = '<div class="hce-panel-row"><label>' + label + '</label><div class="hce-input-group">' +
          '<input type="number" class="hce-input hce-input-num" data-field="' + key + '" data-css="' + f.css + '" data-unit="' + f.unit + '" data-rel="' + (f.rel||'') + '" value="' + val + '" step="any" inputmode="decimal">' +
          '<span class="hce-unit">' + (f.unit || '') + '</span></div></div>';
        if (f.slider) {
          var min = f.sMin, max = f.sMax, step = f.sStep;
          var slidVal = Math.max(min, Math.min(max, parseFloat(val)||min));
          html += '<div class="hce-slider-row"><input type="range" class="hce-slider" data-field="' + key + '" data-css="' + f.css + '" data-unit="' + f.unit + '" data-rel="' + (f.rel||'') + '" min="' + min + '" max="' + max + '" step="' + step + '" value="' + slidVal + '"></div>';
        }
        return html;
      }

      var panel = document.getElementById('hce-panel');
      panel.innerHTML =
        '<div class="hce-panel-selected-tag">&lt;' + el.tagName.toLowerCase() + (el.className && typeof el.className === 'string' ? '.' + el.className.split(/\s+/)[0] : '') + '&gt;</div>' +
        '<div class="hce-panel-title">位置</div>' +
        row('marginTop', '↑ 上下') + row('marginLeft', '← 左右') +
        '<div class="hce-panel-title">文字</div>' +
        row('fontSize', '字号') +
        '<div class="hce-panel-row"><label>字重</label><div class="hce-input-group"><button class="hce-btn-bold ' + (fontWeight >= 700 ? 'active' : '') + '" id="hce-bold">B</button></div></div>' +
        '<div class="hce-panel-row"><label>颜色</label><div class="hce-input-group"><input class="hce-input hce-input-color" data-field="color" type="color" value="' + getColor() + '"></div></div>' +
        row('lineHeight', '行高') + row('letterSpacing', '字间距') +
        '<div class="hce-panel-title">尺寸</div>' +
        row('width', '宽度') + row('height', '高度') +
        '<div class="hce-panel-title">组件</div>' +
        '<div class="hce-panel-row" style="gap:6px">' +
          '<button class="hce-btn-component" data-act="duplicate">复制</button>' +
          '<button class="hce-btn-component danger" data-act="remove">删除</button>' +
        '</div>' +
        '<div class="hce-panel-row" style="gap:6px;margin-top:6px">' +
          '<button class="hce-btn-component" data-act="up">↑ 上移</button>' +
          '<button class="hce-btn-component" data-act="down">↓ 下移</button>' +
        '</div>';
      this._bindPanelInputs(el);
    },

    _bindPanelInputs: function (el) {
      var self = this;
      var id = el.getAttribute('data-hc-id');
      var cssMap = { marginTop:'margin-top', marginLeft:'margin-left', fontSize:'font-size', lineHeight:'line-height', letterSpacing:'letter-spacing', width:'width', height:'height' };

      // 把一个相对单位数值应用到 DOM（转 px），返回保存用的 css 值
      function applyVal(field, num) {
        var inp = document.querySelector('.hce-input-num[data-field="' + field + '"]');
        var rel = inp ? inp.dataset.rel : '';
        var unit = inp ? inp.dataset.unit : 'px';
        var css = inp ? inp.dataset.css : field;
        var px = num;
        if (rel === 'vh') px = self._vhToPx(num);
        else if (rel === 'vw') px = self._vwToPx(num);
        // 应用到 DOM
        if (field === 'width' || field === 'height') el.style.setProperty(css, px + 'px', 'important');
        else if (unit || rel) el.style[css] = px + 'px';
        else el.style[css] = String(num);
        // 记录到 changes（保存用相对单位）
        var realProp = cssMap[field] || field;
        var saveVal;
        if (rel === 'vh') saveVal = self._pxToVh(px) + 'vh';
        else if (rel === 'vw') saveVal = self._pxToVw(px) + 'vw';
        else if (unit) saveVal = px + unit;
        else saveVal = String(num);
        self._recordStyleChange(id, realProp, saveVal);
        self._showHandles(el);
      }

      // 数字输入框：失焦/回车提交 + 上下键微调
      var numInputs = document.querySelectorAll('.hce-input-num');
      for (var i = 0; i < numInputs.length; i++) {
        (function (inp) {
          var field = inp.dataset.field;
          // 回车提交
          inp.addEventListener('keydown', function (e) {
            if (e.key === 'Enter') { e.preventDefault(); inp.blur(); }
            // 上下键微调（Shift 大幅）
            if (e.key === 'ArrowUp' || e.key === 'ArrowDown') {
              e.preventDefault();
              var step;
              if (field === 'lineHeight') step = e.shiftKey ? 0.2 : 0.05;
              else if (field === 'letterSpacing') step = e.shiftKey ? 2 : 0.5;
              else if (field === 'fontSize') step = e.shiftKey ? 0.5 : 0.2;
              else step = e.shiftKey ? 2 : 0.5; // 位置/尺寸
              var cur = parseFloat(inp.value); if (isNaN(cur)) cur = 0;
              var nv = e.key === 'ArrowUp' ? cur + step : cur - step;
              nv = Math.round(nv * 100) / 100;
              inp.value = nv;
              applyVal(field, nv);
              // 同步滑动条
              var sl = document.querySelector('.hce-slider[data-field="' + field + '"]');
              if (sl) sl.value = nv;
            }
          });
          // 失焦提交
          inp.addEventListener('change', function () {
            var num = parseFloat(inp.value);
            if (isNaN(num)) return;
            applyVal(field, num);
            var sl = document.querySelector('.hce-slider[data-field="' + field + '"]');
            if (sl) sl.value = Math.max(parseFloat(sl.min), Math.min(parseFloat(sl.max), num));
          });
        })(numInputs[i]);
      }

      // 滑动条：拖动实时改
      var sliders = document.querySelectorAll('.hce-slider');
      for (var j = 0; j < sliders.length; j++) {
        (function (sl) {
          var field = sl.dataset.field;
          sl.addEventListener('input', function () {
            var num = parseFloat(sl.value);
            var inp = document.querySelector('.hce-input-num[data-field="' + field + '"]');
            if (inp) inp.value = num;
            applyVal(field, num);
          });
          // 滑动结束才记录到 changes（避免拖动中途刷屏式记录）
          sl.addEventListener('change', function () {
            var num = parseFloat(sl.value);
            applyVal(field, num);
          });
        })(sliders[j]);
      }

      // 颜色
      var colorInp = document.querySelector('.hce-input-color');
      if (colorInp) {
        colorInp.addEventListener('change', function () {
          el.style.color = colorInp.value;
          self._recordStyleChange(id, 'color', colorInp.value);
          self._showHandles(el);
        });
      }
      // 加粗
      var boldBtn = document.getElementById('hce-bold');
      if (boldBtn) {
        boldBtn.onclick = function () {
          var cs = self._iframeWin().getComputedStyle(el);
          var cur = parseInt(cs.fontWeight) || 400;
          var nw = cur >= 700 ? '400' : '700';
          el.style.fontWeight = nw;
          boldBtn.classList.toggle('active', nw === '700');
          self._recordStyleChange(id, 'font-weight', nw);
          self._showHandles(el);
        };
      }
      // 组件操作
      var btns = document.querySelectorAll('.hce-btn-component');
      for (var k = 0; k < btns.length; k++) {
        (function (btn) {
          btn.onclick = function () {
            self._componentAction(el, btn.dataset.act);
          };
        })(btns[k]);
      }
    },

    _componentAction: function (el, act) {
      var id = el.getAttribute('data-hc-id');
      if (act === 'duplicate') {
        var clone = el.cloneNode(true);
        // 新元素需要新的 hc-id（保存时 serializer 会处理，这里先标记）
        clone.setAttribute('data-hc-id', 'hc-new-' + Date.now());
        el.parentNode.insertBefore(clone, el.nextSibling);
        this._recordChange(id, { type: 'duplicate' });
        this._select(clone);
      } else if (act === 'remove') {
        this._recordChange(id, { type: 'remove' });
        el.remove();
        this._deselect();
      } else if (act === 'up') {
        if (el.previousElementSibling && el.previousElementSibling.getAttribute('data-hc-id')) {
          this._recordReorder(id, el, 'before', el.previousElementSibling);
          el.parentNode.insertBefore(el, el.previousElementSibling);
          this._showHandles(el);
        }
      } else if (act === 'down') {
        if (el.nextElementSibling && el.nextElementSibling.getAttribute('data-hc-id')) {
          this._recordReorder(id, el, 'after', el.nextElementSibling);
          el.parentNode.insertBefore(el.nextElementSibling, el);
          this._showHandles(el);
        }
      }
    },

    _renderEmptyPanel: function () {
      var panel = document.getElementById('hce-panel');
      if (panel) panel.innerHTML = '<div class="hce-panel-empty"><span class="icon">✎</span>点击画布中的<br>任意元素开始编辑</div>';
    },

    _updatePanelField: function (field, val) {
      var inp = document.querySelector('.hce-input-num[data-field="' + field + '"]');
      if (inp) {
        inp.value = (typeof val === 'number') ? Math.round(val * 100) / 100 : val;
        inp.classList.add('dirty');
      }
      // 同步滑动条
      var sl = document.querySelector('.hce-slider[data-field="' + field + '"]');
      if (sl && typeof val === 'number') {
        sl.value = Math.max(parseFloat(sl.min), Math.min(parseFloat(sl.max), val));
      }
    },

    /* ════════ 改动记录 + 历史栈 ════════ */

    _recordChange: function (id, change) {
      this.state.changes[id] = change;
      this._pushHistory();
    },

    // style 改动：合并到 changes[id].value
    _recordStyleChange: function (id, prop, val) {
      var existing = this.state.changes[id];
      if (!existing || existing.type !== 'style') {
        existing = { type: 'style', value: '' };
        this.state.changes[id] = existing;
      }
      existing.value = global.HCEditorSerializer.mergeStyle(existing.value, prop + ':' + val);
      this._pushHistory();
      this._markInputDirty(prop);
    },


    _markInputDirty: function (prop) {
      var fieldMap = { 'margin-top': 'marginTop', 'margin-left': 'marginLeft', 'font-size': 'fontSize', 'font-weight': 'fontWeight', 'line-height': 'lineHeight', 'letter-spacing': 'letterSpacing', 'width': 'width', 'height': 'height' };
      var field = fieldMap[prop];
      if (field) {
        var inp = document.querySelector('.hce-input[data-field="' + field + '"]');
        if (inp) inp.classList.add('dirty');
      }
    },

    _recordReorder: function (id, el, rel, sibling) {
      var sibId = sibling.getAttribute('data-hc-id');
      this.state.changes['__reorder__' + id] = { type: 'reorder', elHtml: el.outerHTML, sibHtml: sibling.outerHTML, elId: id, sibId: sibId };
      this._pushHistory();
    },

    _pushHistory: function () {
      // 快照方案：每条历史存"操作之后"的完整状态(body HTML + changes 副本)
      // 撤销时回到上一条；最初状态由 enter 时的 baseSnapshot 兜底
      var snapshot = {
        bodyHtml: this._iframeDoc().body.innerHTML,
        changes: JSON.parse(JSON.stringify(this.state.changes))
      };
      // 截断 redo 分支（在中间撤销后再操作，丢弃后面的）
      this.state.history = this.state.history.slice(0, this.state.historyIdx + 1);
      this.state.history.push(snapshot);
      this.state.historyIdx++;
    },

    /* ════════ 保存 + 退出（都基于"清理后的当前 iframe 内容"） ════════ */

    // 取当前 iframe 内容，清理编辑器痕迹，返回完整 HTML 字符串
    _getCleanHtml: function () {
      var doc = this._iframeDoc();
      var clone = doc.documentElement.cloneNode(true);
      var sels = clone.querySelectorAll('.hce-selected');
      for (var i = 0; i < sels.length; i++) {
        sels[i].classList.remove('hce-selected');
        sels[i].removeAttribute('contenteditable');
      }
      var styles = clone.querySelectorAll('style');
      for (var j = 0; j < styles.length; j++) {
        if (styles[j].textContent.indexOf('hce-selected') >= 0) styles[j].remove();
      }
      var scripts = clone.querySelectorAll('script');
      for (var k = 0; k < scripts.length; k++) {
        var txt = scripts[k].textContent;
        // 移除编辑器注入的 blocker 脚本
        if (txt.indexOf('stopImmediatePropagation') >= 0 ||
            txt.indexOf('isContentEditable') >= 0) {
          scripts[k].remove();
          continue;
        }
        // 移除编辑器资源脚本（src 指向 editable-html/assets 的）
        var src = scripts[k].getAttribute('src') || '';
        if (src.indexOf('editable-html/assets/') >= 0) scripts[k].remove();
      }
      // 移除编辑器样式资源（link 指向 editable-html/assets 的）
      var links = clone.querySelectorAll('link');
      for (var n = 0; n < links.length; n++) {
        var href = links[n].getAttribute('href') || '';
        if (href.indexOf('editable-html/assets/') >= 0) links[n].remove();
      }
      var deck = clone.querySelector('#deck');
      if (deck) deck.style.transition = '';
      var tagged = clone.querySelectorAll('[data-hc-id]');
      for (var m = 0; m < tagged.length; m++) tagged[m].removeAttribute('data-hc-id');
      var nav = clone.querySelector('#nav');
      if (nav) nav.innerHTML = '';
      var overview = clone.querySelector('#overview');
      if (overview) overview.remove();
      return '<!DOCTYPE html>\n' + clone.outerHTML;
    },

    // 导出：生成纯净 HTML（无编辑器代码）下载 —— 这是用户最终要用的文件
    export: function () {
      var html = this._getCleanHtml();
      var v = global.HCEditorSerializer.validate(html);
      if (!v.ok) {
        this._toast('导出已取消：' + v.reason + '。建议 Ctrl+Z 撤销后重试。', 'error');
        return false;
      }
      this._download(html);
      this._toast('已导出纯净版 ' + this.state.filename + '-export.html', 'ok');
      return true;
    },

    // 兼容旧调用（Ctrl+S 现在调 export）
    save: function () { return this.export(); },

    _download: function (html) {
      var blob = new Blob([html], { type: 'text/html;charset=utf-8' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = this.state.filename + '-edited.html';
      document.body.appendChild(a);
      a.click();
      a.remove();
    },

    requestFileHandle: function () {
      var self = this;
      if (!global.showOpenFilePicker) {
        this.state.fileHandle = null;
        return Promise.resolve(false);
      }
      return global.showOpenFilePicker({
        types: [{ description: 'HTML', accept: { 'text/html': ['.html', '.htm'] } }]
      }).then(function (handles) {
        self.state.fileHandle = handles[0];
        return handles[0].getFile();
      }).then(function (file) {
        self.state.filename = file.name.replace(/\.html?$/, '');
        var fnEl = document.getElementById('hce-filename');
        if (fnEl) fnEl.textContent = self.state.filename;
        return file.text();
      }).catch(function () { return false; });
    },

    /* ════════ 撤销/重做（快照方案：恢复 body HTML + changes） ════════ */

    undo: function () {
      if (this.state.historyIdx < 0) { this._toast('没有可撤销的操作', 'warn'); return; }
      var snap = this.state.historyIdx === 0
        ? this.state.baseSnapshot  // 撤销到最初
        : this.state.history[this.state.historyIdx - 1]; // 回到上一条
      this.state.historyIdx--;
      this._restoreSnapshot(snap);
      this._toast('已撤销', 'ok');
    },
    redo: function () {
      if (this.state.historyIdx >= this.state.history.length - 1) { this._toast('没有可重做的操作', 'warn'); return; }
      this.state.historyIdx++;
      this._restoreSnapshot(this.state.history[this.state.historyIdx]);
      this._toast('已重做', 'ok');
    },

    // 恢复一个快照：换 body HTML + 换 changes + 重新冻结动画 + 刷新面板
    _restoreSnapshot: function (snap) {
      var selectedId = this.state.selectedId;
      // 换 body 内容（保留 body 的属性，只换 innerHTML）
      this._iframeDoc().body.innerHTML = snap.bodyHtml;
      this.state.changes = JSON.parse(JSON.stringify(snap.changes));
      // 只需重新冻结动画（事件监听绑在 document 上，innerHTML 替换不影响）
      this._refreezeAnims();
      // 重新选中之前选中的元素（如果还在）
      if (selectedId) {
        var el = this._iframeDoc().querySelector('[data-hc-id="' + selectedId + '"]');
        if (el) this._select(el);
        else { this._deselect(); }
      }
    },

    // 只重新钉住 data-anim 元素终态 + 恢复 deck 当前页（不重复注入 blocker 脚本）
    _refreezeAnims: function () {
      var doc = this._iframeDoc();
      var anims = doc.querySelectorAll('[data-anim]');
      for (var i = 0; i < anims.length; i++) {
        anims[i].style.opacity = '1';
        anims[i].style.transform = 'none';
      }
      // 恢复 deck 到当前页（innerHTML 重设后 transform 丢了）
      var deck = doc.querySelector('#deck');
      if (deck) {
        deck.style.transition = 'none';
        deck.style.transform = 'translateX(' + (-this.state.currentSlide * 100) + 'vw)';
      }
    },

    /* ════════ 退出 + toast ════════ */

    // 预览：遮罩式全屏看 PPT 效果，点按钮或 ESC 回编辑
    preview: function () {
      var self = this;
      var cleanHtml = this._getCleanHtml();
      var ov = document.createElement('div');
      ov.id = 'hce-preview';
      ov.style.cssText = 'position:fixed;inset:0;z-index:2147483647;background:#000;display:flex;align-items:center;justify-content:center';
      var ifr = document.createElement('iframe');
      ifr.style.cssText = 'width:100vw;height:100vh;border:0;background:#fff';
      ifr.srcdoc = cleanHtml;
      // 可点击的关闭按钮（不依赖焦点/ESC）
      var closeBtn = document.createElement('button');
      closeBtn.textContent = '✕ 退出预览 (ESC)';
      closeBtn.style.cssText = 'position:fixed;top:16px;right:16px;background:rgba(0,0,0,.75);color:#fff;border:1px solid rgba(255,255,255,.3);padding:8px 16px;border-radius:6px;font-size:14px;font-family:sans-serif;cursor:pointer;z-index:2147483649';
      var closePreview = function () {
        ov.remove();
        document.removeEventListener('keydown', onKey, true);
      };
      closeBtn.onclick = closePreview;
      ov.appendChild(ifr);
      ov.appendChild(closeBtn);
      document.body.appendChild(ov);
      ifr.focus();
      var onKey = function (e) {
        if (e.key === 'Escape') {
          e.preventDefault();
          e.stopPropagation();
          closePreview();
        }
      };
      document.addEventListener('keydown', onKey, true);
      // iframe 内也绑 ESC，并阻止冒泡，防止 PPT 自己的脚本抢 ESC
      ifr.onload = function () {
        try {
          ifr.contentWindow.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
              e.preventDefault();
              e.stopImmediatePropagation();
              closePreview();
            }
          }, true);
        } catch (e2) {}
      };
      self._toast('预览模式 · 点右上角按钮或按 ESC 退出', 'ok');
    },

    exit: function () {
      // 新方案下没有"退出编辑器"的概念。此方法保留为空，避免旧调用报错
    },

    _toast: function (msg, type) {
      var t = document.createElement('div');
      t.className = 'hce-toast ' + (type || 'ok');
      t.textContent = msg;
      document.body.appendChild(t);
      setTimeout(function () { t.remove(); }, 2600);
    },
  };

  /* ════════ 全局快捷键（外层 + iframe 转发，避免焦点问题） ════════ */
  function handleShortcut(e) {
    var active = document.querySelector('.hce-root.active');
    if (!active) return;
    // Ctrl+S 导出
    if (e.ctrlKey && !e.shiftKey && (e.key === 's' || e.key === 'S')) {
      e.preventDefault();
      HCEditor.export();
      return;
    }
    // Ctrl+Z 撤销 / Ctrl+Shift+Z 重做（编辑文字时让 contenteditable 自己用 Ctrl+Z）
    if (e.ctrlKey && (e.key === 'z' || e.key === 'Z')) {
      var ae = document.activeElement;
      var editing = ae && ae.isContentEditable;
      // 检查 iframe 内焦点
      try {
        var ifr = document.getElementById('hce-iframe');
        if (ifr && ifr.contentDocument) {
          var iae = ifr.contentDocument.activeElement;
          if (iae && iae.isContentEditable) editing = true;
        }
      } catch (err) {}
      if (editing) return; // 编辑文字时不拦截，让原生撤销生效
      e.preventDefault();
      if (e.shiftKey) HCEditor.redo(); else HCEditor.undo();
      return;
    }
  }
  document.addEventListener('keydown', handleShortcut);

  global.HCEditor = HCEditor;
})(typeof window !== 'undefined' ? window : this);
