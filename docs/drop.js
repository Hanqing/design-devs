// 页脚头像掉落：滚到页面底部时，所有人物的头像从天而降，在页脚堆成一堆。
// 思路参考 air.build 的页脚（Matter.js 刚体 + canvas 绘制 + 按住聚集）。
(() => {
  const PEOPLE = [{"h":"emilkowalski","n":"Emil Kowalski"},{"h":"raunofreiberg","n":"Rauno Freiberg"},{"h":"rsms","n":"Rasmus Andersson"},{"h":"_DavidSmith","n":"David Smith（_DavidSmith）"},{"h":"_chenglou","n":"Cheng Lou"},{"h":"adamwathan","n":"Adam Wathan"},{"h":"DTD_STUDIOS","n":"CapWords 团队（DTD）"},{"h":"kepano","n":"Steph Ango（kepano）"},{"h":"lorenb","n":"Loren Brichter"},{"h":"sindresorhus","n":"Sindre Sorhus"},{"h":"andy_matuschak","n":"Andy Matuschak"},{"h":"ChristianSelig","n":"Christian Selig"},{"h":"HiTw93","n":"Tw93"},{"h":"jh3yy","n":"Jhey Tompkins"},{"h":"karrisaarinen","n":"Karri Saarinen"},{"h":"steveruizok","n":"Steve Ruiz"},{"h":"_inside","n":"Guilherme Rambo"},{"h":"antfu7","n":"Anthony Fu（antfu）"},{"h":"chockenberry","n":"Craig Hockenberry"},{"h":"evanyou","n":"尤雨溪（Evan You）"},{"h":"henrikruscon","n":"Henrik Ruscon"},{"h":"jakubkrehel","n":"Jakub Krehel"},{"h":"jasonyuan","n":"Jason Yuan"},{"h":"marcedwards","n":"Marc Edwards"},{"h":"marcoarment","n":"Marco Arment"},{"h":"mattgperry","n":"Matt Perry"},{"h":"mitchellh","n":"Mitchell Hashimoto"},{"h":"pacocoursey","n":"Paco Coursey"},{"h":"shadcn","n":"shadcn"},{"h":"__oQuery","n":"拾一 Innei"},{"h":"benjitaylor","n":"Benji Taylor"},{"h":"ccgus","n":"Gus Mueller（August Mueller）"},{"h":"geoffreylitt","n":"Geoffrey Litt"},{"h":"hwwaanng","n":"Hwang"},{"h":"joshm","n":"Josh Miller"},{"h":"koenbok","n":"Koen Bok"},{"h":"mdo","n":"Mark Otto"},{"h":"mrdoob","n":"Ricardo Cabello（mrdoob）"},{"h":"nateparrott","n":"Nate Parrott"},{"h":"raphaelsalaja","n":"Raphael Salaja"},{"h":"romannurik","n":"Roman Nurik"},{"h":"ryolu_","n":"Ryo Lu"},{"h":"thomaspaulmann","n":"Thomas Paul Mann"},{"h":"argyleink","n":"Adam Argyle"},{"h":"b3ll","n":"Adam Bell"},{"h":"jordibruin","n":"Jordi Bruin"},{"h":"jornvandijk","n":"Jorn van Dijk"},{"h":"joshpuckett","n":"Josh Puckett"},{"h":"liuyi0922","n":"61（柳毅）"},{"h":"nathangitter","n":"Nathan Gitter"},{"h":"Rich_Harris","n":"Rich Harris"},{"h":"shuding","n":"Shu Ding"},{"h":"simonbs","n":"Simon B. Støvring"},{"h":"steveschoger","n":"Steve Schoger"},{"h":"1ittlecup","n":"1ittlecup"},{"h":"devongovett","n":"Devon Govett"},{"h":"hal__lee","n":"Hal Lee"},{"h":"Ibelick","n":"Julien Thibeaut（Ibelick）"},{"h":"jasonfried","n":"Jason Fried"},{"h":"jsngr","n":"Jordan Singer"},{"h":"kevinzhow","n":"Kevin Zhow"},{"h":"liuliu","n":"Liu Liu"},{"h":"maxbrunsfeld","n":"Max Brunsfeld"},{"h":"Megabits_mzq","n":"Megabits（金鱼）"},{"h":"mortenjust","n":"Morten Just"},{"h":"nandafyi","n":"Nanda Syahrasyad（nanda）"},{"h":"nathansobo","n":"Nathan Sobo"},{"h":"plidezus","n":"少楠 Plidezus"},{"h":"samuelkraft","n":"Samuel Kraft"},{"h":"samwhoo","n":"Sam Rose"},{"h":"thaliaeche","n":"Thalia Echevarría Fiol"},{"h":"tualatrix","n":"图拉鼎"},{"h":"Vjeux","n":"Christopher Chedeau（vjeux）"},{"h":"waylybaye","n":"Baye"},{"h":"calebporzio","n":"Caleb Porzio"},{"h":"danielpunkass","n":"Daniel Jalkut"},{"h":"Dimillian","n":"Thomas Ricouard"},{"h":"DIYgod","n":"DIYgod"},{"h":"ianstormtaylor","n":"Ian Storm Taylor"},{"h":"jaffathecake","n":"Jake Archibald"},{"h":"lexrus","n":"Lex Tang"},{"h":"maxvoltar","n":"Tim Van Damme（Max Voltar）"},{"h":"chriscoyier","n":"Chris Coyier"},{"h":"jaywcjlove","n":"小弟调调（王楚江 · Kenny）"},{"h":"jordwalke","n":"Jordan Walke"},{"h":"Lakr233","n":"砍砍 Lakr"},{"h":"mattt","n":"Mattt"},{"h":"onevcat","n":"onevcat 王巍"},{"h":"pqoqubbw","n":"dmytro（pqoqubbw）"},{"h":"rea1DonandTrump","n":"Rene Wang"},{"h":"ryanashcraft","n":"Ryan Wesley（Ryan Ashcraft）"},{"h":"vadimdemedes","n":"Vadim Demedes"},{"h":"xiaolinbythesea","n":"笑林（李笑林）"},{"h":"zenorocha","n":"Zeno Rocha"},{"h":"83dwn","n":"Diff"},{"h":"aidenybai","n":"Aiden Bai"},{"h":"chrisbanes","n":"Chris Banes"},{"h":"DavidKPiano","n":"David Khourshid（David K）"},{"h":"dcurtis","n":"Dustin Curtis"},{"h":"Folke","n":"Folke Lemaitre"},{"h":"Hoenheimer","n":"张子恒"},{"h":"joeyabanks","n":"Joey Banks"},{"h":"mikker","n":"Mikkel Malmberg（mikker）"},{"h":"oldj","n":"oldj（老杰）"},{"h":"randyloop","n":"Randy Lu"},{"h":"sofish","n":"Sofish（林建锋）"},{"h":"vanillaCitron","n":"citron"},{"h":"yisibl","n":"一丝（yisibl）"},{"h":"chriseidhof","n":"Chris Eidhof"},{"h":"fabiospampinato","n":"Fabio Spampinato"},{"h":"joehribar","n":"Joe Hribar"},{"h":"krzyzanowskim","n":"Marcin Krzyżanowski"},{"h":"lukaskubanek","n":"Lukáš Kubánek"},{"h":"mds","n":"Matt D. Smith（MDS）"},{"h":"mjtsai","n":"Michael Tsai"},{"h":"mrncst","n":"Mariana Castilho"},{"h":"nikitabobko","n":"Nikita Bobko"},{"h":"OwenYoungZh","n":"Owen"},{"h":"pfrazee","n":"Paul Frazee"},{"h":"tannerlinsley","n":"Tanner Linsley"},{"h":"tomkrcha","n":"Tom Krcha"},{"h":"x74353","n":"William Gustafson"},{"h":"yiliush","n":"Yiliu"},{"h":"acdlite","n":"Andrew Clark"},{"h":"alexrozanski","n":"Alex Rozanski"},{"h":"bramus","n":"Bramus Van Damme（Bramus）"},{"h":"chenchengpro","n":"陈成（云谦 / sorrycc）"},{"h":"crafty","n":"Nick Butcher"},{"h":"jmitch","n":"Justin Mitchell"},{"h":"JordanMorgan10","n":"Jordan Morgan"},{"h":"mattrothenberg","n":"Matt Rothenberg"},{"h":"poteto","n":"Lauren Tan"},{"h":"samselikoff","n":"Sam Selikoff"},{"h":"twostraws","n":"Paul Hudson"},{"h":"unixzii","n":"Cyandev"},{"h":"yetone","n":"yetone"},{"h":"caiyue5","n":"蔡越 Yue"},{"h":"cloudwu","n":"云风（吴云洋）"},{"h":"danielsaidi","n":"Daniel Saidi"},{"h":"evandinsmore","n":"Evan Dinsmore"},{"h":"mjackson","n":"Michael Jackson（MJ）"},{"h":"nixzhu","n":"NIX"},{"h":"noahsark769","n":"Noah Gilmore"},{"h":"stephancasas","n":"Stephan Casas"},{"h":"delba_oliveira","n":"Delba de Oliveira"},{"h":"harlanhaskins","n":"Harlan Haskins"},{"h":"haxfenx","n":"fenx"},{"h":"Huxpro","n":"黄玄（Xuan Huang · Hux）"},{"h":"jeresig","n":"John Resig"},{"h":"JidanzaiDashan","n":"鸡蛋仔"},{"h":"jonnyburch","n":"Jonny Burch"},{"h":"JourneymanChina","n":"Journeyman"},{"h":"manuel_kehl","n":"Manuel Kehl"},{"h":"mattie","n":"Matt Massicotte"},{"h":"mitsuhiko","n":"Armin Ronacher"},{"h":"mxcl","n":"Max Howell"},{"h":"RyanCarniato","n":"Ryan Carniato"},{"h":"ryanflorence","n":"Ryan Florence"},{"h":"soffes","n":"Sam Soffes"},{"h":"twannl","n":"Antoine van der Lee（SwiftLee）"},{"h":"Una","n":"Una Kravets"},{"h":"anthonyshort","n":"Anthony Short"},{"h":"fatbobman","n":"东坡肘子 Fatbobman"},{"h":"manateelazycat","n":"王勇（Andy Stewart / ManateeLazyCat）"},{"h":"threepointone","n":"Sunil Pai"},{"h":"yihong0618","n":"yihong0618"},{"h":"BHolmesDev","n":"Ben Holmes"},{"h":"DeRyckNth","n":"DeRyck"},{"h":"dingyi","n":"Ding（丁一）"},{"h":"frostming90","n":"Frost Ming（frostming）"},{"h":"G_Z_Y","n":"Shawn Gong"},{"h":"HzaoHzao","n":"Hzao（Zac）"},{"h":"iamcheyan","n":"徹言"},{"h":"lencx_","n":"lencx"},{"h":"mecid","n":"Majid Jabrayilov"},{"h":"nishuang","n":"倪爽"},{"h":"rainyluo","n":"rainyluo"},{"h":"rauchg","n":"Guillermo Rauch"},{"h":"sarunw","n":"Sarun Wongpatcharapakorn（Sarun W.）"},{"h":"simonw","n":"Simon Willison"},{"h":"sonicbluestrats","n":"TED*（Pixegen）"},{"h":"steipete","n":"Peter Steinberger"},{"h":"tdinh_me","n":"Tony Dinh"},{"h":"thdxr","n":"Dax Raad（thdxr）"},{"h":"timneutkens","n":"Tim Neutkens"},{"h":"zacwhite","n":"Zac White"},{"h":"adamlyttleapps","n":"Adam Lyttle"},{"h":"AriesZhou","n":"Aries Zhou"},{"h":"azamsharp","n":"Mohammad Azam（AzamSharp）"},{"h":"dalonng","n":"大桥（姜大龙）"},{"h":"DonnyWals","n":"Donny Wals"},{"h":"kemchenj","n":"Kem Chen（四娘）"},{"h":"miantiao_me","n":"面条（MT）"},{"h":"sanxiaozhizi","n":"三咲智子（Kevin Deng · sxzz）"},{"h":"AcboxLiu","n":"Acbox"},{"h":"JoshHrach","n":"Josh Hrach"},{"h":"JupiterTheWL","n":"术士木星（Jupiter The Warlock）"},{"h":"levelsio","n":"Pieter Levels"},{"h":"mkdir700","n":"Mark（mkdir700）"},{"h":"realWeZZard","n":"WeZZard"},{"h":"robinjdev","n":"RobinJ"},{"h":"owenzhao","n":"肇鑫 Zhao Xin"},{"h":"ThaddeusJiang","n":"TJ（ThaddeusJiang）"},{"h":"ctatedev","n":"Chris Tate"},{"h":"fanjiewang","n":"Frank Wang"},{"h":"frank_uid","n":"Frank"},{"h":"haohailong","n":"郝海龙"},{"h":"imwritingbugs","n":"夕阳针 Duskzhen"},{"h":"isukkaw","n":"Sukka"},{"h":"jayair","n":"Jay"},{"h":"joenrv","n":"Joaquim Vergès"},{"h":"shaoruu","n":"Ian Huang（黄绍儒）"},{"h":"alexyang","n":"Alex Yang（himself65）"},{"h":"ianneo_ai","n":"伊恩 Ian"},{"h":"kelvinmade13","n":"Kelvin"},{"h":"PaulSolt","n":"Paul Solt"},{"h":"sanketsahu","n":"Sanket Sahu"},{"h":"TvWoo","n":"Steve（GOTSTAR）"},{"h":"amlcodes","n":"Alex Lane"},{"h":"ElazerWang","n":"石头 Elazer Wang"},{"h":"m0d8ye","n":"Max Lv"},{"h":"maomao000211","n":"mao mao"},{"h":"mike_chong_zh","n":"迈克 Mike Chong"},{"h":"virushuo","n":"霍炬（virushuo）"},{"h":"withfolyd","n":"Folyd（朱爽）"},{"h":"Barret_China","n":"Barret 李靖（小胡子哥）"},{"h":"bojie_li","n":"李博杰"},{"h":"dannypostma","n":"Danny Postma"},{"h":"istdrc","n":"RC（Richard Chien / stdrc）"},{"h":"jakevin7","n":"卡比卡比"},{"h":"qingnianxiaozhe","n":"青年小哲 Ethan Zhao"},{"h":"rameerez","n":"Javi（rameerez）"},{"h":"songofhawk","n":"蓝星（宋辉）"},{"h":"B1ngsha","n":"冰沙 Cheyne Chen"},{"h":"damonchen","n":"Damon Chen"},{"h":"indie_maker_fox","n":"Fox"},{"h":"karpathy","n":"Andrej Karpathy"},{"h":"lemomo_ai","n":"Lemomo"},{"h":"ninthbit_ai","n":"Kieran Zhang"},{"h":"rudraxx13","n":"Rudra Satani"},{"h":"zhufengme","n":"朱峰"},{"h":"Jimmy_JingLv","n":"吕立青（JimmyLv）"},{"h":"kevinma_dev_zh","n":"Kevin Ma"},{"h":"marclou","n":"Marc Lou"},{"h":"yifanxu_ephai","n":"Yifan Xu"},{"h":"AI_Jasonyu","n":"鱼总"},{"h":"idoubicc","n":"idoubi（艾逗笔）"},{"h":"jiayuan_jy","n":"Jiayuan Zhang"},{"h":"bbruceyuan","n":"袁朝发（Chaofa Yuan）"},{"h":"evilcos","n":"余弦（Cos）"},{"h":"FreiheitYu","n":"余晟（YU）"},{"h":"ivanleomk","n":"Ivan Leo"},{"h":"ring_hyacinth","n":"海辛"},{"h":"shoucccc","n":"Chaofan Shou"},{"h":"sherwinwu","n":"Sherwin Wu"},{"h":"dongxi_nlp","n":"东锡（Dongxi）"},{"h":"dingalingts","n":"dingaling"},{"h":"yourQuantGuy","n":"yourQuantGuy"}];
  const root = document.querySelector('[data-drop]');
  const script = document.currentScript;
  if (!root || !script) return;

  const base = new URL('.', script.src).href;
  const scene = root.querySelector('.drop-scene');
  const canvas = scene.querySelector('canvas');
  const cue = root.querySelector('.drop-cue');
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const current = (location.pathname.match(/\/people\/([^/]+)\//) || [])[1];

  let matter;
  function loadMatter() {
    if (window.Matter) return Promise.resolve(window.Matter);
    matter ||= new Promise((ok, fail) => {
      const s = document.createElement('script');
      s.src = base + 'vendor/matter.min.js';
      s.onload = () => ok(window.Matter);
      s.onerror = fail;
      document.head.append(s);
    });
    return matter;
  }

  // ---------- 贴图 ----------
  const TEX = 128;
  const COLORS = ['#e6532f', '#2f6fe6', '#7a4ee6', '#1f9d6a', '#d99a1a', '#d6336c', '#0c8599', '#495057'];

  function texture(img, person, i, ring) {
    const pad = Math.round(TEX * 0.06), W = TEX + pad * 2;
    const c = document.createElement('canvas');
    c.width = c.height = W;
    const g = c.getContext('2d');
    const circle = () => { g.beginPath(); g.arc(W / 2, W / 2, TEX / 2, 0, Math.PI * 2); };
    g.save();
    circle();
    g.clip();
    if (img) {
      g.drawImage(img, pad, pad, TEX, TEX);
    } else {
      g.fillStyle = COLORS[i % COLORS.length];
      g.fillRect(0, 0, W, W);
      g.fillStyle = '#fff';
      g.font = `600 ${TEX * 0.42}px -apple-system, "PingFang SC", sans-serif`;
      g.textAlign = 'center';
      g.textBaseline = 'middle';
      g.fillText([...(person.n || person.h)][0].toUpperCase(), W / 2, W / 2 + TEX * 0.02);
    }
    g.restore();
    circle();
    g.lineWidth = ring ? TEX * 0.07 : TEX * 0.02;
    g.strokeStyle = ring ? '#e6532f' : 'rgba(255,255,255,.55)';
    g.stroke();
    return { canvas: c, ratio: W / TEX };
  }

  // 阴影单独画、不跟着头像旋转，滚动时光影才自然
  function shadowSprite() {
    const S = 128, W = S * 2;
    const c = document.createElement('canvas');
    c.width = c.height = W;
    const g = c.getContext('2d');
    g.shadowColor = 'rgba(15,23,42,.30)';
    g.shadowBlur = S * 0.16;
    g.shadowOffsetY = S * 0.07 + W;
    g.beginPath();
    g.arc(W / 2, W / 2 - W, S / 2 * 0.96, 0, Math.PI * 2);
    g.fill();
    return { canvas: c, ratio: W / S };
  }

  const imgCache = new Map();
  function loadImg(src) {
    if (!imgCache.has(src)) {
      imgCache.set(src, new Promise((ok, fail) => {
        const im = new Image();
        im.decoding = 'async';
        im.onload = () => ok(im);
        im.onerror = fail;
        im.src = src;
      }));
    }
    return imgCache.get(src);
  }

  // ---------- 物理场景 ----------
  function createScene(M) {
    const { Engine, Bodies, Body, Composite, Query, Sleeping } = M;
    const ctx = canvas.getContext('2d');
    const shadow = shadowSprite();
    let W = Math.max(scene.clientWidth, 1), H = Math.max(scene.clientHeight, 1);
    let raf = 0, alive = true, active = false, last = performance.now(), acc = 0;

    const engine = Engine.create({ enableSleeping: true, positionIterations: 8, velocityIterations: 6 });
    engine.gravity.y = 1;
    const wall = { isStatic: true, friction: 0.5, restitution: 0.2 };
    const BIG = 1e5;
    const floor = Bodies.rectangle(W / 2, H + 50, BIG, 100, wall);
    const left = Bodies.rectangle(-50, -H, 100, BIG, wall);
    const right = Bodies.rectangle(W + 50, -H, 100, BIG, wall);
    const ceil = Bodies.rectangle(W / 2, -2600, BIG, 100, wall);
    Composite.add(engine.world, [floor, left, right, ceil]);

    // 窄屏缩小头像，保证一堆的高度差不多
    const scale = () => Math.max(0.6, Math.min(1, W / 960));
    const band = () => Math.min(W, 960);
    const spawnX = (f, r) => {
      const b = band();
      return (W - b) / 2 + r + 6 + f * (b - 2 * r - 12);
    };

    const order = PEOPLE.map((p, i) => i).sort(() => Math.random() - 0.5);
    const items = order.map((i, k) => {
      const p = PEOPLE[i];
      const me = p.h === current;
      const d = (me ? 88 : 44 + Math.random() * 34) * scale();
      const f = Math.random();
      const body = Bodies.circle(spawnX(f, d / 2), -60 - k * 18 - Math.random() * 120, d / 2, {
        restitution: 0.32, friction: 0.25, frictionStatic: 0.6, frictionAir: 0.012, density: 0.0012,
        angle: Math.random() * Math.PI * 2,
      });
      body.plugin.person = p;
      const it = {
        body, p, d, f, me,
        tex: texture(null, p, i, me),
        orbitR: 30 + Math.random() * 120,
        orbitA: Math.random() * Math.PI * 2,
        orbitV: (Math.random() < 0.5 ? -1 : 1) * (0.25 + Math.random() * 0.5),
      };
      loadImg(base + 'avatars/s/' + p.h + '.jpg').then(im => { it.tex = texture(im, p, i, me); wake(); }).catch(() => {});
      return it;
    });
    Composite.add(engine.world, items.map(it => it.body));

    function resize() {
      W = Math.max(scene.clientWidth, 1);
      H = Math.max(scene.clientHeight, 1);
      const dpr = Math.min(devicePixelRatio || 1, 2);
      canvas.width = Math.round(W * dpr);
      canvas.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      Body.setPosition(floor, { x: W / 2, y: H + 50 });
      Body.setPosition(left, { x: -50, y: -H });
      Body.setPosition(right, { x: W + 50, y: -H });
      for (const it of items) {
        const r = it.d / 2, { x, y } = it.body.position;
        Body.setPosition(it.body, { x: Math.max(r, Math.min(W - r, x)), y: Math.min(H - r, y) });
      }
      wake();
    }

    // ---------- 交互：悬停看名字、点击打开、按住聚集 ----------
    const ptr = { x: 0, y: 0, in: false, down: false, gather: false, t: 0, sx: 0, sy: 0, hit: null };
    const target = { x: W / 2, y: H * 0.45 };
    let holdTimer = 0;

    const local = e => {
      const r = scene.getBoundingClientRect();
      return { x: e.clientX - r.left, y: e.clientY - r.top };
    };
    const hitTest = (x, y) => {
      const b = Query.point(items.map(it => it.body), { x, y })[0];
      return b ? items.find(it => it.body === b) : null;
    };
    const onControl = e => e.target.closest('a, button, input, select, textarea');

    function showCue(text, x, y, held) {
      cue.textContent = text;
      cue.style.left = Math.max(70, Math.min(W - 70, x)) + 'px';
      cue.style.top = Math.max(30, Math.min(H - 30, y)) + 'px';
      cue.classList.toggle('is-held', !!held);
      cue.hidden = false;
    }
    const hideCue = () => { cue.hidden = true; };

    function hover(e) {
      const { x, y } = local(e);
      ptr.x = x; ptr.y = y;
      if (ptr.gather) { showCue('松开让大家落下', x, y, true); return; }
      if (ptr.down && Math.hypot(x - ptr.sx, y - ptr.sy) > 8 && !reduce) startGather();
      if (ptr.down) return;
      const it = onControl(e) ? null : hitTest(x, y);
      root.classList.toggle('is-hot', !!it);
      if (it) showCue(`${it.p.n} · @${it.p.h}`, it.body.position.x, it.body.position.y - it.d / 2 - 22);
      else hideCue();
    }

    function startGather() {
      if (ptr.gather) return;
      clearTimeout(holdTimer);
      ptr.gather = true;
      ptr.hit = null;
      target.x = ptr.x; target.y = ptr.y;
      root.classList.add('is-gather');
      root.classList.remove('is-hot');
      showCue('松开让大家落下', ptr.x, ptr.y, true);
      wake();
    }

    function down(e) {
      if (e.button !== 0 || onControl(e)) return;
      const { x, y } = local(e);
      Object.assign(ptr, { x, y, sx: x, sy: y, down: true, t: performance.now(), hit: hitTest(x, y) });
      if (!reduce) holdTimer = setTimeout(startGather, ptr.hit ? 260 : 120);
    }

    function up(e) {
      if (!ptr.down) return;
      clearTimeout(holdTimer);
      const wasGather = ptr.gather, hit = ptr.hit;
      ptr.down = false;
      ptr.gather = false;
      root.classList.remove('is-gather');
      if (wasGather) {
        engine.gravity.y = 1;
        hideCue();
        wake();
        return;
      }
      if (hit && e && e.type === 'pointerup') {
        location.href = base + 'people/' + hit.p.h + '/index.html';
      }
    }

    function cancel() {
      if (!ptr.down) return;
      clearTimeout(holdTimer);
      ptr.down = false;
      ptr.hit = null;
      if (ptr.gather) {
        ptr.gather = false;
        root.classList.remove('is-gather');
        engine.gravity.y = 1;
        hideCue();
        wake();
      }
    }

    root.addEventListener('pointerdown', down);
    root.addEventListener('pointermove', hover);
    root.addEventListener('pointerleave', () => { if (!ptr.down) { hideCue(); root.classList.remove('is-hot'); } });
    window.addEventListener('pointerup', up);
    window.addEventListener('pointercancel', cancel);
    window.addEventListener('blur', cancel);

    // ---------- 主循环 ----------
    const STEP = 1000 / 60;
    function physics(dt) {
      const g = ptr.gather;
      engine.gravity.y = g ? 0 : 1;
      if (g) {
        target.x += (ptr.x - target.x) * 0.18;
        target.y += (ptr.y - target.y) * 0.18;
      }
      for (acc = Math.min(acc + dt, STEP * 3); acc >= STEP - 0.01; acc -= STEP) {
        for (const it of items) {
          const b = it.body;
          b.frictionAir = g ? 0.05 : 0.012;
          if (!g) continue;
          it.orbitA += it.orbitV / 60;
          const r = Math.max(it.orbitR * Math.min(1, Math.min(W, H) / 700), 10);
          let dx = target.x + Math.cos(it.orbitA) * r - b.position.x;
          let dy = target.y + Math.sin(it.orbitA) * r - b.position.y;
          const dist = Math.hypot(dx, dy);
          if (dist > 600) { dx = dx / dist * 600; dy = dy / dist * 600; }
          const k = 2.6e-6, swirl = 6.4e-5 * Math.sign(it.orbitV);
          Body.applyForce(b, b.position, {
            x: b.mass * (dx * k - dy / (dist + 1) * swirl),
            y: b.mass * (dy * k + dx / (dist + 1) * swirl),
          });
          const sp = Math.hypot(b.velocity.x, b.velocity.y);
          if (sp > 26) Body.setVelocity(b, { x: b.velocity.x / sp * 26, y: b.velocity.y / sp * 26 });
        }
        Engine.update(engine, STEP);
      }
    }

    function draw() {
      ctx.clearRect(0, 0, W, H);
      for (const it of items) {
        const { x, y } = it.body.position;
        if (y < -it.d) continue;
        const ss = it.d * shadow.ratio;
        ctx.drawImage(shadow.canvas, x - ss / 2, y - ss / 2, ss, ss);
      }
      for (const it of items) {
        const { body: b, d, tex } = it;
        if (b.position.y < -d) continue;
        const s = d * tex.ratio;
        ctx.save();
        ctx.translate(b.position.x, b.position.y);
        ctx.rotate(b.angle);
        ctx.drawImage(tex.canvas, -s / 2, -s / 2, s, s);
        ctx.restore();
      }
    }

    function frame(now) {
      raf = 0;
      if (!alive || !active) return;
      const dt = Math.min(now - last, 1000 / 24);
      last = now;
      physics(dt);
      draw();
      if (ptr.gather || items.some(it => !it.body.isSleeping)) raf = requestAnimationFrame(frame);
    }

    function wake() {
      if (reduce) { draw(); return; }
      for (const it of items) Sleeping.set(it.body, false);
      if (alive && active && !raf) { last = performance.now(); raf = requestAnimationFrame(frame); }
    }

    resize();
    new ResizeObserver(resize).observe(scene);

    // 减少动态效果：直接算出堆好的样子，只画静态结果
    if (reduce) {
      for (let i = 0; i < 900; i++) Engine.update(engine, STEP);
      draw();
    }

    return {
      setActive(v) {
        active = v;
        if (v) wake();
        else { cancelAnimationFrame(raf); raf = 0; cancel(); }
      },
    };
  }

  // ---------- 何时开始 ----------
  // 页脚接近视口时预加载引擎；露出三分之一时头像开始落下，离开视口就暂停。
  let sim = null, seen = false;
  new IntersectionObserver(es => {
    if (!es.some(e => e.isIntersecting)) return;
    loadMatter().catch(() => {});
    for (const p of PEOPLE) loadImg(base + 'avatars/s/' + p.h + '.jpg').catch(() => {});
  }, { rootMargin: '600px 0px' }).observe(root);

  new IntersectionObserver(es => {
    const e = es[es.length - 1];
    const on = e.isIntersecting && e.intersectionRatio >= (seen ? 0 : 0.3);
    if (on && !sim) {
      seen = true;
      loadMatter().then(M => {
        sim = createScene(M);
        sim.setActive(!document.hidden);
      }).catch(() => root.setAttribute('data-drop-error', ''));
    } else if (sim) {
      sim.setActive(e.isIntersecting && !document.hidden);
    }
  }, { threshold: [0, 0.3] }).observe(root);

  document.addEventListener('visibilitychange', () => {
    if (sim) sim.setActive(!document.hidden && root.getBoundingClientRect().top < innerHeight);
  });
})();
