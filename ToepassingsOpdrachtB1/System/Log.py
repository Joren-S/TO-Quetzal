def makeLog(history):
    logfile = open("log_template.html", 'r').read()

    # The following lines make the table header bar. For this we need
    # the different werknemers, chocolades and extras from the system

    # Implementation: replace werknemers with appropriate source
    werknemers = self.getWerknemers
    t_werknemers = ""
    for persoon in werknemers:
        t_werknemers += "<th>\n"
        t_werknemers += persoon + "\n"
        t_werknemers += "</th>\n"
    logfile = logfile.replace("%WERKNEMERS%", t_werknemers)

    # replace chocolades with appropriate source
    chocolades = ["Wit", "Melk", "Bruin", "Zwart"]
    t_chocolades = ""
    for choco in chocolades:
        t_chocolades += "<th>\n"
        t_chocolades += choco + "\n"
        t_chocolades += "</th>\n"
    logfile = logfile.replace("%CHOCOLADES%", t_chocolades)

    # replace chocolades with appropriate source
    extras = ["Honing", "Marshmallow", "Chili"]
    t_extras = ""
    for extra in extras:
        t_extras += "<th>\n"
        t_extras += extra + "\n"
        t_extras += "</th>\n"
    logfile = logfile.replace("%EXTRAS%", t_extras)

    # The following lines make up the table body
    # for implementation: get each history moment as an object and put them in a list

    history = ["0", "1", "2", "3"]
    t_table = ""

    for moment in history:
        t_newline = ""

        #use moment.getTijdstip() instead of tijdstip which is "0". Be sure to convert to string if necessary
        t_newline += "<tr>\n"
        t_newline += "<td>"
        t_newline += moment
        t_newline += "</td>"

        #Get moment.getWorkloadstack() instead of workloadstack which is now generically chosen.
        workloadstack = "5 7 9"
        t_newline += "<td>"
        t_newline += workloadstack
        t_newline += "</td>"

        #For each werknemer, get their occupation at time of history with moment.getWerknemerWorkload(werknemer)
        for i in werknemers:
            t_newline += "<td>"
            t_newline += " "
            t_newline += "</td>"

        # If this moment brings a new bestelling, put it here with moment.getNieuweBestelling()
        t_newline += "<td>"
        t_newline += " "
        t_newline += "</td>"

        # Get all wachtende bestellingen with moment.getWachtendeBestelling()
        t_newline += "<td>"
        t_newline += " "
        t_newline += "</td>"

        for i in chocolades:
            t_newline += "<td>"
            # moment.getStock(i)
            t_newline += "20"
            t_newline += "</td>"

        for i in extras:
            t_newline += "<td>"
            # moment.getStock(i)
            t_newline += "10"
            t_newline += "</td>"

        t_newline += "</tr> \n"
        t_table += t_newline

    logfile = logfile.replace("%BESTELLINGTABLE%", t_table)

    print(logfile)

    with open("output_log.html", "w") as target:
        target.write(logfile)

