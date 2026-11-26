// Original cartoon illustrations drawn for this blog, one per category plus the
// hero character. Plain inline SVG: no external assets, scales cleanly, and the
// strings are static, so inserting them with innerHTML is safe.

const INK = '#1f1b2e';
const S = `stroke="${INK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"`;

const face = (cx, cy, { mood = 'happy', blush = '#ff8fa3' } = {}) => {
  const eyes = mood === 'sleepy'
    ? `<path d="M${cx - 18} ${cy} q6 6 12 0 M${cx + 6} ${cy} q6 6 12 0" fill="none" ${S}/>`
    : `<circle cx="${cx - 12}" cy="${cy}" r="5" fill="${INK}"/><circle cx="${cx + 12}" cy="${cy}" r="5" fill="${INK}"/>
       <circle cx="${cx - 10}" cy="${cy - 2}" r="1.6" fill="#fff"/><circle cx="${cx + 14}" cy="${cy - 2}" r="1.6" fill="#fff"/>`;
  const brows = mood === 'worried'
    ? `<path d="M${cx - 20} ${cy - 14} l10 -5 M${cx + 20} ${cy - 14} l-10 -5" ${S} fill="none"/>`
    : '';
  const mouth = {
    happy: `<path d="M${cx - 9} ${cy + 12} q9 9 18 0" fill="none" ${S}/>`,
    worried: `<path d="M${cx - 9} ${cy + 16} q4.5 -5 9 0 q4.5 5 9 0" fill="none" ${S}/>`,
    sleepy: `<path d="M${cx - 5} ${cy + 13} q5 4 10 0" fill="none" ${S}/>`,
    calm: `<path d="M${cx - 7} ${cy + 12} q7 6 14 0" fill="none" ${S}/>`,
  }[mood];
  return `${brows}${eyes}${mouth}
    <ellipse cx="${cx - 24}" cy="${cy + 10}" rx="7" ry="4.5" fill="${blush}" opacity=".75"/>
    <ellipse cx="${cx + 24}" cy="${cy + 10}" rx="7" ry="4.5" fill="${blush}" opacity=".75"/>`;
};

const sparkle = (x, y, r = 8, fill = '#fff') =>
  `<path d="M${x} ${y - r} Q${x} ${y} ${x + r} ${y} Q${x} ${y} ${x} ${y + r} Q${x} ${y} ${x - r} ${y} Q${x} ${y} ${x} ${y - r}Z" fill="${fill}" ${S} stroke-width="3"/>`;

const svg = (body, label) =>
  `<svg viewBox="0 0 200 200" role="img" aria-label="${label}" xmlns="http://www.w3.org/2000/svg">${body}</svg>`;

export const ILLUSTRATIONS = {
  // A worried little storm cloud, with the sun already peeking out behind it.
  'kaygi-ve-stres': svg(`
    <circle cx="150" cy="58" r="26" fill="#ffd23f" ${S}/>
    <path d="M150 18v-8M182 30l6-6M190 58h8" ${S}/>
    <path d="M46 138c-22 0-30-30-8-40-4-26 26-42 46-26 8-24 50-24 56 4 26-2 36 30 16 44 6 14-6 22-16 22H46z" fill="#dfe7ff" ${S}/>
    ${face(98, 108, { mood: 'worried' })}
    <path d="M92 146l-12 22h14l-8 22 26-30h-14l8-14z" fill="#ffd23f" ${S} stroke-width="4"/>
    <path d="M150 110c0 6-4 9-7 9s-7-3-7-9 7-14 7-14 7 8 7 14z" fill="#7cc8ff" ${S} stroke-width="3.5"/>
  `, 'Endişeli bir bulut karakteri'),

  // A cheerful sprout growing out of its pot.
  'kisisel-gelisim': svg(`
    <path d="M100 112V70" ${S}/>
    <path d="M100 86c-6-24-30-34-46-28 4 22 26 34 46 28z" fill="#7ed957" ${S}/>
    <path d="M100 74c8-24 34-32 48-24-6 22-30 30-48 24z" fill="#9be36f" ${S}/>
    <path d="M52 112h96l-12 70H64z" fill="#ff9966" ${S}/>
    <path d="M46 104h108v18H46z" fill="#ff7f50" ${S}/>
    ${face(100, 148, { mood: 'happy', blush: '#ff5a5a' })}
    ${sparkle(42, 50, 10, '#ffd23f')}
    ${sparkle(160, 100, 7, '#fff')}
  `, 'Saksıda büyüyen gülümseyen bir filiz'),

  // Two speech bubbles sharing a heart.
  'iliskiler': svg(`
    <path d="M22 44c0-12 8-20 20-20h70c12 0 20 8 20 20v40c0 12-8 20-20 20H64l-22 20 4-20h-4c-12 0-20-8-20-20z" fill="#fff" ${S}/>
    <path d="M70 96c0-12 8-20 20-20h70c12 0 20 8 20 20v40c0 12-8 20-20 20h-4l4 20-22-20H90c-12 0-20-8-20-20z" fill="#ffc2d1" ${S}/>
    <circle cx="52" cy="64" r="5" fill="${INK}"/><circle cx="72" cy="64" r="5" fill="${INK}"/><circle cx="92" cy="64" r="5" fill="${INK}"/>
    <path d="M125 142c-22-14-30-24-30-34 0-8 6-14 14-14 7 0 12 4 16 10 4-6 9-10 16-10 8 0 14 6 14 14 0 10-8 20-30 34z" fill="#ff4f6d" ${S}/>
    ${sparkle(170, 46, 9, '#ffd23f')}
  `, 'Ortasında kalp olan iki konuşma balonu'),

  // A sleepy crescent moon in a nightcap.
  'uyku-ve-beden': svg(`
    <path d="M120 30c-44 6-70 52-52 92 16 34 58 46 90 28-38 0-66-30-62-70 2-22 10-38 24-50z" fill="#ffe27a" ${S}/>
    <path d="M96 40c-2-22 20-34 40-26l26 10-30 10c-10 2-24 4-36 6z" fill="#6c8cff" ${S}/>
    <circle cx="166" cy="26" r="9" fill="#fff" ${S} stroke-width="4"/>
    <path d="M78 96q6 6 12 0" fill="none" ${S}/>
    <path d="M86 116q6 5 12 0" fill="none" ${S}/>
    <ellipse cx="74" cy="110" rx="7" ry="4.5" fill="#ff8fa3" opacity=".8"/>
    <path d="M132 70h18l-18 18h18M160 100h12l-12 12h12" fill="none" ${S} stroke-width="4"/>
    ${sparkle(40, 50, 8, '#fff')}
    ${sparkle(170, 150, 10, '#fff')}
  `, 'Bere takmış uykulu bir hilal'),

  // A calm round friend meditating on a lotus.
  'farkindalik': svg(`
    <circle cx="100" cy="58" r="20" fill="none" stroke="#ffd23f" stroke-width="5" stroke-dasharray="6 10" stroke-linecap="round"/>
    <path d="M40 172c10-26 40-30 60-30s50 4 60 30z" fill="#ff9ec4" ${S}/>
    <path d="M70 168c4-18 14-26 30-30 16 4 26 12 30 30" fill="#ffc2d1" ${S}/>
    <ellipse cx="100" cy="116" rx="48" ry="46" fill="#cdb8ff" ${S}/>
    ${face(100, 108, { mood: 'sleepy' })}
    <path d="M54 128c-10 8-14 18-6 22 8 2 22-4 30-10M146 128c10 8 14 18 6 22-8 2-22-4-30-10" fill="#cdb8ff" ${S}/>
    ${sparkle(34, 80, 8, '#fff')}
    ${sparkle(168, 70, 10, '#ffd23f')}
  `, 'Lotus üzerinde meditasyon yapan yuvarlak bir karakter'),
};

