"""Sample texts shared by the scan and command-line tests. Both are invented."""

from __future__ import annotations

HUMAN = ("Last March our export job started timing out for one customer.\n\n"
         "I spent two days blaming the database. It was a retry loop I wrote in 2022 "
         "that doubled the work every time a file was larger than 50 MB.\n\n"
         "We removed the loop on a Thursday. The next Monday the same customer sent "
         "a 400 MB file and it went through in nine minutes.")

SLOP = ("In today's landscape, leaders must leverage robust, seamless workflows to unlock value.\n\n"
        "Here is what changed. It's not about tools. It's about people. We made it faster, cheaper, calmer. "
        "Truly transformative.\n\n"
        "Furthermore, a holistic approach can empower teams to navigate change and foster synergy.\n\n"
        "Thoughts?")
