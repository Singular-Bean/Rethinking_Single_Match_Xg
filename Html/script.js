// script.js
document.getElementById('shotmapForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const league = document.getElementById('league').value;
    const season = document.getElementById('season').value;
    const xgMin = parseFloat(document.getElementById('xgMin').value);
    const xgMax = parseFloat(document.getElementById('xgMax').value);

    const leagueId = await fetchLeagueId(league);
    const seasonId = await fetchSeasonId(leagueId, season);
    const matches = await fetchMatches(seasonId, leagueId);

    const shots = await fetchShots(matches);

    plotShots(shots, xgMin, xgMax);
});

async function fetchLeagueId(league) {
    const response = await fetch(`https://www.sofascore.com/api/v1/search/unique-tournaments?q=${league}&page=0`);
    const data = await response.json();
    return data.results[0].entity.id;
}

async function fetchSeasonId(leagueId, season) {
    const response = await fetch(`https://www.sofascore.com/api/v1/unique-tournament/${leagueId}/seasons`);
    const data = await response.json();
    const seasonData = data.seasons.find(s => s.year === season);
    return seasonData.id;
}

async function fetchMatches(seasonId, leagueId) {
    const response = await fetch(`https://www.sofascore.com/api/v1/unique-tournament/${leagueId}/season/${seasonId}/events/round/1`);
    const data = await response.json();
    return data.events.map(event => event.id);
}

async function fetchShots(matches) {
    const shots = [];
    for (const matchId of matches) {
        const response = await fetch(`https://www.sofascore.com/api/v1/event/${matchId}/shotmap`);
        const data = await response.json();
        shots.push(...data.shotmap);
    }
    return shots;
}

function plotShots(shots, xgMin, xgMax) {
    const ctx = document.getElementById('shotmapCanvas').getContext('2d');
    const chart = new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Shots',
                data: shots.filter(shot => shot.xg >= xgMin && shot.xg <= xgMax).map(shot => ({
                    x: shot.playerCoordinates.x,
                    y: shot.playerCoordinates.y,
                    backgroundColor: shot.shotType === 'goal' ? 'red' : 'white',
                    borderColor: 'black',
                    borderWidth: 1
                }))
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom',
                    min: 0,
                    max: 100
                },
                y: {
                    min: 0,
                    max: 75
                }
            }
        }
    });
}