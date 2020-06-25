import matplotlib, wordcloud, pickle, progressbar, copy, pdb
from konlpy.tag import Okt 

def wcComment(comments, file_path = 'wordcould_resut.png', numWord = 50,
              wcBackround_color = 'white', 
              font_path = None, 
              min_font_size = 4, 
              max_font_size = None,
              width = 400, 
              height = 200, 
              scale = 1,
              exceptionWords = None) :

    corpus = tokenizeComments(comments)       
    corpus = trimNouns(corpus)         
    corpus = removeWords(corpus, exceptionWords)
    
    wordsFreqDict  = sortNouns(corpus, numWord, decreasing = True)

    wc = wordcloud.WordCloud(background_color = wcBackround_color, 
                             font_path = font_path, 
                             min_font_size = min_font_size,
                             max_font_size = max_font_size,
                             scale = scale, 
                             width = width, 
                             height = height)
    gen = wc.generate_from_frequencies(wordsFreqDict)

    matplotlib.pyplot.figure()
    matplotlib.pyplot.imshow(gen, interpolation = 'bilinear')
    wc.to_file(file_path)

    matplotlib.pyplot.close()

def tokenizeComments(comments) :
    # progress bar define 
    numComments = len(comments)
    bar = progressbar.ProgressBar(maxval  = numComments,
                                widgets = [' [', progressbar.Timer(), '] ', progressbar.Bar(), ' (', progressbar.ETA(), ') ',]).start()
    bar_index =  1

    # tokenizing 
    MorphemeAnalyzer = Okt()
    nouns = []
    for comment in comments :
        nouns += MorphemeAnalyzer.nouns(comment['text'])
        
        bar.update(bar_index)
        bar_index += 1
    bar.finish()

    return nouns

def trimNouns(nouns, lenWord = 1) : 
    temp_nouns = []
    for word in nouns :
        if len(word) > 1 :
            temp_nouns.append(word)
    nouns = copy.deepcopy(temp_nouns)

    return nouns

def sortNouns(nouns, numWord, decreasing = False) : 
    nounsFreqDict = {}
    for word in set(nouns) :
        nounsFreqDict[word] = nouns.count(word)
    nounsFreqDict = sorted(nounsFreqDict.items(), key = (lambda item: item[1]), reverse = decreasing)
    nounsFreqDict = nounsFreqDict[:numWord]
    nounsFreqDict = {key : value for key, value in nounsFreqDict}

    return nounsFreqDict

def removeWords(words,exceptionWords) :
    if exceptionWords == None :
        return words

    result_words = []
    for word in words :
        if word not in exceptionWords :
            result_words.append(word)

    return result_words
