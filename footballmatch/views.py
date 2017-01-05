from django.shortcuts import render, redirect
from DatabaseManager import DB

db = DB()


def main(request):
    msgs = []
    if 'date1' in request.GET and 'date2' in request.GET and request.GET['date1'] != '' and request.GET['date2'] != '':
        matches = db.searchDate(request.GET['date1'], request.GET['date2'])
    elif 'res' in request.GET:
        matches = db.searchWin(request.GET['res'])
    elif ('fullword' in request.GET and request.GET['fullword'] != '') or ('incword' in request.GET and request.GET['incword'] != '') or ('excword' in request.GET and request.GET['excword'] != ''):
        matches = db.search(request.GET['fullword'], request.GET['incword'], request.GET['exword'])
    else:
        matches = db.getMatchList()
    return render(request, "main.html", {'matches': matches})


def add(request):
    if request.method == 'GET':
        teams = db.getTeamList()
        stadium = db.getStadiumList()
        return render(request, 'add_page.html', {'teams': teams, 'stadium': stadium})
    elif request.method == 'POST':
        db.saveMatch(request.POST['team1_id'], request.POST['team2_id'], request.POST['stadium_id'],
                     request.POST['score1_id'], request.POST['score2_id'], request.POST['entry-day-time'])
        return redirect('/')


def initialize_database(request):
    database = DB()
    database.initialization()
    return redirect('/')


def edit(request, id):
    if request.method == 'GET':
        matches = db.getMatch(id)
        stadium = db.getStadiumList()
        teams = db.getTeamList()
        return render(request, 'edit_page.html', {'matches': matches, 'stadium': stadium, 'teams': teams})
    else:
        db.editMatch(request.POST['team1_id'], request.POST['team2_id'], request.POST['stadium_id'],
                     request.POST['score1_id'], request.POST['score2_id'], request.POST['entry-day-time'], id)
        return redirect('/')


def remove(request, id):
    db.removeMatch(id)
    return redirect('/')
