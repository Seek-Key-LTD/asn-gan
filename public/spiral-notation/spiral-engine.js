/**
 * 螺线谱 (Spiral Notation) 核心引擎包 v1.0.0
 * 零依赖 ESM 模块：支持十二平均律/非标调式、八席位卦象映射、三合局约束与 WebAudio 合成
 */

export class SpiralNotationEngine {
  constructor(options = {}) {
    this.canvas = options.canvas;
    this.ctx = this.canvas ? this.canvas.getContext('2d') : null;
    this.audioCtx = null;
    this.activeNodes = [];

    // 地支 12 位与角度映射 (以 C 为子/0°)
    this.earthlyBranches = [
      { name: '子', note: 'C',  angle: 0 },
      { name: '丑', note: 'C#', angle: 30 },
      { name: '寅', note: 'D',  angle: 60 },
      { name: '卯', note: 'D#', angle: 90 },
      { name: '辰', note: 'E',  angle: 120 },
      { name: '巳', note: 'F',  angle: 150 },
      { name: '午', note: 'F#', angle: 180 },
      { name: '未', note: 'G',  angle: 210 },
      { name: '申', note: 'G#', angle: 240 },
      { name: '酉', note: 'A',  angle: 270 },
      { name: '戌', note: 'A#', angle: 300 },
      { name: '亥', note: 'B',  angle: 330 },
    ];

    // 八席位卦象与调式约束定义
    this.seats = {
      ludongbin: { name: '吕洞宾', hex: '☰ 乾', angle: 0,   root: 'G',  bureau: '申子辰', element: '水', color: '#00f0ff' },
      hexian-gu: { name: '何仙姑', hex: '☷ 坤', angle: 90,  root: 'C',  bureau: '亥卯未', element: '木', color: '#00ff66' },
      zhangguolao: { name: '张果老', hex: '☶ 艮', angle: 180, root: 'D',  bureau: '寅午戌', element: '火', color: '#ff3366' },
      hanxiangzi: { name: '韩湘子', hex: '☱ 兑', angle: 270, root: 'A',  bureau: '巳酉丑', element: '金', color: '#ffd700' },
      hanzhongli: { name: '汉钟离', hex: '☲ 离', angle: 45,  root: 'Eb', bureau: '巳酉丑', element: '金', color: '#ff9900' },
      lancaihe:   { name: '蓝采和', hex: '☵ 坎', angle: 135, root: 'Ab', bureau: '申子辰', element: '水', color: '#0099ff' },
      caoguojiu:  { name: '曹国舅', hex: '☳ 震', angle: 225, root: 'Bb', bureau: '亥卯未', element: '木', color: '#99ff33' },
      tieguai-li: { name: '铁拐李', hex: '☴ 巽', angle: 315, root: 'Db', bureau: '寅午戌', element: '火', color: '#ff00ff' }
    };

    // 三合局路径 (等分 120° 三角线)
    this.bureaus = {
      '申子辰': [240, 0, 120],   // 水局
      '亥卯未': [330, 90, 210],  // 木局
      '寅午戌': [60, 180, 300],  // 火局
      '巳酉丑': [150, 270, 30]   // 金局
    };

    // 螺旋几何参数: r = a * e^(b * theta)
    this.a = options.a || 20;
    this.b = options.b || 0.12;

    if (this.canvas) {
      this.initResize();
      requestAnimationFrame(() => this.render([], 'ludongbin'));
    }
  }

  initAudio() {
    if (!this.audioCtx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      this.audioCtx = new AudioContext();
    }
    if (this.audioCtx.state === 'suspended') {
      this.audioCtx.resume();
    }
  }

  initResize() {
    const resize = () => {
      const parent = this.canvas.parentElement;
      const width = parent.clientWidth || window.innerWidth - 340;
      const height = parent.clientHeight || window.innerHeight;
      this.canvas.width = width * window.devicePixelRatio;
      this.canvas.height = height * window.devicePixelRatio;
      this.ctx.resetTransform();
      this.ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
      this.render(this.lastActiveNotes || [], this.lastActiveSeat || 'ludongbin');
    };
    setTimeout(resize, 100);
    window.addEventListener('resize', resize);
  }

  /**
   * 将频率 (Hz) 或 Pitch 转换为螺旋坐标 (r, theta)
   */
  freqToSpiral(freq, octaveOffset = 0) {
    // 基础 A4 = 440Hz, C4 = 261.63Hz
    const midi = 69 + 12 * Math.log2(freq / 440);
    const semitoneFromC = (midi - 60) % 12;
    const octave = Math.floor((midi - 60) / 12) + octaveOffset;
    
    // 角度 (rad) 与 径向 r
    const theta = (semitoneFromC / 12) * Math.PI * 2 + octave * Math.PI * 2;
    const r = this.a * Math.exp(this.b * theta);
    
    return { r, theta, octave, semitone: semitoneFromC, freq };
  }

  /**
   * 计算 AI 谱曲音符序列的礼乐鉴赏值 (Appreciation Value)
   * @param {Array} notes 音符频率或 MIDI 列表
   * @param {Object} seat 指定工位/席位
   */
  evaluateAppreciation(notes, seatKey) {
    const seat = this.seats[seatKey] || this.seats.ludongbin;
    if (!notes || notes.length === 0) return { score: 100, status: '礼乐一致' };

    let totalPoints = 0;
    let breaches = 0;
    const allowedAngles = this.bureaus[seat.bureau] || [];

    notes.forEach(note => {
      const freq = typeof note === 'number' ? note : note.freq;
      const { semitone } = this.freqToSpiral(freq);
      const angle = (semitone / 12) * 360;

      // 检测是否在根音或三合局容差 15° 内
      const isCompliant = allowedAngles.some(targetAngle => {
        const diff = Math.abs((angle - targetAngle + 360) % 360);
        return diff <= 15 || diff >= 345;
      });

      if (isCompliant) {
        totalPoints += 1;
      } else {
        breaches += 1;
      }
    });

    const complianceRate = totalPoints / notes.length;
    const score = Math.round(complianceRate * 100);
    
    let status = '礼乐一致';
    if (score < 60) status = '严重破格';
    else if (score < 85) status = '局部偏离';

    return {
      seat: seat.name,
      bureau: seat.bureau,
      score,
      breaches,
      status
    };
  }

