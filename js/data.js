// 詞彙資料。可直接編輯文字；檔名由 letter 與 word 自動對應（見 README.md）。
const WORDS = [
 {
  "letter": "A",
  "word": "aroint",
  "ipa": "/əˈrɔɪnt/",
  "zh": "滾開！（驅趕用的咒語）",
  "note": "古語，用來喝退女巫或惡靈。",
  "quote": "“Aroint thee, witch!” the rump-fed ronyon cries.",
  "source": "《馬克白》Macbeth · 1.3",
  "stem": "aroint"
 },
 {
  "letter": "B",
  "word": "bombast",
  "ipa": "/ˈbɒmbast/",
  "zh": "誇大空洞的辭藻",
  "note": "原指填充衣服的棉絮，後比喻浮誇的言辭。",
  "quote": "But he, as loving his own pride and purposes,\nEvades them, with a bombast circumstance\nHorribly stuffed with epithets of war.",
  "source": "《奧賽羅》Othello · 1.1",
  "stem": "bombast"
 },
 {
  "letter": "C",
  "word": "cerements",
  "ipa": "/ˈsɪəmənts/",
  "zh": "裹屍布",
  "note": "包裹遺體的蠟布，常用於描寫亡靈與墳墓。",
  "quote": "Why thy canonized bones, hearsed in death,\nHave burst their cerements.",
  "source": "《哈姆雷特》Hamlet · 1.4",
  "stem": "cerements"
 },
 {
  "letter": "D",
  "word": "dateless",
  "ipa": "/ˈdeɪtləs/",
  "zh": "無期限的；永恆的",
  "note": "在此指沒有終點的、永遠有效的契約。",
  "quote": "A dateless bargain to engrossing death!",
  "source": "《羅密歐與茱麗葉》Romeo and Juliet · 5.3",
  "stem": "dateless"
 },
 {
  "letter": "E",
  "word": "extenuate",
  "ipa": "/ɪkˈstɛnjʊeɪt/",
  "zh": "減輕（罪過）；為…開脫",
  "note": "奧賽羅臨終前要求人們如實講述他的故事。",
  "quote": "Speak of me as I am; nothing extenuate,\nNor set down aught in malice.",
  "source": "《奧賽羅》Othello · 5.2",
  "stem": "extenuate"
 },
 {
  "letter": "F",
  "word": "fardel",
  "ipa": "/ˈfɑːdl/",
  "zh": "包袱；重擔",
  "note": "舊時指捆紮的行李，後比喻人生的重負。",
  "quote": "Who would fardels bear,\nTo grunt and sweat under a weary life,",
  "source": "《哈姆雷特》Hamlet · 3.1",
  "stem": "fardels"
 },
 {
  "letter": "G",
  "word": "gossamer",
  "ipa": "/ˈɡɒsəmə/",
  "zh": "蛛絲；輕薄如紗",
  "note": "形容極輕、極細的東西。",
  "quote": "Hadst thou been aught but gossamer, feathers, air,\nSo many fathom down precipitating,\nThou’dst shiver’d like an egg.",
  "source": "《李爾王》King Lear · 4.6",
  "stem": "gossamer"
 },
 {
  "letter": "H",
  "word": "halcyon",
  "ipa": "/ˈhælsiən/",
  "zh": "平靜安詳的",
  "note": "源自神話中的翠鳥，傳說牠孵卵時海面風平浪靜。",
  "quote": "Expect Saint Martin’s summer, halcyon days,\nSince I have entered into these wars.",
  "source": "《亨利六世（上）》Henry VI, Part 1 · 1.2",
  "stem": "halcyon"
 },
 {
  "letter": "I",
  "word": "incarnadine",
  "ipa": "/ɪnˈkɑːnədaɪn/",
  "zh": "染成血紅色",
  "note": "極罕見的動詞，意思是把某物染得鮮紅。",
  "quote": "This my hand will rather\nThe multitudinous seas incarnadine,\nMaking the green one red.",
  "source": "《馬克白》Macbeth · 2.2",
  "stem": "incarnadine"
 },
 {
  "letter": "J",
  "word": "jocund",
  "ipa": "/ˈdʒɒkənd/",
  "zh": "歡快的；愉悅的",
  "note": "文學中形容明朗、快活的氣氛。",
  "quote": "Night’s candles are burnt out, and jocund day\nStands tiptoe on the misty mountain tops.",
  "source": "《羅密歐與茱麗葉》Romeo and Juliet · 3.5",
  "stem": "jocund"
 },
 {
  "letter": "K",
  "word": "knell",
  "ipa": "/nɛl/",
  "zh": "喪鐘（聲）",
  "note": "敲響宣告死亡或終結的鐘聲。",
  "quote": "Sea-nymphs hourly ring his knell:\nDing-dong.",
  "source": "《暴風雨》The Tempest · 1.2",
  "stem": "knell"
 },
 {
  "letter": "L",
  "word": "lascivious",
  "ipa": "/ləˈsɪviəs/",
  "zh": "輕佻放蕩的",
  "note": "理查三世嘲諷和平時期只剩享樂的宮廷。",
  "quote": "He capers nimbly in a lady’s chamber\nTo the lascivious pleasing of a lute.",
  "source": "《理查三世》Richard III · 1.1",
  "stem": "lascivious"
 },
 {
  "letter": "M",
  "word": "mewling",
  "ipa": "/ˈmjuːlɪŋ/",
  "zh": "（嬰兒）嗚嗚哭鬧",
  "note": "形容幼兒細聲哭啼的樣子。",
  "quote": "At first the infant,\nMewling and puking in the nurse’s arms.",
  "source": "《皆大歡喜》As You Like It · 2.7",
  "stem": "mewling"
 },
 {
  "letter": "N",
  "word": "nuncle",
  "ipa": "/ˈnʌŋkl/",
  "zh": "叔叔；舅舅（暱稱）",
  "note": "由 mine uncle 連讀而成，小丑用來稱呼李爾王。",
  "quote": "Can you make no use of nothing, nuncle?",
  "source": "《李爾王》King Lear · 1.4",
  "stem": "nuncle"
 },
 {
  "letter": "O",
  "word": "oxlips",
  "ipa": "/ˈɒkslɪps/",
  "zh": "黃花九輪草",
  "note": "一種春天開花的野花。",
  "quote": "I know a bank where the wild thyme blows,\nWhere oxlips and the nodding violet grows.",
  "source": "《仲夏夜之夢》A Midsummer Night’s Dream · 2.1",
  "stem": "oxlips"
 },
 {
  "letter": "P",
  "word": "perdition",
  "ipa": "/pəˈdɪʃn/",
  "zh": "毀滅；沉淪（靈魂永遠喪失）",
  "note": "神學詞彙，指靈魂的永劫。",
  "quote": "Perdition catch my soul,\nBut I do love thee! and when I love thee not,\nChaos is come again.",
  "source": "《奧賽羅》Othello · 3.3",
  "stem": "perdition"
 },
 {
  "letter": "Q",
  "word": "quintessence",
  "ipa": "/kwɪnˈtɛsns/",
  "zh": "精髓；典範",
  "note": "原指古代傳說中的「第五元素」。",
  "quote": "And yet, to me, what is this quintessence of dust?",
  "source": "《哈姆雷特》Hamlet · 2.2",
  "stem": "quintessence"
 },
 {
  "letter": "R",
  "word": "rood",
  "ipa": "/ruːd/",
  "zh": "（基督的）十字架",
  "note": "by the rood 是以十字架起誓的舊式說法。",
  "quote": "No, by the rood, not so:\nYou are the queen, your husband’s brother’s wife.",
  "source": "《哈姆雷特》Hamlet · 3.4",
  "stem": "rood"
 },
 {
  "letter": "S",
  "word": "sooth",
  "ipa": "/suːθ/",
  "zh": "真實；實情",
  "note": "in sooth 即「說真的」；也可說 forsooth。",
  "quote": "In sooth, I know not why I am so sad.",
  "source": "《威尼斯商人》The Merchant of Venice · 1.1",
  "stem": "sooth"
 },
 {
  "letter": "T",
  "word": "tarry",
  "ipa": "/ˈtæri/",
  "zh": "逗留；稍待",
  "note": "古雅的說法，叫對方先別動、等一下。",
  "quote": "Tarry a little; there is something else.",
  "source": "《威尼斯商人》The Merchant of Venice · 4.1",
  "stem": "tarry"
 },
 {
  "letter": "U",
  "word": "unsex",
  "ipa": "/ʌnˈsɛks/",
  "zh": "使失去（性別）特質",
  "note": "麥克白夫人祈求褪去柔弱，換上狠心。",
  "quote": "Come, you spirits\nThat tend on mortal thoughts, unsex me here.",
  "source": "《馬克白》Macbeth · 1.5",
  "stem": "unsex"
 },
 {
  "letter": "V",
  "word": "votaress",
  "ipa": "/ˈvəʊtərɪs/",
  "zh": "女信徒；矢志獨身的女子",
  "note": "指虔誠奉獻、立誓守貞的女性。",
  "quote": "In the imperial votaress passed on,\nIn maiden meditation, fancy-free.",
  "source": "《仲夏夜之夢》A Midsummer Night’s Dream · 2.1",
  "stem": "votaress"
 },
 {
  "letter": "W",
  "word": "wanton",
  "ipa": "/ˈwɒntən/",
  "zh": "任性放縱的；頑劣的",
  "note": "此處指隨意玩弄、不顧後果的孩子。",
  "quote": "As flies to wanton boys are we to the gods;\nThey kill us for their sport.",
  "source": "《李爾王》King Lear · 4.1",
  "stem": "wanton"
 },
 {
  "letter": "X",
  "word": "Xanthippe",
  "ipa": "/zænˈtɪpi/",
  "zh": "贊西佩（蘇格拉底之妻）",
  "note": "後世用來指脾氣潑辣的妻子；莎翁裡少見的 X 開頭詞。",
  "quote": "…as curst and shrewd\nAs Socrates’ Xanthippe, or a worse,\nShe moves me not.",
  "source": "《馴悍記》The Taming of the Shrew · 1.2",
  "stem": "xanthippe"
 },
 {
  "letter": "Y",
  "word": "yeomen",
  "ipa": "/ˈjəʊmən/",
  "zh": "自耕農；平民士兵（yeoman 的複數）",
  "note": "在英國歷史上指擁有小塊土地的自由農民。",
  "quote": "And you, good yeomen,\nWhose limbs were made in England, show us here\nThe mettle of your pasture.",
  "source": "《亨利五世》Henry V · 3.1",
  "stem": "yeomen"
 },
 {
  "letter": "Z",
  "word": "zenith",
  "ipa": "/ˈzɛnɪθ/",
  "zh": "天頂；巔峰",
  "note": "原指天空正上方的那一點，比喻運勢最高點。",
  "quote": "…I find my zenith doth depend upon\nA most auspicious star.",
  "source": "《暴風雨》The Tempest · 1.2",
  "stem": "zenith"
 }
];
