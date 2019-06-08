import jieba
import numpy as np
#中文文本情绪分析py
def Chinese(data):
    # 打开词典文件，返回列表
    def open_dict(Dict='hahah',path = r'Textming/Textming/'):
        path = path + '%s.txt' %Dict
        dictionary = open(path, 'r', encoding='utf-8')
        dict = []
        for word in dictionary:
            word = word.strip('\n')
            dict.append(word)
        return dict

    def judgeodd(num):
        if num % 2 == 0:
            return 'even'
        else:
            return 'odd'

    deny_word = open_dict(Dict='否定词')
    posdict = open_dict(Dict='positive')
    negdict = open_dict(Dict = 'negative')

    degree_word = open_dict(Dict = '程度级别词语',path=r'Textming/Textming/')
    mostdict = degree_word[degree_word.index('extreme')+1: degree_word.index('very')] #权重4，即在情感前乘以3
    verydict = degree_word[degree_word.index('very')+1: degree_word.index('more')] #权重3
    moredict = degree_word[degree_word.index('more')+1: degree_word.index('ish')]#权重2
    ishdict = degree_word[degree_word.index('ish')+1: degree_word.index('last')]#权重0.5

    def sentiment_score_list(dataset):
        seg_sentence = dataset.split('.')

        count1 = []
        count2 = []
        for sen in seg_sentence: # 循环遍历每一个评论
            segtmp = jieba.lcut(sen, cut_all=False) # 把句子进行分词，以列表的形式返回
            i = 0 #记录扫描到的词的位置
            a = 0 #记录情感词的位置
            poscount = 0 # 积极词的第一次分值
            poscount2 = 0 # 积极反转后的分值
            poscount3 = 0 # 积极词的最后分值（包括叹号的分值）
            negcount = 0
            negcount2 = 0
            negcount3 = 0
            for word in segtmp:
                if word in posdict: # 判断词语是否是情感词
                    poscount +=1
                    c = 0
                    for w in segtmp[a:i]: # 扫描情感词前的程度词
                        if w in mostdict:
                            poscount *= 4.0
                        elif w in verydict:
                            poscount *= 3.0
                        elif w in moredict:
                           poscount *= 2.0
                        elif w in ishdict:
                            poscount *= 0.5
                        elif w in deny_word: c+= 1
                    if judgeodd(c) == 'odd': # 扫描情感词前的否定词数
                        poscount *= -1.0
                        poscount2 += poscount
                        poscount = 0
                        poscount3 = poscount + poscount2 + poscount3
                        poscount2 = 0
                    else:
                        poscount3 = poscount + poscount2 + poscount3
                        poscount = 0
                    a = i+1
                elif word in negdict: # 消极情感的分析，与上面一致
                    negcount += 1
                    d = 0
                    for w in segtmp[a:i]:
                        if w in mostdict:
                            negcount *= 4.0
                        elif w in verydict:
                            negcount *= 3.0
                        elif w in moredict:
                            negcount *= 2.0
                        elif w in ishdict:
                            negcount *= 0.5
                        elif w in degree_word:
                            d += 1
                    if judgeodd(d) == 'odd':
                        negcount *= -1.0
                        negcount2 += negcount
                        negcount = 0
                        negcount3 = negcount + negcount2 + negcount3
                        negcount2 = 0
                    else:
                        negcount3 = negcount + negcount2 + negcount3
                        negcount = 0
                    a = i + 1
                elif word == '！' or word == '!': # 判断句子是否有感叹号
                    for w2 in segtmp[::-1]: # 扫描感叹号前的情感词，发现后权值+2，然后退出循环
                        if w2 in posdict or negdict:
                            poscount3 += 2
                            negcount3 += 2
                            break
                i += 1

                # 以下是防止出现负数的情况
                pos_count = 0
                neg_count = 0
                if poscount3 <0 and negcount3 > 0:
                    neg_count += negcount3 - poscount3
                    pos_count = 0
                elif negcount3 <0 and poscount3 > 0:
                    pos_count = poscount3 - negcount3
                    neg_count = 0
                elif poscount3 <0 and negcount3 < 0:
                    neg_count = -pos_count
                    pos_count = -neg_count
                else:
                    pos_count = poscount3
                    neg_count = negcount3
                count1.append([pos_count,neg_count])
            count2.append(count1)
            count1=[]

        return count2

    def sentiment_score(senti_score_list):
        score = []
        for review in senti_score_list:
            score_array =  np.array(review)
            Pos = np.sum(score_array[:,0])
            Neg = np.sum(score_array[:,1])
            AvgPos = np.mean(score_array[:,0])
            AvgPos = float('%.lf' % AvgPos)
            AvgNeg = np.mean(score_array[:, 1])
            AvgNeg = float('%.1f' % AvgNeg)
            StdPos = np.std(score_array[:, 0])
            StdPos = float('%.1f' % StdPos)
            StdNeg = np.std(score_array[:, 1])
            StdNeg = float('%.1f' % StdNeg)
            score.append([Pos,Neg,AvgPos,AvgNeg,StdPos,StdNeg])
        return score

    #print("[Pos,Neg,AvgPos,AvgNeg,StdPos,StdNeg]")
    a=(sentiment_score(sentiment_score_list(data)))
    print(a)
    x=a[0][0]#积极值
    y=a[0][1]#消极值
    # 以下是对情绪分析结果列表进行情绪分析值计算
    if x==y:  # 积极情绪值和消极情绪值相等则情绪分析为中性
        the_sentiment_score=0.5
    elif x==0 and y!=0:  # 积极情绪值为0，消极情绪值不为0，则为消极情绪结果，并将结果化1
        the_sentiment_score=y/(y+a[0][2]+a[0][3]+a[0][4]+a[0][5])
        if the_sentiment_score>0.5:
            the_sentiment_score=1-the_sentiment_score
    elif x!=0 and y==0:  # 积极情绪值不为0，消极情绪值为0，则为积极情绪结果，并将结果化1
        the_sentiment_score=x/(x+a[0][2]+a[0][3]+a[0][4]+a[0][5])
        if the_sentiment_score<0.5:
            the_sentiment_score=1-the_sentiment_score
    else:  # 积极情绪值和消极情绪值均不为0，且不相等，则情绪结果以积极情绪值占比为主，大于0.5则为积极，小于0.5则为消极
        the_sentiment_score=x/(x+y)
    return the_sentiment_score