// Hero character: a reader with a thought bubble, on a soft brush blob.
export const HERO = `
<svg viewBox="0 0 420 400" role="img" aria-label="Kitap okuyan ve aklından kalp geçen gülümseyen bir karakter" xmlns="http://www.w3.org/2000/svg">
  <path d="M60 210c-30-70 30-150 120-160 70-8 150 20 180 90 26 60 6 140-60 180-70 42-190 30-230-20-12-16-4-60-10-90z" fill="#ffd9c7"/>
  <path d="M40 250c10 20 30 30 50 28M360 120c14 10 22 26 20 44" fill="none" stroke="#f3b9a0" stroke-width="10" stroke-linecap="round"/>
  <g>
    <circle cx="318" cy="70" r="40" fill="#fff" ${S}/>
    <circle cx="294" cy="126" r="11" fill="#fff" ${S}/>
    <circle cx="286" cy="150" r="6" fill="#fff" ${S}/>
    <path d="M318 92c-16-10-24-18-24-26 0-6 5-11 11-11 5 0 10 3 13 8 3-5 8-8 13-8 6 0 11 5 11 11 0 8-8 16-24 26z" fill="#ff4f6d" ${S} stroke-width="4"/>
  </g>
  <path d="M96 400c0-60 40-96 110-96s110 36 110 96z" fill="#ffd23f" ${S}/>
  <path d="M178 306l28 30 28-30" fill="none" ${S}/>
  <path d="M186 268h40v40h-40z" fill="#ffc9a3" ${S}/>
  <path d="M136 176c0-58 30-92 70-92s70 34 70 92c0 54-30 98-70 98s-70-44-70-98z" fill="#ffc9a3" ${S}/>
  <path d="M130 186c-8-74 30-118 82-114 46 4 74 42 68 106-12-24-30-40-52-48-6 16-30 30-60 30-14 0-26 10-38 26z" fill="#5b3a29" ${S}/>
  <circle cx="212" cy="72" r="20" fill="#5b3a29" ${S}/>
  <circle cx="178" cy="190" r="22" fill="#fff" fill-opacity=".35" ${S}/>
  <circle cx="238" cy="190" r="22" fill="#fff" fill-opacity=".35" ${S}/>
  <path d="M200 190h16M156 186l-18-6M260 186l16-6" ${S}/>
  <circle cx="180" cy="192" r="5" fill="${INK}"/><circle cx="236" cy="192" r="5" fill="${INK}"/>
  <path d="M192 236q16 14 32 0" fill="none" ${S}/>
  <ellipse cx="160" cy="228" rx="10" ry="6" fill="#ff8fa3" opacity=".8"/>
  <ellipse cx="256" cy="228" rx="10" ry="6" fill="#ff8fa3" opacity=".8"/>
  <path d="M120 330l86 20 86-20v62l-86 8-86-8z" fill="#ff5a36" ${S}/>
  <path d="M206 350v48" ${S}/>
  <path d="M134 346l50 10M134 364l50 10M228 356l50-10M228 374l50-10" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".85"/>
  <path d="M110 338c-10-4-16 6-10 14l14 10M302 338c10-4 16 6 10 14l-14 10" fill="#ffc9a3" ${S}/>
</svg>`;

export const categoryArt = slug => ILLUSTRATIONS[slug] || ILLUSTRATIONS['kisisel-gelisim'];
