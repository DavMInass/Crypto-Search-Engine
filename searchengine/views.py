from django.shortcuts import render
from django.views import generic
from searchindex.query import run_query
from searchengine.models import Document
import re
from searchindex.query_completion import complete_query
from django.http import JsonResponse

# Create your views here.


class Index(generic.TemplateView):
    template_name = "search.html"


class Search(generic.ListView):
    template_name = "search.html"
    context_object_name = 'searchresults'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET['query']
        doc_ids, words = run_query(query)

        if not doc_ids:
            return ['No Results']

        docs = [Document.objects.get(doc_no=doc_id) for doc_id in doc_ids]
        sorted_docs_by_count = sorted(docs, key=lambda d:d.views_count, reverse=True)

        md = []
        for doc in sorted_docs_by_count:
            # Highlight words in the document title
            title = highlight_words(doc.title, words)

            # Highlight words in the document text
            text = highlight_words(doc.text, words)

            # Format the document
            formatted_doc = format_result(doc.doc_no, title, text, doc.views_count)

            # Add the formatted document to the results
            md.append(formatted_doc)

        if len(md) >= 50:
            return md[:50]
        return md


def format_result(doc_no, title, text, views_count):
    link = f"<a href='https://bitcoin.stackexchange.com/questions/{doc_no}'>{title} <span style='font-size:13px; color:white;'><p style='color:white'><img class='viewed' src='https://icon-library.com/images/views-icon/views-icon-10.jpg'/>Viewed.{views_count}</p></span></a>"
    return f"<h2>{link}</h2><br/>{text}"


def highlight_words(doc, words):
    """Highlight all occurences of the words in the documents"""
    for i in words:
        location = re.search(f"([^\\w])({i})([^\\w])", doc)
        if location:
            # doc_n = location.span()[0]
            # small = doc[doc_n -150 :doc_n +150]

            for i in words:
                html = f'<b><span class="query" style="color:#F7931A">{i}</span></b>'
                doc = re.sub(
                    f"([^\\w])({i})([^\\w])", f"\\1{html}\\3", doc)
                # small = small.replace(i, html)
    return doc


def complete(request):
    # Get the text typed into the textbox
    query = request.GET['q']

    completions = complete_query(query)
    return JsonResponse(completions, safe=False)
