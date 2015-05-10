import re

summary_sent_num = 3
ignoreList = open('google-10000-english.txt', 'r').read()

def naiveSummarizer(article_filename):
	f = open(article_filename, 'r')
	abr = open('abbrev', 'r')

	abvDict = makeAbbrevDict(abr)

	# Replace abbreavtions, removing periods for sentence splitting.
	curr_art = f.read()
	for key in abvDict.keys():
		curr_art = curr_art.replace(key, abvDict[key])

	total_size = getArticleWordCount(curr_art)

	similarity_matrix = []
	for line1 in curr_art.split('.'):
		curr_lines = []
		for line2 in curr_art.split('.'):
			if line1 != line2:
				curr_lines.append(similarity(line1, line2)) # Issues with computing similarity - fixed to case ignore comparison and 
		similarity_matrix.append(curr_lines)                # changed the simiarity normailization to float.

	weightDict = {}
	count = 0
	for row in similarity_matrix:
		weightDict[count] = sum(row)
		count += 1

	summ = getSentences(weightDict, curr_art)
	summ_size = getArticleWordCount(summ)

	return summ, summ_size/float(total_size)

def makeAbbrevDict(abrFile):
	abbrevationDict = {}
	for line in abrFile:
		abbrevationDict[line.strip().split(' ')[0]] = line.strip().split(' ')[1]

	return abbrevationDict

def getArticleWordCount(curr_article):
	return len(re.split('. | \s', curr_article))

def similarity(sent1, sent2):
	sim_count = 0
	avg_len = (len(sent1.split(' ')) + len(sent2.split(' ')))/float(2)
	for word in sent1.split(' '):
		for word_other in sent2.split(' '):
			if word.lower() == word_other.lower() and word.lower() not in ignoreList:
				sim_count += 1

	return (sim_count/avg_len)

# After we have a weighted dictionary we use it to 
# extract the particular senteces from the article.
def getSentences(weight_dict, curr_art):
	summary = ''
	sentenceIndecies = []
	sentWeights = []
	vals = weight_dict.values()

	for i in range(summary_sent_num):
		curr_max = max(vals)
		curr_min = min(vals)
		sentWeights.append(curr_max)
		sentWeights.append(curr_min)
		vals.remove(curr_min)
		vals.remove(curr_max)

	for key, val in weight_dict.iteritems():
		if val in sentWeights:
			sentenceIndecies.append(key)

	# if len(curr_art.split('.')) - 2 not in sentenceIndecies:
	# 	sentenceIndecies.append(len(curr_art.split('.')) - 2)

	sentenceIndecies = sorted(sentenceIndecies)
	sentence_arr = curr_art.strip().split('.')
	for index in sentenceIndecies:
		summary += sentence_arr[index] + '. \n'
		summary += '\n'

	return summary


if __name__ == '__main__':
	summ_text, sum_reduction = naiveSummarizer('extracted_article')
	print summ_text
	print "The summary is " + str(sum_reduction * 100) + "% of total"