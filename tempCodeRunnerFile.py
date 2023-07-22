 if request.method == "POST":
        players = player_database.query.filter_by(team="nyj").filter(player_database.year > 2010)
        for player in players:
            name = player.name
            team = teams.get(player.team)
            output = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user",
                "content":
                        "Write a 5 sentence summary about "+name+"s career with the "+team+". Be certain to include when he joined the team(year), how he joined the team(drafted, traded for, or signed as free agent), how he left the team (year), and how he left the team (traded, cut, or retired) or if he still on the team. "}]
            )
            content = output.choices[0].message.content
            player.desc = content
        db.session.commit()
        return render_template("ai.html")