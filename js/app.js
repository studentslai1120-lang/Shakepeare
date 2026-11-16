'use strict';
// 檔名規則：images/<字母>_<單字小寫>.jpg、audio/words/<同名>.mp3、audio/quotes/<同名>.mp3
// 例：A_aroint。把同名檔案放進去（覆蓋）就能抽換；不需要改程式。
const MIN_REAL_SECONDS = 0.5;   // mp3 短於這個秒數，視為「占位檔」，改用瀏覽器語音朗讀
const $ = id => document.getElementById(id);
const slug = e => e.letter + '_' + e.word.toLowerCase();
const synth = window.speechSynthesis;
let cur = 0, voice = null, player = null, session = 0;

function pickVoice() {
  if (!synth) return;
  const vs = synth.getVoices();
  voice = vs.find(v => v.lang === 'en-GB') || vs.find(v => /^en/i.test(v.lang)) || null;
}
if (synth) { pickVoice(); if (synth.addEventListener) synth.addEventListener('voiceschanged', pickVoice); }

function status(t) { $('status').textContent = t || ''; }
function stopAll() {
  session++;
  if (player) { player.pause(); player = null; }
  if (synth) synth.cancel();
}
function speak(text) {
  if (!synth) { status('這個瀏覽器不支援語音朗讀，也還沒有放入 mp3 錄音。'); return; }
  const u = new SpeechSynthesisUtterance(text);
  u.lang = voice ? voice.lang : 'en-GB'; if (voice) u.voice = voice; u.rate = +$('rate').value;
  synth.speak(u);
}
function quoteText(e) { return e.quote.replace(/\n/g, ' ').replace(/[…“”]/g, ''); }

function play(kind) {                       // kind: 'words' 或 'quotes'
  const e = WORDS[cur]; stopAll(); const my = session;
  const file = 'audio/' + kind + '/' + slug(e) + '.mp3';
  const label = kind === 'words' ? '單字' : '金句';
  let fell = false;
  const fallback = () => {
    if (fell || my !== session) return; fell = true;
    status('找不到有內容的 mp3（' + file + '），改用瀏覽器語音朗讀' + label + '。');
    speak(kind === 'words' ? e.word : quoteText(e));
  };
  const a = new Audio(); player = a; a.preload = 'auto'; a.playbackRate = +$('rate').value;
  a.addEventListener('error', fallback);
  a.addEventListener('loadedmetadata', () => { if (!isFinite(a.duration) || a.duration < MIN_REAL_SECONDS) { a.pause(); fallback(); } });
  a.addEventListener('playing', () => { if (!fell && my === session && a.duration >= MIN_REAL_SECONDS) status('播放 mp3：' + file); });
  a.addEventListener('ended', () => { if (my === session && !fell) status(''); });
  a.src = file;
  const p = a.play();
  if (p && p.catch) p.catch(err => { if (err && err.name !== 'AbortError') fallback(); });
}

function show(i, speakWord) {
  cur = (i + WORDS.length) % WORDS.length; const e = WORDS[cur];
  stopAll(); status('');
  $('pic').src = 'images/' + slug(e) + '.jpg';
  $('pic').alt = e.word + ' 的印象派風格油畫插圖';
  $('cap').textContent = '插圖：images/' + slug(e) + '.jpg';
  $('lt').textContent = e.letter;
  $('w').textContent = e.word; $('ipa').textContent = e.ipa; $('zh').textContent = e.zh; $('note').textContent = e.note;
  const re = new RegExp(e.stem, 'i');
  $('q').innerHTML = '“' + e.quote.replace(re, m => '<mark>' + m + '</mark>') + '”';
  $('src').textContent = '—— ' + e.source;
  [...$('idx').children].forEach((b, k) => b.setAttribute('aria-current', String(k === cur)));
  if (speakWord) play('words');
}

WORDS.forEach((e, i) => {
  const b = document.createElement('button');
  b.type = 'button'; b.textContent = e.letter; b.setAttribute('aria-label', e.letter + '：' + e.word);
  b.addEventListener('click', () => show(i, true));
  $('idx').appendChild(b);
});
$('sw').addEventListener('click', () => play('words'));
$('sq').addEventListener('click', () => play('quotes'));
$('stop').addEventListener('click', () => { stopAll(); status(''); });
$('pv').addEventListener('click', () => show(cur - 1, true));
$('nx').addEventListener('click', () => show(cur + 1, true));
$('rate').addEventListener('change', () => { if (player) player.playbackRate = +$('rate').value; });
document.addEventListener('keydown', e => {
  if (e.ctrlKey || e.metaKey || e.altKey || e.target.tagName === 'SELECT') return;
  const i = WORDS.findIndex(w => w.letter === e.key.toUpperCase());
  if (/^[a-z]$/i.test(e.key) && i >= 0) show(i, true);
  else if (e.key === 'ArrowRight') show(cur + 1, true);
  else if (e.key === 'ArrowLeft') show(cur - 1, true);
});
show(0, false);