  /**
   * 触发 WebAudio 播放单个音符 (支持非标准调式 Hz)
   */
  playNote(freq, duration = 0.8, type = 'sine') {
    this.initAudio();
    const osc = this.audioCtx.createOscillator();
    const gain = this.audioCtx.createGain();

    osc.type = type;
    osc.frequency.setValueAtTime(freq, this.audioCtx.currentTime);

    gain.gain.setValueAtTime(0.3, this.audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.audioCtx.currentTime + duration);

    osc.connect(gain);
    gain.connect(this.audioCtx.destination);

    osc.start();
    osc.stop(this.audioCtx.currentTime + duration);
  }

  /**
   * 渲染渲染太虚朋克风 2D 螺线谱画布
   */
  render(activeNotes = [], activeSeatKey = 'ludongbin') {
    if (!this.ctx) return;
    const width = this.canvas.width / window.devicePixelRatio;
    const height = this.canvas.height / window.devicePixelRatio;
    const ctx = this.ctx;

    ctx.clearRect(0, 0, width, height);

    const centerX = width / 2;
    const centerY = height / 2;

    // 1. 绘制太虚深空背景线圈
    ctx.save();
    ctx.translate(centerX, centerY);

    // 绘制 3 个八度的对数螺旋线
    ctx.beginPath();
    ctx.strokeStyle = 'rgba(0, 240, 255, 0.25)';
    ctx.lineWidth = 1.5;

    const maxTheta = 6 * Math.PI; // 3 圈八度
    for (let t = 0; t <= maxTheta; t += 0.05) {
      const r = this.a * Math.exp(this.b * t);
      const x = r * Math.cos(t - Math.PI / 2);
      const y = r * Math.sin(t - Math.PI / 2);
      if (t === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    }
    ctx.stroke();

    // 2. 绘制 12 地支射线
    this.earthlyBranches.forEach(b => {
      const rad = (b.angle - 90) * (Math.PI / 180);
      const maxR = this.a * Math.exp(this.b * maxTheta);
      const x = maxR * Math.cos(rad);
      const y = maxR * Math.sin(rad);

      ctx.beginPath();
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.08)';
      ctx.setLineDash([2, 4]);
      ctx.moveTo(0, 0);
      ctx.lineTo(x, y);
      ctx.stroke();
      ctx.setLineDash([]);

      // 地支与音符标注
      const labelR = maxR + 20;
      const lx = labelR * Math.cos(rad);
      const ly = labelR * Math.sin(rad);
      ctx.fillStyle = 'rgba(0, 240, 255, 0.6)';
      ctx.font = '12px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(`${b.name} (${b.note})`, lx, ly);
    });

    // 3. 高亮当前激活席位的三合局连线
    const currentSeat = this.seats[activeSeatKey];
    if (currentSeat) {
      const angles = this.bureaus[currentSeat.bureau];
      if (angles) {
        ctx.beginPath();
        ctx.strokeStyle = currentSeat.color;
        ctx.lineWidth = 2;
        ctx.shadowColor = currentSeat.color;
        ctx.shadowBlur = 10;

        angles.forEach((deg, idx) => {
          const rad = (deg - 90) * (Math.PI / 180);
          const r = this.a * Math.exp(this.b * (4 * Math.PI)); // 中圈
          const x = r * Math.cos(rad);
          const y = r * Math.sin(rad);
          if (idx === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        });
        ctx.closePath();
        ctx.stroke();
        ctx.shadowBlur = 0;
      }
    }

    // 4. 绘制激活的音符点、几何多边形亮灯与激光能量弦线
    if (activeNotes && activeNotes.length > 0) {
      const points = activeNotes.map(note => {
        const freq = typeof note === 'number' ? note : note.freq;
        const { r, theta } = this.freqToSpiral(freq);
        return {
          x: r * Math.cos(theta - Math.PI / 2),
          y: r * Math.sin(theta - Math.PI / 2),
          color: note.color || '#00f0ff'
        };
      });

      // 4a. 如果被点亮音符 >= 2 个，自动拉出激光能量弦线形成几何图形
      if (points.length >= 2) {
        ctx.beginPath();
        ctx.strokeStyle = points[0].color;
        ctx.lineWidth = 2.5;
        ctx.shadowColor = points[0].color;
        ctx.shadowBlur = 15;

        points.forEach((pt, idx) => {
          if (idx === 0) ctx.moveTo(pt.x, pt.y);
          else ctx.lineTo(pt.x, pt.y);
        });
        if (points.length >= 3) ctx.closePath();
        ctx.stroke();
        ctx.shadowBlur = 0;
      }

      // 4b. 点亮音符强光喷发节点
      points.forEach(pt => {
        ctx.beginPath();
        ctx.arc(pt.x, pt.y, 8, 0, Math.PI * 2);
        ctx.fillStyle = pt.color;
        ctx.shadowColor = pt.color;
        ctx.shadowBlur = 20;
        ctx.fill();

        ctx.beginPath();
        ctx.arc(pt.x, pt.y, 3, 0, Math.PI * 2);
        ctx.fillStyle = '#ffffff';
        ctx.fill();
        ctx.shadowBlur = 0;
      });
    }

    ctx.restore();
  }
}
