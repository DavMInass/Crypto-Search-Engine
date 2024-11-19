from searchindex.build_index import index
from searchindex.preprocessing import preprocess_line_en
from searchengine.models import Document
import re
import math


def run_ranked_search(query):
    # Preprocess the query
    words = preprocess_line_en(query)
    scores = {}

#    Loop ove every word in the query
# """
# for term in words:
#     if term in index:
#         doc_ids = index[term]
#         for doc_id in doc_ids:
#             term_freq = index[term][doc_id].freq
#             doc_freq = index[term].docFreq
#             weight =(1 + math.log10(term_freq)) * math.log10(index.docCount / doc_freq)

# """
    for word in words:
        docs = index.get(word, [" No results"])

        for doc_id in docs:
            score = (1 + math.log10(docs[doc_id].freq)) * \
                math.log10(index.docCount / docs.docFreq)

            if (doc_id in scores):
                scores[doc_id] += score
            else:
                scores[doc_id] = score

    sorted_scores_ids = sorted(scores, key=scores.get, reverse=True)
    sorted_scores = {doc_id: scores[doc_id] for doc_id in sorted_scores_ids}
    #    print(sorted_scores)

    return sorted_scores


def run_query(query):
    words = preprocess_line_en(query)
    if not words:
        return [], words
    nums = []

    if ' and not ' in query:

        res1 = set(index.get(words[0], []))
        res2 = set(index.get(words[1], []))

        all_doc_ids = set([str(doc.doc_no) for doc in Document.objects.all()])
        not_res2 = all_doc_ids.difference(res2)

        nums = res1.intersection(not_res2)
        nums = [int(i) for i in nums]

    # and search
    elif ' and ' in query:
        #    words.remove("and")
        res1 = set(index.get(words[0], []))
        res2 = set(index.get(words[1], []))

        nums = res1.intersection(res2)

    elif ' or not ' in query:
        res1 = set(index.get(words[0], []))
        res2 = set(index.get(words[1], []))

        all_doc_ids = set([str(doc.doc_no) for doc in Document.objects.all()])

        not_res2 = all_doc_ids.difference(res2)

        nums = res1.union(not_res2)
        nums = [int(i) for i in nums]

    # or search
    elif ' or ' in query:
        #    words.remove("or")

        res1 = set(index.get(words[0], []))
        res2 = set(index.get(words[1], []))

        nums = res1.union(res2)

    else:
        # one word
        nums = run_ranked_search(query)

    # -----------
    return nums, words

    # res = {}
    # for i in nums:
    #     try:96
    #         res[str(i)] = index.get(words[0], ["No Results"])[i]
    #     except:
    #         res[str(i)] = index.get(words[1], ["No Results"])[i]

    # return res
