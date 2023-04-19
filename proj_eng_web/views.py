from django.shortcuts import render
from django.core.cache import cache
from . import terms_work


def index(request):
    return render(request, "index.html")


def terms_list(request):
    terms = terms_work.get_terms_for_table()
    return render(request, "term_list.html", context={"terms": terms})


def add_term(request):
    return render(request, "term_add.html")


def send_term(request):
    if request.method == "POST":
        cache.clear()
        user_name = request.POST.get("name")
        user_email = request.POST.get("email")
        new_term = request.POST.get("new_word", "")
        new_definition = request.POST.get("new_translation", "").replace(";", ",")
        context = {"user": user_name}
        if len(new_definition) == 0 and len(new_term) == 0:
            context["success"] = False
            context["comment"] = "Слово или выражение и перевод должны быть не пустыми"
        elif len(new_term) == 0:
            context["success"] = False
            context["comment"] = "Слово или выражение должно быть не пустым"
        elif len(new_definition) == 0:
            context["success"] = False
            context["comment"] = "Перевод должен быть не пустым"
        else:
            context["success"] = True
            context["comment"] = "Ваше слово или выражение добавлено"
            terms_work.write_term(new_term, new_definition, f"{user_name}/{user_email}")
        if context["success"]:
            context["success-title"] = ""
        return render(request, "term_request.html", context)
    else:
        return add_term(request)


def show_stats(request):
    stats = terms_work.get_terms_stats()
    return render(request, "stats.html", stats)

def terms_play(request):
    trans = terms_work.get_term_to_play()
    return render(request, "terms_play.html", context={"trans": trans})

def check_term(request):
    if request.method == "POST":
        cache.clear()
        known_word_user = request.POST.get("known_word", "")
        known_word_correct = terms_work.get_term_to_check()
        context = dict()
        if known_word_user.lower() != known_word_correct.lower():
            context["success"] = False
            context["comment"] = f"Правильный ответ: {known_word_correct}Вы ввели: {known_word_user}"
            context["correct"] = known_word_correct
            context["user_ans"] = known_word_user
        else:
            context["success"] = True
            context["comment"] = "Вы абсолютно правы! Так держать!"
        return render(request, "terms_play_check.html", context)
    else:
        return terms_play(request)

def add_note(request):
    return render(request, "add_note.html")

def send_note(request):
    if request.method == "POST":
        cache.clear()
        note_name = request.POST.get("new_note", "")
        note_description = request.POST.get("new_note_description")
        terms_work.write_note(note_name, note_description)
        return index(request)
    else:
        return add_note(request)

def show_notes(request):
    notes = terms_work.get_notes_to_show()
    return render(request, "notes.html", context={"notes": notes})
