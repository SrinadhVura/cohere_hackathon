#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import sys
import cohere
from streamlit.web import cli as stcli
from streamlit import runtime
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

COHERE_CLIENT = os.environ.get("COHERE_CLIENT")
COHERE_MODEL = os.environ.get("COHERE_MODEL")
BASE_PROMPT="Generate Mandarin by HSK level and English keywords\nenglish:  light\nhsk: 1\nmandarin: 所有的灯都闪了一会儿。\npinyin: suǒ yǒu de dēng dōu shǎn le yī huìr。\n--\nenglish:  window\nhsk: 1\nmandarin: 所有的窗户都用砖堵住了。\npinyin: suǒ yǒu de chuāng hu dōu yòng zhuān dǔ zhù le。\n--\nenglish:  airplane\nhsk: 1\nmandarin: 一架飞机在机场着陆。\npinyin: yī jià fēi jī zài jī chǎng zhuó lù。\n--\nenglish: styles\nhsk: 2\nmandarin: 这些式样均可改动以适应个人不同的爱好.\npinyin: zhè xie shì yàng jūn kě gǎi dòng yǐ shì yìng gè rén bù tóng de ài hào.\n--\nenglish: food.\nhsk: 2\nmandarin: 他以自己的名字命名的冷冻食品成了名牌。\npinyin: tā yǐ zì jǐ de míng zi mìng míng de lěng dòng shí pǐn chéng le míng pái。\n--\nenglish: glasses.\nhsk: 2\nmandarin: 印刷字体太小，我不带眼镜就看不清。\npinyin: yìn shuà zì tǐ tài xiǎo， wǒ bù dài yǎn jìng jiù kàn bù qīng。\n--\nenglish: practice\nhsk: 3\nmandarin: 实践与理论一样重要，但是我们易于珍视后者而轻视前者。\npinyin: shí jiàn yù lǐ lùn yí yàng zhòng yào， dàn shì wǒ men yì yú zhēn shì hǒu zhě ér qīng shì qián zhě。\n--\nenglish: sluggish\nhsk: 3\nmandarin: 很多队员渐渐变得动作迟缓了。这支队所需的是一些新鲜血液。\npinyin: hěn duō duì yuán jiàn jiàn biàn de dòng zuò chí huǎn le。 zhè zhī duì suǒ xū de shì yī xiē xīn xiān xuè yè。\n--\nenglish: medicine\nhsk: 3\nmandarin: 医术在于，当大自然为病者医治疾病的一段期间内，逗得病人高兴。\npinyin: yī zhú zài yú， dàng dà zì rán wèi bìng zhě yī zhì jí bìng de yī duàn qī jiān nèi， dòu dé bìng rén gāo xìng。\n--\n--\nenglish: princess\nhsk: 4\nmandarin: 公主光彩照人地穿着一身雪白的新礼服来了。\npinyin: gōng zhǔ guāng cǎi zhào rén de chuān zhuó yī shēn xuě bái de xīn lǐ fú lái le。\n--\nenglish: parking space\nhsk: 4\nmandarin: 我认为他侵占我的停车位肯定是有意和我作对。\npinyin: wǒ rèn wéi tā qīn zhàn wǒ de tíng chē wèi kěn dìng shì yǒu yì huò wǒ zuò duì。\n--\nenglish: discrepancy\nhsk: 4\nmandarin: 这件事的两种说法有很大出入.\npinyin: zhè jiàn shì de liǎng zhòng shuō fa yǒu hěn dà chū rù.\n--\n"


def generate_texts(keyword, hsk):
  print(f"keyword: {keyword} and hsk: {hsk}")
  co = cohere.Client(COHERE_CLIENT)
  response = co.generate(
    model=COHERE_MODEL,
    prompt=BASE_PROMPT + "english: {keyword}\nhsk: {hsk}\nmandarin:".format(keyword=keyword, hsk=hsk),
    max_tokens=200,
    temperature=0.5,
    k=0,
    p=0.75,
    frequency_penalty=0.5,
    presence_penalty=0.5,
    stop_sequences=["--"],
    return_likelihoods='NONE')
  
  print('Prediction: {}'.format(response.generations[0].text))
  return response.generations[0].text


def main():
  st.title("Chinese Sentence Generator with English Keyword and HSK Level")
  
  form = st.form(key="user_settings")
  with form:
      en_keyword = st.text_input("English Keyword",
                                 placeholder="Enter an English keyword, eg. home, key, etc",
                                 key = "en_keyword")
      hsk_level = st.select_slider("HSK Level",
                                   options=["1", "2", "3", "4"],
                                   key = "hsk_level")

      generate_button = form.form_submit_button("Generate Mandarin Sentence and Pinyin")

      if generate_button:
        cohere_txts = generate_texts(en_keyword, hsk_level)
        st.markdown("##### " + "Generated Mandarin Sentence: ")
        st.write(cohere_txts)

  st.write("Check out the prediction on [Google Translate](https://www.google.com/search?q=google+translate&oq=google+translate&aqs=chrome.0.69i59j69i64j0i271l2j69i60.5320j0j1&sourceid=chrome&ie=UTF-8)")
  
if __name__ == "__main__":
  if runtime.exists():
    main()
  else:
    sys.argv = ["streamlit", "run", sys.argv[0]]
    sys.exit(stcli.main())